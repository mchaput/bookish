import re

from bookish import paths, pipeline, functions
from bookish.compat import iteritems, text_type
from bookish.wikipages import WikiPages
from bookish.util import flatten_text


class HoudiniPages(WikiPages):
    def __init__(self, *args, **kwargs):
        WikiPages.__init__(self, *args, **kwargs)
        self._setup_pipelines()

    def _setup_pipelines(self):
        # Get the default pre-processors and add Houdini-specific ones
        preprocs = self._prepipe.processors
        preprocs.extend([HoudiniNodes(), HoudiniShortcuts(), ExampleFiles(),
                         Parameters(), ContentFroms(), Replaces()])

        # Get the default post-processors and add Houdini-specific ones
        postprocs = self._postpipe.processors
        postprocs.extend([HomClasses()])

        # Recompute dependencies and make new pipelines
        self._prepipe = pipeline.make_pipeline(preprocs)
        self._postpipe = pipeline.make_pipeline(postprocs)

        # Tell the AnnotateLinks processor to copy Houdini-specific fields onto
        # links
        anno = self._postpipe.processor_by_class(pipeline.AnnotateLinks)
        anno.add_attrs("context", "status")

        # print("prepipe=", self._prepipe)
        # print("postpipe=", self._postpipe)


# Support functions

scheme_map = {
    "Node": "/nodes/%s",
    "Cmd": "/commands/%s",
    "Exp": "/expressions/%s",
    "Vex": "/vex/functions/%s",
    "Hom": lambda x: "/hom/%s" % (x.replace(".", "/")),
    "Mantra": "/props/mantra#%s",
}


def get_shortcut(scheme, value):
    if scheme in scheme_map:
        template = scheme_map[scheme]
        if callable(template):
            return template(value)
        else:
            return template % value
    else:
        return value


def parse_shortcut(path):
    if path and path[0] == path[0].upper() and ":" in path:
        scheme, value = path.split(":", 1)
        return get_shortcut(scheme, value)
    else:
        return path


# Houdini-specific processors

class HoudiniNodes(pipeline.Processor):
    """
    Sets any missing node-specific information based on HOM calls.
    """

    name = "nodes"
    after = ("properties", )

    def apply(self, block, context):
        path = paths.basepath(context["path"])
        if not path.startswith("/nodes/"):
            return

        # Assume if it doesn't have a parameters section it's not a node
        body = block.get("body", ())
        parms = functions.first_subblock_of_type(body, "parameters_section")
        if not parms:
            return

        from houdinihelp import path_to_components
        from houdinihelp import path_to_nodetype
        from houdinihelp import table_to_dir

        nodeinfo = path_to_components(path)
        if nodeinfo is None:
            return

        # Fill in missing properties from information in path
        attrs = block.setdefault("attrs", {})
        if "type" not in attrs:
            attrs["type"] = "node"
        if "context" not in attrs:
            attrs["context"] = table_to_dir[nodeinfo.table]
        if "internal" not in attrs:
            attrs["internal"] = nodeinfo.corename
        if "version" not in attrs:
            attrs["version"] = nodeinfo.version
        if "namespace" not in attrs:
            attrs["namespace"] = nodeinfo.namespace

        body = block.get("body", ())
        title = functions.first_subblock_of_type(body, "title")
        if title is None:
            # Get the node label from HOM
            nodetype = path_to_nodetype(path)
            if nodetype:
                title = nodetype.description()
                if title:
                    # Create a fake title block and add it to the beginning of
                    # the document body
                    tblock = {"type": "title", "text": [title]}
                    body.insert(0, tblock)


