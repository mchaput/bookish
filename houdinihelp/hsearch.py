import re

from whoosh import fields, columns

from bookish import paths, util, functions
from bookish.search import default_fields, Searchables, index_mode
from houdinihelp.api import nodetype_to_path, path_to_nodetype


# Helper functions

def find_parms(block):
    """
    Recursively finds dt blocks inside containers (but doesn't recurse inside
    the dt blocks). This is necessary because for bad historical reasons nodes
    docs don't mark parameters as items like they should.
    """

    if block.get("type") in ("dt", "parameter"):
        yield block
    elif block.get("container"):
        body = block.get("body", ())
        for subblock in body:
            for x in find_parms(subblock):
                yield x


#

ws_exp = re.compile("[\t\r\n ]+")


houdini_fields = {
    "bestbet": fields.KEYWORD,
    "status": fields.ID(stored=True),
    "superclass": fields.ID(stored=True),
    "replaces": fields.KEYWORD(stored=True),
    "version": fields.ID,
    "summary": fields.STORED,
    "helpid": fields.KEYWORD,
    "context": fields.KEYWORD(commas=True, stored=True),
    "namespace": fields.KEYWORD(commas=True, stored=True),
    "examplefile": fields.STORED,
    "examplefor": fields.KEYWORD(stored=True),
    "uses": fields.KEYWORD,
    "group": fields.ID(sortable=columns.RefBytesColumn(), stored=True),
}