class Replaces(pipeline.Processor):
    """
    Annotates documents with replaces/replacedby relationships.

    This processor finds any "replaces" sections, and any "replaces" properties,
    and copies the paths to a "replaces" list on the document root, making them
    easier to index.

    If a searcher is available, this processor finds any documents that
    "replace" the current path, and adds information about them to a
    "replacedby" list on the document root, making them available to display
    in the document.
    """

    name = "hreplaces"
    after = ("properties",)
    split_expr = re.compile("[ ,]+")
    prefixes = ("/commands/", "/expressions/", "/nodes/")
    fields = ("title", "path", "type", "summary", "icon")

    @staticmethod
    def _do(block):
        attrs = block["attrs"]
        text = attrs["replaces"]
        # Split the space/comma separated string
        replacelist = Replaces.split_expr.split(text)
        if replacelist:
            replaces = []
            for path in replacelist:
                replaces.append(parse_shortcut(path))
            attrs["replaces"] = " ".join(replaces)

    def apply(self, block, context, root=None, in_replaces=False):
        attrs = block.get("attrs", {})
        if root is None:
            root = block

            # Find any documents that replace this one
            searcher = context.searcher
            if searcher:
                path = paths.basepath(context["path"])
                # Only run the search for pages the start with one of the
                # prefixes listed in the class's prefixes attribute
                for prefix in self.prefixes:
                    if path.startswith(prefix):
                        repls = []
                        for doc in searcher.documents(replaces=path):
                            d = {}
                            for f in self.fields:
                                if f in doc:
                                    d[f] = doc[f]
                            repls.append(d)
                        if repls:
                            block["replacedby"] = repls
                        break

        # Look for "replaces" property on block
        if "replaces" in attrs:
            self._do(block)

        # Look for a "replaces" section
        if block.get("role") == "section" and block.get("id") == "replaces":
            in_replaces = True
        elif in_replaces:
            for span in block.get("text", ()):
                if isinstance(span, dict) and span.get("type") == "link":
                    rpath = span.get("fullpath")
                    if rpath:
                        rpath = parse_shortcut(rpath)
                        if "replaces" in root:
                            root["replaces"] += " " + rpath
                        else:
                            root["replaces"] = rpath

        for subblock in block.get("body", ()):
            self.apply(subblock, context, root, in_replaces)


class HoudiniShortcuts(pipeline.TextModifier):
    """
    Implements Houdini-specific link features such as "opdef:" syntax and
    convenience schemes such as "Node:" and "Hom:".
    """

    name = "hshortcuts"
    before = ("promote", "includes")

    do_properties = ("icon", )

    opdef_exp = re.compile("""
    opdef:
    /?  # Optional starting slash... not sure if Houdini supports this
    (?P<spec>[^?;]*)  # Node spec string
    ([?;](?P<section>.*))?  # Optional reference to a section inside the asset
    """, re.VERBOSE)

    @staticmethod
    def _parse_opdef(currentpath, value):
        # Check that the value matches the opdef: regex
        match = HoudiniShortcuts.opdef_exp.match(value)
        if not match:
            return value

        spec = match.group("spec")
        # Supporting "." (meaning "current node") is easy, just tack the
        # section on to the current path
        if spec == ".":
            value = currentpath
        else:
            from houdinihelp.api import components_to_path
            table, namepart = spec.split("/", 1)

            # Because of the flawed design of namespaces/versions, it's
            # impossible to parse the names without asking Houdini. So,
            # suck it up and try to import hou
            try:
                import hou
                cffntn = hou.hda.componentsFromFullNodeTypeName
                # Use this unwieldy function to parse the name
                scopeop, namespace, nodetype, version = cffntn(namepart)
            except ImportError:
                # We can't import hou, so we can't support the fancy
                # scopes/namespaces/versions
                scopeop = None
                namespace = None
                nodetype = namepart
                version = None

            # Convert the components into a server path
            value = components_to_path(table, scopeop, namespace,
                                       nodetype, version)
            # Tack the section on the end
            section = match.group("section")
            if section:
                value += "/%s" % section

        return value

    def apply(self, block, context):
        path = context["path"]
        attrs = block.get("attrs")
        for name in self.do_properties:
            if name in block:
                block[name] = self._parse_opdef(path, block[name])
            if attrs and name in attrs:
                attrs[name] = self._parse_opdef(path, attrs[name])

        if "text" in block:
            self.text(block["text"], context)

        body = block.get("body", ())
        for subblock in body:

            self.apply(subblock, context)

    def text(self, text, context):
        for span in text:
            # Only look at links
            if not (isinstance(span, dict) and span.get("type") == "link"):
                continue
            # Ignore spans this processor has already done
            if span.get("_hs_sc"):
                continue

            # The scheme is the "Node" in [Node:sop/copy]
            scheme = span.get("scheme")
            # The value is the "sop/copy" in [Node:sop/copy]
            value = span.get("value")

            # I hate this, but we have to support using Houdini-style "opdef:"
            # paths in help links to point to sections inside an asset
            if value.startswith("opdef:"):
                value = self._parse_opdef(context["path"], value)
                span["value"] = value

            if scheme == "IncludeProp":
                # This is a convenience to let node help authors include a
                # render property in the parameter documentation; convert it
                # into an include
                span["scheme"] = "Include"
                span["value"] = "/props/mantra#hprop=%s" % value

            elif scheme:
                # Call the "get_shortcut" function to use the scheme_map (above)
                # to deal with Houdini-specific link schemes such as "Node:" and
                # "Hom:"
                span["value"] = get_shortcut(scheme, value)

            span["_hs_sc"] = True

        return text


class ContentFroms(pipeline.Modifier):
    """
    Finds the "#contentfrom:" property and replaces it with an include.
    """

    name = "hcontentfrom"
    after = ("hierarchy",)
    before = ("properties", "includes")

    def modify(self, block, context):
        body = block.get("body")
        if body:
            for i, b in enumerate(body):
                if b.get("type") == "prop" and b.get("name") == "contentfrom":
                    ref = flatten_text(b.get("value"))
                    body[i] = {"type": "include", "ref": ref + "/"}


class HomClasses(pipeline.Processor):
    """
    Implements several features related to HOM pages, such as listing subclasses
    and methods inherited from superclasses.
    """

    name = "homclasses"
    before = ("annotate",)

    def _annotate_subclasses(self, searcher, path, block):
        assert path.startswith("/hom/hou")
        fqname = path[5:].replace("/", ".")
        block["subclasses"] = subclasses = []
        for subdoc in searcher.documents(superclass=fqname):
            subclasses.append({
                "title": subdoc.get("title"),
                "path": subdoc.get("path"),
                "summary": subdoc.get("summary")
            })

    def _get_method_names(self, block):
        methodnames = set()
        section = functions.subblock_by_id(block, "methods")
        if section:
            for methblock in functions.find_items(section, "methods_item"):
                text = functions.string(methblock.get("text"))
                name = text.split("(")[0]
                methodnames.add(name)
        return methodnames

    def _superclasses(self, pages, methodnames, context, block, history=None):
        # Recursively loads the doc pointed to by the block's "superclass"
        # attribute and yields a (path, rootblock) pair for each superclass

        history = history or set()
        attrs = block.get("attrs", {})
        superclass = attrs.get("superclass")
        if superclass:
            path = "/hom/" + superclass.replace(".", "/")
            spath = pages.source_path(path)

            if pages.exists(spath):
                if spath in history:
                    raise Exception("Circular superclass structure")
                else:
                    history.add(spath)

                doc = pages.json(spath, conditional=context.get("conditional"),
                                 postprocess=False)

                titleblock = functions.first_subblock_of_type(doc, "title")
                if titleblock:
                    title = functions.string(titleblock.get("text"))
                else:
                    title = superclass

                # Find the method items on the superclass
                section = functions.subblock_by_id(doc, "methods")
                methods = []
                if section:
                    for methblock in functions.find_items(doc, "methods_item"):
                        text = methblock.get("text")
                        name = functions.string(text).split("(")[0]
                        attrs = methblock.get("attrs", {})
                        body = methblock.get("body", [])

                        # If this name is in the set of seen methods, it's
                        # overridden, so we should skip it
                        if name in methodnames:
                            continue
                        methodnames.add(name)

                        # Copy information about the method into a dict
                        summary = functions.first_subblock_string(methblock)
                        methdict = {
                            "name": name,
                            "text": text,
                            "summary": summary,
                            "more": len(body) > 1,
                        }
                        if "status" in attrs:
                            methdict["status"] = attrs["status"]
                        methods.append(methdict)

                yield {
                    "path": path,
                    "title": title,
                    "methods": methods
                }
                for x in self._superclasses(pages, methodnames, context, doc,
                                            history):
                    yield x

    def apply(self, block, context):
        # Only operate on HOM class documents
        attrs = block.get("attrs", {})
        if attrs.get("type") != "homclass":
            return

        path = paths.basepath(context["path"])
        pages = context.pages
        searcher = context.searcher

        # Find the subclasses using the full-text index
        if searcher:
            self._annotate_subclasses(searcher, path, block)

        # Get a list of methods on this class, so we can check if one of
        # the super methods is overridden
        methodnames = self._get_method_names(block)

        # Recursively load the docs for superclasses
        supers = list(self._superclasses(pages, methodnames, context, block))
        block["superclasses"] = supers