class HoudiniSearchables(Searchables):
    @staticmethod
    def _attr(attrs, name):
        return attrs.get(name) or None

    def schema(self):
        fs = default_fields
        fs.update(houdini_fields)
        return fields.Schema(**fs)

    def _should_index_block(self, block):
        attrs = block.get("attrs")
        status = attrs.get("status") if attrs else None
        if status in ("ni", "nd"):
            return False

        return index_mode(block) != "no"

    def _should_index_document(self, pages, path, root, block):
        # Hide nodes that are hidden or superceded
        # Only do this test at the top level (not for every sub-doc)
        if path.startswith("/nodes/") and block is root:
            # See if we can turn the path into a nodetype using HOM
            nodetype = path_to_nodetype(path)
            if nodetype:
                if nodetype.hidden() or nodetype.deprecated():
                    return False

                # Check if the node has been superseded by a more recent version
                order = nodetype.namespaceOrder()
                if order and nodetype.name() != order[0]:
                    return False

        rootattrs = root.get("attrs")
        pagetype = rootattrs.get("type") if rootattrs else None
        attrs = block.get("attrs")
        blocktype = block.get("type")

        if attrs and attrs.get("status") in ("ni", "nd"):
            return False

        # Recognize Houdini-specific sub-documents
        if blocktype in ("methods_item", "functions_item"):
            return True
        if blocktype == "properties_item" and pagetype == "properties":
            return True

        parent = super(HoudiniSearchables, self)
        return parent._should_index_document(pages, path, root, block)

    def _make_doc(self, pages, path, root, block, text):
        parent = super(HoudiniSearchables, self)
        doc = parent._make_doc(pages, path, root, block, text)

        blocktype = block.get("type")
        if blocktype in ("methods_item", "functions_item"):
            self._process_method(pages, path, root, block, doc)
        elif blocktype == "properties_item":
            self._process_property(pages, path, root, block, doc)
        else:
            self._process_doc(pages, path, root, block, doc)

        return doc

    def _process_doc(self, pages, path, root, block, doc):
        # Add Houdini-specific fields to each document
        path = paths.basepath(path)
        attrs = block.get("attrs", {})

        doctype = attrs.get("type", "").strip()
        context = attrs.get("context", "").strip().replace(",", "") or None

        if doctype == "node":
            if context in ("pop", "part") or context.endswith("_state"):
                return
            internal = attrs.get("internal")
            if internal:
                doc["grams"] += " %s" % internal

        if doc.get("category") == "_":
            if path.startswith("/shelf/"):
                doc["category"] = "tool"
            elif path.startswith("/ref/util/"):
                doc["category"] = "utility"
            elif path.startswith("/gallery/shop/"):
                doc["category"] = "gallery/shop"
            elif doctype == "node":
                doc["category"] = "%s/%s" % (doctype, context)
                doc["grams"] += " %s" % context
            elif doctype in ("hscript", "expression", "example", "homclass",
                             "hommodule", "vex"):
                doc["category"] = doctype

        replaces = attrs.get("replaces")
        rsection = functions.subblock_by_id(block, "replaces")
        if rsection:
            rlist = " ".join(link.get("fullpath", "") for link
                             in functions.find_links(rsection))
            if replaces:
                replaces = replaces + " " + rlist
            else:
                replaces = rlist

        doc.update({
            "context": context,
            "bestbet": attrs.get("bestbet"),
            "helpid": attrs.get("helpid"),
            "superclass": attrs.get("superclass"),
            "version": attrs.get("version"),
            "replaces": replaces or None,
            "examplefor": root.get("examplefor"),
            "examplefile": root.get("examplefile"),
            "group": attrs.get("group"),
        })

        # Add example file info
        if root is block and "examplefile" in root:
            otlpath = root["examplefile"]
            # Usages file should be in the same location with .usages ext
            usagespath = paths.basepath(otlpath) + ".usages"
            if pages.exists(usagespath):
                usagescontent = pages.content(usagespath)
                usages = ws_exp.split(usagescontent)
                doc["uses"] = " ".join(usages)

    def _process_method(self, pages, path, root, block, doc):
        blocktype = block.get("type")
        title = self._get_title(root)
        text = self._get_title(block)
        name = text.split("(")[0]
        attrs = block.get("attrs")
        replaces = attrs.get("replaces") if attrs else None

        doc["path"] = "%s#%s" % (path, name)
        doc["title"] = doc["sortkey"] = "%s.%s()" % (title, name)
        doc["grams"] = name
        doc["replaces"] = replaces

        if blocktype == "methods_item":
            doc["type"] = doc["category"] = "hommethod"
        elif blocktype == "functions_item":
            doc["type"] = doc["category"] = "hommethod"

    def _process_property(self, pages, path, root, block, doc):
        name = self._get_title(block)
        attrs = block.get("attrs")
        ifdprop = attrs.get("ifdprop") if attrs else None
        hprop = attrs.get("hprop") if attrs else None

        # Set the best-bet field to the Houdini property name
        doc["title"] = name
        if hprop and hprop != name:
            doc["grams"] = "%s (%s)" % (name, hprop)

        # Set the page fragment to the Houdini or IFD property name
        if hprop:
            ident = hprop
        elif ifdprop:
            ident = ifdprop.replace(":", "_")
        else:
            ident = util.make_id(name)

        doc["path"] = "%s#%s" % (path, ident)
        doc["type"] = doc["category"] = "property"


# Functions for indexing example usages

def gather_node_paths(node, pathset):
    # Recursively examines every node under a starting subnet, converts the
    # node into a help path, and adds it to the given set

    nodetype = node.type()
    tablename = nodetype.category().name()
    typename = nodetype.name()

    # Try to ignore uninteresting nodes
    if typename != "subnet" and tablename not in ("VopNet", "Manager"):
        path = nodetype_to_path(nodetype)
        pathset.add(path)

    for n in node.children():
        # Ignore nodes inside locked assets
        if not n.isInsideLockedHDA():
            gather_node_paths(n, pathset)


def usages_for_otl(otlpath):
    import hou

    # HOM doesn't like unicode
    otlpath = otlpath.encode("utf8")
    # ...or backslashes
    otlpath = otlpath.replace("\\", "/")

    pathset = set()
    hou.hda.installFile(otlpath)
    obj = hou.node("/obj")
    for hdadef in hou.hda.definitionsInFile(otlpath):
        n = obj.createNode(hdadef.nodeTypeName(), exact_type_name=True)
        gather_node_paths(n, pathset)
        n.destroy()
    hou.hda.uninstallFile(otlpath)
    return pathset