class Parameters(pipeline.Processor):
    name = "hparms"
    after = ("properties", "sections")
    before = ("groups",)

    def apply(self, block, context):
        btype = block.get("type")
        if btype == "root":
            attrs = block.get("attrs", {})
            if attrs.get("type") == "node":
                parmsblock = functions.subblock_by_id(block, "parameters")
                if parmsblock:
                    self.apply(parmsblock, context)
        elif block.get("type") == "dt":
            block["type"] = "parameters_item"
            block["role"] = "item"
        elif block.get("type") == "dt_group":
            block["type"] = "parameter_group"
            for subblock in block.get("body", ()):
                self.apply(subblock, context)
        elif block.get("container"):
            for subblock in block.get("body", ()):
                self.apply(subblock, context)


class ExampleFiles(pipeline.Processor):
    """
    For example files, computes the nodes and example files and adds them as
    annotations on the document.

    For node docs, searches for examples related to the node.
    """

    name = "hexamples"
    before = ("includes",)

    def apply(self, block, context):
        # At the document root
        if block.get("type") == "root":
            attrs = block.get("attrs", {})
            path = context["path"]
            dirpath, filename = paths.split_dirpath(path)

            is_node_eg = (path.startswith("/examples/nodes/") and
                          not filename.startswith("_"))
            is_panel_eg = (path.startswith("/examples/python_panels/") and
                           not filename.startswith("_"))

            if is_node_eg or is_panel_eg:
                # This file is an example
                self._process_example_page(block, context, is_node_eg,
                                           is_panel_eg)

            elif attrs.get("type") == "node":
                # This is a node, add associated examples
                self._process_node_page(block, context)

        # The other stuff needs a searcher to work
        if not context.searcher:
            return

        # Look for :load_example: items
        body = block.get("body")
        blocktype = block.get("type")
        if blocktype == "load_example":
            self._process_load_block(block, context)
        elif blocktype == "list_examples":
            self._process_list_block(block, context)
        elif body:
            for sub in body:
                self.apply(sub, context)

    @staticmethod
    def _process_load_block(block, context):
        pages = context.pages
        attrs = block.setdefault("attrs", {})
        egpath = attrs.get("path")
        egfile = attrs.get("examplefile")
        title = functions.string(block.get("text"))
        body = block.get("body")
        if egpath:
            # If the user gave a path to an example description file, load
            # it and use it to fill in any missing bits
            egsrc = pages.source_path(egpath)
            if pages.exists(egsrc):
                egdata = pages.json(egpath, context)
                egbody = egdata.get("body", [])
                # Fill in example file path
                if not egfile:
                    attrs["examplefile"] = egdata.get("examplefile")
                # Fill in example text body
                if not body and attrs.get("include") == "yes":
                    block["body"] = egbody
                # Fill in example title
                if not title:
                    tb = functions.first_subblock_of_type(egbody, "title")
                    block["text"] = tb.get("text", [])

    @classmethod
    def _make_load_example(cls, hit):
        egpath = hit["path"]
        return {
            "type": "load_example",
            "attrs": {
                "path": egpath,
                "examplefile": hit.get("examplefile"),
                "examplefor": hit.get("examplefor"),
            },
            "text": hit.get("title", egpath),
            "body": [
                {
                    "type": "include",
                    "ref": egpath,
                }
            ]
        }

    @classmethod
    def _hits_to_blocks(cls, hits):
        for hit in hits:
            if paths.basename(hit["path"]) != "_index":
                yield cls._make_load_example(hit)

    @classmethod
    def _process_list_block(cls, block, context):
        searcher = context.searcher
        r = pipeline.RunSearches.get_results(block, context)
        attrs = block.get("attrs", {})
        body = block.setdefault("body", [])

        if not r.is_empty():
            if "groupedby" in attrs:
                for key, docnums in sorted(r.groups().items()):
                    hits = searcher.group_hits(docnums)

                    # The type CANNOT end in _group, because there's a step in
                    # the pipeline that coalesces adjacent groups of the same
                    # type
                    body.append({
                        "type": "grouped_examples", "key": key,
                        "body": list(cls._hits_to_blocks(hits)),
                        "container": True,
                    })
            else:
                body.extend(cls._hits_to_blocks(r))

    def _process_example_page(self, block, context, is_node_eg, is_panel_eg):
        path = context["path"]
        attrs = block.get("attrs", {})

        # Example authors are very lax about giving the example documents
        # titles; if the document doesn't have a title, make one up from the
        # file name
        title = functions.first_subblock_of_type(block, "title")
        if not title:
            name = text_type(paths.barename(path))
            body = block.setdefault("body", [])
            body.insert(0, {
                "type": "title", "indent": 0, "text": [name]
            })

        # Check for an explicit exampleFor property, otherwise guess it
        # from the example's directory tree
        if is_node_eg:
            block.setdefault("attrs", {})["type"] = "example"

            if "exampleFor" in attrs:
                egfor = attrs["exampleFor"]
            elif "examplefor" in attrs:
                egfor = attrs["examplefor"]
            else:
                egfor = self._node_path_from_example_path(path)
            # Attach the list of nodes to the root
            block["examplefor"] = egfor

        egpath = None
        # Check for an explicit exampleFile property, otherwise guess it
        # by looking for the example name with an extension
        if "exampleFile" in attrs:
            egpath = attrs["exampleFile"]
        elif "examplefile" in attrs:
            egpath = attrs["examplefile"]
        elif is_node_eg:
            base = paths.basepath(path)
            for ext in (".hda", ".otl"):
                egpath = base + ext
                if context.pages.exists(egpath):
                    break
        elif is_panel_eg:
            egpath = self._file_path_from_panel_path(path)

        if egpath:
            egpath = paths.join(path, egpath)
            if context.pages.exists(egpath):
                block["examplefile"] = egpath

    def _process_node_page(self, block, context):
        path = context["path"]
        pages = context.pages
        searcher = context.searcher
        if not searcher:
            return

        # Look for an examples section on this page
        body = block.setdefault("body", [])
        egblock = functions.first_subblock_of_type(body, "examples_section")
        if egblock:
            found = True
        else:
            # This page doesn't have an examples section, we have to
            # make one
            found = False
            egblock = {
                "type": "examples_section", "role": "section",
                "id": "examples", "level": 1,
                "text": "Examples",
            }
        has_egs = False

        # Find direct examples
        vpath = paths.basepath(path)
        egdocs = searcher.documents(examplefor=vpath)
        if egdocs:
            # Put them in an attribute on the examples section
            egblock["examples"] = self._example_items(pages, egdocs, context,
                                                      include=True)
            has_egs = True

        # Find usages
        usagedocs = searcher.documents(uses=vpath)
        if usagedocs:
            # Put them in an attribute on the examples section
            egblock["usages"] = self._example_items(pages, usagedocs, context)
            has_egs = True

        # If we have examples and the page didn't have its own examples
        # section, append the one we made to the body
        if has_egs and not found:
            body.append(egblock)

    @staticmethod
    def _node_path_from_example_path(path):
        # Guess the node based on what directory the example is in
        parts = paths.norm_parts(path)
        # Remove the examples prefix
        assert parts.pop(1) == "examples/"
        # Remove the filename from the end
        parts.pop()
        # Put the path back together
        nodepath = "".join(parts)
        if nodepath.endswith("/"):
            nodepath = nodepath[:-1]
        return nodepath

    @staticmethod
    def _file_path_from_panel_path(path):
        return paths.basepath(path) + ".pypanel"

    @staticmethod
    def _example_items(pages, egdocs, context, include=False):
        items = []
        for egdoc in egdocs:
            data = {}
            if include:
                egdata = pages.json(egdoc["path"], context)
                if egdata:
                    body = egdata.get("body", ())
                    attrs = egdata.get("attrs", {})
                    title = functions.first_subblock_of_type(body, "title")
                    summary = functions.first_subblock_of_type(body, "summary")

                    data["body"] = body
                    data["examplefile"] = attrs.get("examplefile")
                    data["examplefor"] = attrs.get("examplefor")

                    if title:
                        data["title"] = title.get("text", ())
                    if summary:
                        data["summary"] = summary.get("text", ())

            if not data.get("title"):
                data["title"] = egdoc.get("title")
            if not data.get("summary"):
                data["summary"] = egdoc.get("summary")
            if not data.get("examplefile"):
                data["examplefile"] = egdoc.get("examplefile")
            if not data.get("examplefor"):
                data["examplefor"] = egdoc.get("examplefor")
            data["path"] = egdoc["path"]
            data["key"] = egdoc.get("title", "")
            items.append(data)

        items.sort(key=lambda d: d["key"])
        return items

