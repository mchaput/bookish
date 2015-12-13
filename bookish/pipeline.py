# Copyright 2013 Matt Chaput. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY MATT CHAPUT ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL MATT CHAPUT OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of Matt Chaput.

from __future__ import print_function

import copy
import logging
from collections import defaultdict

from pygments.lexers import get_lexer_for_filename

from bookish import paths, stores, functions
from bookish.compat import configparser, BytesIO
from bookish.compat import iteritems, string_type
from bookish.util import join_text


logger = logging.getLogger(__name__)


# Exceptions

class CircularIncludeError(Exception):
    pass


# Utility functions

def find_by_attr(top, name, value):
    for b in functions.find_all_breadth(top):
        if name == "id" and functions.string(b.get("id")) == value:
            yield b
        elif "attrs" in b and functions.string(b["attrs"].get(name)) == value:
            yield b


def first_by_attr(top, name, value):
    for b in find_by_attr(top, name, value):
        return b


def find_id(top, value):
    return first_by_attr(top, "id", value)


# Base classes

class Processor(object):
    """
    Base class for objects that walk a document tree modifying the blocks in
    place.
    """

    name = ""

    def __repr__(self):
        return "<%s:%s>" % (type(self).__name__, self.name)

    def __or__(self, other):
        return Pipe([self, other])

    def add(self, other):
        return Pipe([self, other])

    def apply(self, block, context):
        pass


class Pipe(Processor):
    """
    Processor that wraps multiple processor objects and calls them each in turn.
    """

    def __init__(self, processors):
        self.processors = []
        for v in processors:
            self.add(v)

    def __repr__(self):
        return "<%s %r>" % (type(self).__name__, self.processors)

    def add(self, other):
        if isinstance(other, Pipe):
            for v in other.processors:
                self.add(v)
        elif self.processors and isinstance(other, Modifier):
            last = self.processors[-1]
            if isinstance(last, MultiModifier):
                last.add(other)
            elif isinstance(last, Modifier):
                self.processors[-1] = MultiModifier([last, other])
            else:
                self.processors.append(other)
        elif isinstance(other, Processor):
            self.processors.append(other)
        else:
            raise Exception("Can't add %s %r to pipeline"
                            % (type(other), other))

    def processor_by_class(self, cls):
        for proc in self.processors:
            if isinstance(proc, cls):
                return proc

    def apply(self, block, context):
        for v in self.processors:
            v.apply(block, context)


class MultiModifier(Processor):
    """
    Processor that wraps multiple Modifier objects. This object walks the document
    tree and calls each modifier on each block.
    """

    def __init__(self, modifiers):
        self.modifiers = modifiers

    def __repr__(self):
        return "<%s %r>" % (type(self).__name__, self.modifiers)

    def add(self, modifier):
        self.modifiers.append(modifier)

    def apply(self, block, context):
        for m in self.modifiers:
            m.apply(block, context)
        for subblock in block.get("body", ()):
            self.apply(subblock, context)


class Modifier(Processor):
    """
    A type of Processor that only modifies a single block at a time (that is, that
    doesn't care about hierarchy). This allows them to be grouped together in a
    MultiModifier.
    """

    def modify(self, block, context):
        raise NotImplementedError

    def apply(self, block, context):
        self.modify(block, context)
        body = block.get("body", ())
        for subblock in body:
            if not isinstance(subblock, dict):
                raise Exception("body contains %r" % (subblock))
            self.apply(subblock, context)


# Block processors

class Title(Processor):
    """
    Finds the page title and summary blocks and copies their text up to the root
    for easier access by other code.
    """

    name = "title"

    def apply(self, block, context):
        for subblock in block.get("body", ()):
            sbtype = subblock.get("type")
            if sbtype == "title":
                block["title"] = subblock.get("text")
            elif sbtype == "summary":
                block["summary"] = subblock.get("text")


class Hierarchy(Processor):
    """
    Organizes a linear list of blocks into a hierarchy based on the relative
    values of a key (usually "indent").
    """

    name = "hierarchy"

    def __init__(self, attr="indent", default=0):
        """
        :param attr: The key to use to determine the hierarchical level of
            a given block.
        :param default: The value to use for blocks that don't have the
            attribute key.
        """

        self.attr = attr
        self.default = default

    def apply(self, block, context):
        attr = self.attr
        default = self.default

        body = block.get("body")
        if body:
            newbody = []
            lastvalue = None
            lastblock = None
            for subblock in body:
                value = subblock.get(attr, default)
                if lastblock is not None and value > lastvalue:
                    if "body" not in lastblock:
                        lastblock["body"] = []

                    lastblock["body"].append(subblock)
                else:
                    newbody.append(subblock)
                    lastblock = subblock
                    lastvalue = value
            block["body"] = newbody

            if newbody:
                for subblock in newbody:
                    self.apply(subblock, context)


class SortHeadings(Processor):
    """
    Implements "linear" header style, where blocks simply come after headers at
    the same indent, instead of being indented under the heading. This processor
    looks for headings without bodies and pulls any subsequent blocks into them.
    """

    name = "sortheadings"
    after = ("hierarchy",)

    def apply(self, block, context):
        body = block.get("body")
        if not body:
            return

        newbody = []
        inheading = False
        currentlevel = None
        for sb in body:
            if sb.get("container"):
                level = sb.get("level", 0)
                if inheading and level > currentlevel:
                    newbody[-1]["body"].append(sb)
                else:
                    if "body" not in sb:
                        sb["body"] = []
                    newbody.append(sb)
                    inheading = True
                    currentlevel = level
            else:
                if inheading:
                    newbody[-1]["body"].append(sb)
                else:
                    newbody.append(sb)
        block["body"] = newbody

        if newbody:
            for subblock in newbody:
                self.apply(subblock, context)


class Groups(Processor):
    """
    Groups blocks of the same type "N" under "group_N" superblocks.
    """

    name = "groups"
    after = ("hierarchy", "sections")

    def __init__(self, types=("bullet", "ord", "dt", "item")):
        """
        :param whitelist: if not empty, only type names in this collection
            will be grouped.
        :param blacklist: if not empty, no type names in this collection will
            be grouped.
        """

        self.types = frozenset(types)

    def apply(self, block, context):
        # if context.get("include_history"):
        #     return

        body = block.get("body")
        if not body:
            return

        newbody = []
        current = None

        # Note that this algorithm needs to deal with groups already existing
        # in the data because of includes
        for subblock in body:
            typename = subblock.get("type", "")
            role = subblock.get("role", "")
            groupname = typename + "_group"

            # This block is of a type that should be grouped
            if typename in self.types or role in self.types:
                self.apply(subblock, context)

                # If this is not type of the current grouping, start a new
                # group and push it onto the new body
                if groupname != current:
                    group = {"type": groupname, "body": [], "container": True}
                    if role:
                        group["role"] = "%s_group" % role
                    newbody.append(group)
                # Put the block in the group at the end of the new body
                newbody[-1]["body"].append(subblock)
                # This block's type is now the current grouping
                current = groupname

            # This block is a group that's the same as the current grouping
            elif current is not None and typename and typename == current:
                # Move the items in this group into the group at the end of the
                # new body
                newbody[-1]["body"].extend(subblock["body"])
                # Don't need to change current here

            # This block is a group
            elif typename.endswith("_group") and subblock.get("container"):
                newbody.append(subblock)
                # Make this the current grouping
                current = typename

            # This is some other kind of block
            else:
                self.apply(subblock, context)
                newbody.append(subblock)
                # Reset the grouping to None
                current = None

        block["body"] = newbody


class Properties(Processor):
    """
    Changes "property" blocks into attributes on the parent block.
    Make sure this runs after Hierarchy.
    """

    name = "properties"
    after = ("sortheadings",)

    def apply(self, block, context):
        body = block.get("body")
        if body:
            newbody = []
            for subblock in body:
                if subblock.get("type") == "prop":
                    name = subblock["name"]
                    value = subblock.get("value")
                    if "attrs" in block:
                        attrs = block["attrs"]
                    else:
                        attrs = block["attrs"] = {}
                    attrs[name] = value
                else:
                    newbody.append(subblock)
                    self.apply(subblock, context)

            block["body"] = newbody


class EmptyBlocks(Processor):
    """
    Removes blocks without any content. Ignores certain things.
    """

    name = "empty"

    @staticmethod
    def _can_be_empty(block):
        return (
            block.get("container")
            or block.get("role") == "item"
            or block.get("type") in ("xml", "pxml", "divider", "sep")
        )

    def apply(self, block, context):
        body = block.get("body")
        if body:
            i = 0
            while i < len(body):
                sb = body[i]
                nobody = not sb.get("body")
                notext = not sb.get("text")
                if nobody and notext and not self._can_be_empty(sb):
                    del body[i]
                    continue

                self.apply(sb, context)
                i += 1


class Promote(Processor):
    """
    Finds blocks where a bit of xml or an include is the only thing in the
    block, and "promotes" that span up to block level.
    """

    name = "promote"

    def apply(self, block, context):
        body = block.get("body")
        if body:
            for i, subblock in enumerate(body):
                spans = subblock.get("text")
                if spans and len(spans) == 1 and isinstance(spans[0], dict):
                    only = spans[0]
                    otype = only.get("type")
                    oscheme = only.get("scheme")
                    is_xml = otype == "xml"
                    is_include = ((otype == "link" and oscheme == "Include")
                                  or otype == "include")

                    if is_xml or is_include:
                        # Replace this block with the XML or include inside
                        subbody = subblock.get("body")
                        if subbody:
                            only["body"] = subbody
                        subblock = body[i] = only

                self.apply(subblock, context)


class Sections(Processor):
    """
    Sets the "text" on sections if it wasn't given, and changes the "type" of
    plain items inside a section to a type based on the section name. For
    example, a plain item inside a `@properties` section becomes type
    `properties_item`.
    """

    name = "sections"
    after = ("hierarchy",)

    def apply(self, block, context, itemtype=None):
        # If this is a section...
        if block.get("role") == "section":
            # Give it a title if it doesnt have one
            if not block.get("text"):
                block["text"] = functions.string(block["id"]).capitalize()

            # Take its ID and make an item type from it
            itemtype = block["id"] + "_item"

        blocktype = block.get("type")
        if blocktype == "item" and itemtype:
            # If we're in a section, change this item's type to one based on
            # the section ID
            block["type"] = itemtype

        elif block.get("body"):
            # Recurse inside containers, passing down the item type
            for subblock in block.get("body", ()):
                self.apply(subblock, context, itemtype)


class Includes(Processor):
    """
    Finds include directives and replaces them with the included wiki content.
    """

    name = "includes"
    after = ("promote",)

    @staticmethod
    def _target(root, name, value, unwrap):
        if name:
            if name == "id":
                block = find_id(root, value)
            else:
                block = first_by_attr(root, name, value)

            if block is None:
                return None
            if unwrap:
                return block.get("body")
            else:
                return [block]
        else:
            return root["body"]

    @staticmethod
    def _load_include(path, root, context, icache, name=None, value=None,
                      unwrap=False):
        # Add the current path to the list of included paths
        incd = set(root.get("included", ()))
        incd.add(path)
        root["included"] = list(incd)

        # Create a unique key for this include so we can check for circular
        # includes
        key = "%s#%s=%s" % (path, name, value)
        # Check if the unique key is already in the include history stored in
        # the context
        history = context.get("include_history", frozenset())
        if key in history:
            raise CircularIncludeError("Trying to import %s with import history %r" %
                                       (key, history))

        # In case of recursive includes, create a new context that adds this
        # to the include history
        newhistory = history.union([key])
        icontext = context.push({"include_history": newhistory,
                                 "path": path})
        icontext.pages = context.pages
        icontext.searcher = context.searcher

        # Load the included file
        if path in icache:
            incdata = icache[path]
        else:
            try:
                incdata = context.pages.json(path, icontext, postprocess=False)
            except stores.ResourceNotFoundError:
                return None
            icache[path] = incdata

        assert incdata["type"] == "root"
        if incdata.get("included"):
            # Add the included file's root "included" key to this file's
            root["included"] = sorted(set(root["included"])
                                      | set(incdata.get("included", ())))

        # The _target function takes care of finding a fragment
        return Includes._target(incdata, name, value, unwrap)

    @staticmethod
    def _parse_include_path(incpath):
        name = value = None
        unwrap = False
        incpath, _, frag = incpath.partition("#")
        if frag:
            if frag.endswith("/"):
                unwrap = True
                frag = frag[:-1]
            if "=" in frag:
                name, value = frag.split("=", 1)
            else:
                name = "id"
                value = frag

        return incpath, name, value, unwrap

    def _get_include_content(self, path, root, context, icache, ref):
        incpath, name, value, unwrap = self._parse_include_path(ref)

        if incpath and incpath != paths.basepath(path):
            # The include is in another page
            incpath = paths.join(path, incpath)
            _, ext = paths.split_extension(incpath)
            if not ext:
                incpath = context.pages.source_path(incpath)

            incpath = paths.join(path, incpath)
            return self._load_include(incpath, root, context, icache, name,
                                      value, unwrap)
        elif name and value:
            # If no path was given, or it was this page's path, grab the target
            # from this page
            return self._target(root, name, value, unwrap)

    def _replace_includes(self, objs, context, root, icache):
        i = 0
        thispath = context["path"]
        while i < len(objs):
            sub = objs[i]
            if not isinstance(sub, dict):
                i += 1
                continue

            stype = sub.get("type")
            icontent = None
            if stype == "source":
                attrs = sub.get("attrs", {})
                srcpath = paths.join(thispath, attrs.get("path"))
                content = context.pages.content(srcpath)
                if content:
                    lang = (attrs.get("lang")
                            or get_lexer_for_filename(srcpath).name)
                    icontent = [{
                        "type": "pre", "lang": lang,
                        "text": [content]
                    }]
            else:
                ref = None
                if stype == "link" and sub.get("scheme") == "Include":
                    ref = sub.get("value")
                elif stype == "include":
                    ref = sub.get("ref")
                if ref:
                    icontent = self._get_include_content(thispath, root,
                                                         context, icache, ref)

            if icontent:
                # Splice the content into the block list
                objs[i:i + 1] = icontent
                # ...then move the pointer to after the spliced in content
                i += len(icontent)
            else:
                if sub.get("text"):
                    self._replace_includes(sub["text"], context, root, icache)
                if sub.get("body"):
                    self._replace_includes(sub["body"], context, root, icache)
                i += 1

    def apply(self, block, context, root=None, icache=None):
        if context.get("noinclude") or not context.get("path"):
            return

        icache = {}
        root = root or block
        body = block.get("body")
        self._replace_includes(body, context, root, icache)


class Tables(Processor):
    """
    Because of the way simple tables are marked up, you end up with a cell block
    for each row, where each rightward cell is the only child of the cell to its
    left. This processor re-organizes this into a more render-friendly
    structure.
    """

    name = "tables"
    after = ("hierarchy",)

    def apply(self, block, context):
        body = block.get("body")
        if body:
            if any(b.get("type") == "cell" for b in body):
                newbody = []

                # Find runs of adjacent "cell" blocks in the body
                run = []
                for subblock in body:
                    # If we find a cell, add it to the current run
                    if subblock.get("type") == "cell":
                        run.append(subblock)
                    else:
                        # This is not a cell, so flush the current run
                        if run:
                            # Convert the run to a table block
                            newbody.append(self._run_to_table(run, context))
                            run = []

                        self.apply(subblock, context)
                        newbody.append(subblock)

                if run:
                    newbody.append(self._run_to_table(run, context))

                block["body"] = newbody
            else:
                # No cells here, recurse into the body
                for subblock in body:
                    self.apply(subblock, context)

    def _run_to_table(self, run, context):
        thead = []
        tbody = []

        for cell in run:
            # Convert the recursive structure of cells containing rightward
            # cells into a linear row
            cells = self._cells_to_row(cell, context)
            row = {"type": "row", "body": cells}

            # If all the cells are heading cells, and there hasn't been a body
            # row yet, put this row in the thead
            if all(c.get("role") == "th" for c in cells) and not tbody:
                thead.append(row)
            else:
                tbody.append(row)

        return {"type": "table", "thead": thead, "body": tbody}

    def _cells_to_row(self, cell, context):
        body = cell.get("body")
        left = cell
        if body:
            del left["body"]
            if len(body) == 1 and body[0].get("type") == "cell":
                return [left] + self._cells_to_row(body[0], context)
            else:
                for subblock in body:
                    self.apply(subblock, context)
                return [left, {"type": "cell", "role": "td", "body": body}]
        else:
            return [left]


class RenumberHeadings(Processor):
    """
    Adds "level" keys to headings indicating their level in the heading
    hierarchy.
    """

    name = "renumberheadings"
    after = ("sortheadings", "includes")

    def apply(self, block, context, level=2):
        body = block.get("body", ())
        for subblock in body:
            if subblock.get("type") == "h":
                subblock["level"] = level
                self.apply(subblock, context, level + 1)
            else:
                self.apply(subblock, context, level)


class LinkProcessor(Processor):
    """
    Base class for processors of links.
    """

    def _apply_to_subtopics(self, block, context):
        if "parents" in block:
            for parent in block["parents"]:
                parentpath = parent["path"]
                psubs = parent.get("subtopics")
                if psubs:
                    self.apply(psubs, context, parentpath)

    def apply(self, block, context, basepath=None):
        if block.get("type") == "root":
            self._apply_to_subtopics(block, context)

        basepath = basepath or paths.basepath(context.get("path"))
        if "text" in block:
            self.text(context, block["text"], basepath)

        # Recurse
        for subblock in block.get("body", ()):
            self.apply(subblock, context, basepath)

    def text(self, context, text, basepath):
        for span in text:
            if isinstance(span, dict) and span.get("type") == "link":
                self.link(context, span, basepath)

    def link(self, context, span, basepath):
        return


class FullPaths(LinkProcessor):
    """
    Finds links in the content, and annotates them with the absolute path to the
    linked page.
    """

    name = "fullpaths"

    def link(self, context, span, basepath):
        pages = context.pages

        # Don't bother if this object has already operated on this link
        # (for example, if it was included)
        if "fullpath" in span:
            return

        path = span.get("value")
        if not path or ":" in path:
            span["exists"] = True
            return

        fullpath = pages.full_path(basepath, path)
        span["fullpath"] = fullpath

        pagepath, fragment = paths.split_fragment(fullpath)
        if fragment:
            span["fragment"] = fragment


# class Templates(Modifier):
#     name = "templates"
#
#     def modify(self, block, context):
#         if block.get("type") == "template" and block.get("role") == "item":
#             path = functions.string(block.get("text"))


# Text processors

class TextModifier(Modifier):
    """
    Special subclass of Modifier that only modifies text nodes.
    """

    def modify(self, block, context):
        text = block.get("text")
        if text:
            block["text"] = self.text(text, context)

    def text(self, text, context):
        raise NotImplementedError


class JoinText(TextModifier):
    """
    Joins adjacent runs of text together, so `["foo", "bar"]` becomes
    `["foobar"]`.
    """

    name = "join"

    def text(self, text, context):
        return join_text(text)


class Shortcuts(TextModifier):
    """
    Finds shortcuts and looks for a method corresponding to the shortcut's
    scheme to process it. You must subclass this to get it to do anything.
    """

    name = "shortcuts"

    def text(self, text, context):
        for i, span in enumerate(text):
            if isinstance(span, dict) and span.get("type") == "link":
                scheme = span.get("scheme", "link")
                methodname = "_xform_%s" % scheme.lower()
                if hasattr(self, methodname):
                    text[i] = getattr(self, methodname)(span)
        return text


# Post processors

class AnnotateLinks(LinkProcessor):
    """
    Finds links in the content, looks up the linked document in the search
    index, and adds annotations to the link based on the linked document's
    search fields.
    """

    name = "annotate"
    default_attrs = "title type icon summary container".split()

    def __init__(self, attrs=None):
        self.attrs = self.default_attrs
        if attrs:
            if isinstance(attrs, string_type):
                attrs = attrs.split()
            self.add_attrs(*attrs)

    def add_attrs(self, *attrs):
        self.attrs.extend(attrs)

    def link(self, context, span, basepath):
        pages = context.pages
        searcher = context.searcher

        # Don't bother if this object has already operated on this link
        # (for example, if it was included).
        # Only operate on links to other wiki pages.
        if "fields" in span or "fullpath" not in span:
            return

        fullpath = span["fullpath"]
        pagepath, fragment = paths.split_fragment(fullpath)
        spath = pages.source_path(pagepath)
        exists = span["exists"] = pages.exists(spath)

        # Look up the linked page in the index and copy its stored
        # fields onto the link
        if searcher and exists:
            stored = searcher.document(path=fullpath)
            if stored is not None:
                spanfields = span["fields"] = {}
                # Copy the stored fields onto the span
                for attrname in self.attrs:
                    if attrname in stored:
                        spanfields[attrname] = stored[attrname]

                title = stored.get("title")
                if not span.get("text") and title:
                    span["text"] = [title]


class RunSearches(Processor):
    """
    Finds various items that run searches and replaces them with the search
    results.
    """

    name = "searches"
    default_fields = "path title summary type icon status tags".split()

    def __init__(self, itemtypes="list"):
        if isinstance(itemtypes, string_type):
            itemtypes = itemtypes.split()
        self.itemtypes = frozenset(itemtypes)

    @staticmethod
    def _hit_to_dict(hit, fieldnames):
        return dict((fn, hit.get(fn)) for fn in fieldnames if fn in hit)

    @staticmethod
    def _read_labels(pages, basepath, labelspath, labels):
        labelspath = paths.join(basepath, labelspath)
        labelspath, section = paths.split_fragment(labelspath)
        section = section[1:] if section else "Labels"

        if pages.exists(labelspath):
            content = pages.content(labelspath, encoding=None)
            bio = BytesIO(content)
            parser = configparser.SafeConfigParser()
            parser.readfp(bio)
            if parser.has_section(section):
                labels.update(dict(parser.items(section)))

    @staticmethod
    def get_results(block, context):
        attrs = block.get("attrs", {})
        searcher = context.searcher
        if searcher is None:
            return

        q = searcher.query()
        if "query" not in attrs:
            block["error"] = "No query property"
            return
        q.set(attrs["query"])

        if "limit" in attrs:
            limstring = attrs["limit"]
            try:
                limit = int(limstring)
            except ValueError:
                limit = None
            q.set_limit(limit)

        if "sortedby" in attrs:
            fieldnames = attrs["sortedby"].split()
            for fieldname in fieldnames:
                rev = False
                if fieldname.startswith("-"):
                    fieldname = fieldname[1:]
                    rev = True
                q.add_sort_field(fieldname, rev)

        if "groupedby" in attrs:
            groupfield = attrs["groupedby"].strip()
            overlap = attrs.get("overlap", "").lower() == "true"
            q.set_group_field(groupfield, overlap)

        return q.search()

    @classmethod
    def _run_search(cls, context, basepath, block, icache):
        pages = context.pages
        searcher = context.searcher
        if searcher is None:
            return

        path = context["path"]
        attrs = block.get("attrs", {})
        if not attrs:
            return

        r = cls.get_results(block, context)
        if r and not r.is_empty():
            if "groupedby" in attrs:
                labels = block["labels"] = {}
                if "labels" in attrs:
                    cls._read_labels(pages, path, attrs["labels"], labels)

                groups = block["groups"] = {}
                for key, docnums in iteritems(r.groups()):
                    if not key:
                        key = u"_"
                    groups[key] = searcher.group_hits(docnums)
            else:
                hits = []
                for hit in r:
                    d = hit.fields()
                    path = d["path"]
                    if path == basepath:
                        d["is_here"] = True

                    # if include_content:
                    #     spath = pages.source_path(path)
                    #     json = pages.json(spath, postprocess=False)
                    #     if json:
                    #         d["body"] = json.get("body")

                    hits.append(d)
                block["hits"] = hits

    def apply(self, block, context, root=None):
        searcher = context.searcher
        if not searcher:
            return
        basepath = paths.basepath(context.get("path"))
        root = root or block

        for parent in block.get("parents", ()):
            psubs = parent.get("subtopics")
            if psubs:
                self.apply(psubs, context, root)

        if block.get("type") in self.itemtypes:
            icache = {}
            self._run_search(context, basepath, block, icache)
        else:
            for subblock in block.get("body", ()):
                self.apply(subblock, context, root)


class Parents(Processor):
    """
    Annotates the current document with information about its parent documents,
    including their subtopics, allowing the template to display things like
    breadcrumbs and a tree view.
    """

    name = "parents"

    @staticmethod
    def _find_ancestor(pages, dirpath):
        # Look for an _index file in the given directory, and if not found,
        # recursively look in parent directories

        spath = None
        while True:
            spath = pages.source_path(dirpath)
            if pages.exists(spath):
                return spath
            elif dirpath != "/":
                dirpath = paths.parent(dirpath)
                continue
            break

        return spath

    @staticmethod
    def _get_parent_path(pages, path, block):
        # Find the path to the parent document

        attrs = block.get("attrs", {})
        if "parent" in attrs:
            # If the author specified a parent, use that
            parent = attrs.get("parent")
            parentpath = pages.source_path(paths.join(path, parent))

        elif pages.is_index_page(path):
            # If this is an index page, assume its parent is the _index page of
            # the parent directory
            parentpath = Parents._find_ancestor(pages, paths.parent(path))

        else:
            # Assume the parent is the _index page for this directory
            parentpath = Parents._find_ancestor(pages, paths.directory(path))

        return parentpath

    @staticmethod
    def _parent_info(json, path):
        # Find the subtopics section
        subtopics = functions.subblock_by_id(json, "subtopics")
        if subtopics:
            stbody = subtopics.get("body")
            if stbody:
                # Remove
                body = functions.collapse(stbody, ("col_group", "col"))
                subtopics["body"] = body

        return {
            "path": path,
            "basepath": paths.basepath(path),
            "title": json.get("title", ()),
            "summary": json.get("summary", ()),
            "attrs": json.get("attrs", {}),
            "subtopics": subtopics,
        }

    def apply(self, block, context):
        # Only run on the root block
        if block.get("type") != "root":
            return
        root = block

        # Get needed objects and options from the context
        pages = context.pages
        searcher = context.searcher
        path = context["path"]
        conditional = context["conditional"]
        save_to_cache = context["save_to_cache"]

        # Remember parent paths to avoid circular loops
        seen = set()
        # A list of dictionaries containing ancestor doc info
        parents = []

        # Recursively load parent documents
        current_block = block
        current_path = path
        while True:
            # Compute the parent of this document
            ppath = self._get_parent_path(pages, current_path, current_block)
            if ppath == path or ppath in seen:
                break
            seen.add(ppath)

            if not pages.exists(path):
                break

            # Load the parent document
            json = pages.json(ppath, conditional=conditional,
                              postprocess=False, save_to_cache=save_to_cache,
                              searcher=searcher)
            parents.append(self._parent_info(json, ppath))

            # Loop
            current_path = ppath
            current_block = json

        if parents:
            # Reverse the list so it's in descending order
            parents.reverse()
        else:
            info = self._parent_info(copy.deepcopy(block), path)
            parents = [info]

        # Attach the parent JSON and list of parents to the root
        root["parents"] = parents


class Toc(Processor):
    name = "toc"
    before = ("annotate",)

    @staticmethod
    def _apply(context, item, basepath, depth, maxdepth):
        pages = context.pages

        # Find the first link in the item and use its path
        text = item.get("text")
        link = functions.first_span_of_type(text, "link")
        if not link:
            return
        ref = link.get("value")
        if not ref or ":" in ref:
            return

        fullpath = pages.full_path(basepath, ref)
        if not pages.exists(fullpath):
            return

        # Load the referenced page
        json = pages.json(fullpath, context)
        # Find the subtopics section
        subtopics = functions.subblock_by_id(json, "subtopics")
        if not subtopics:
            return

        # Copy the subtopics onto this topic's body
        if "body" in subtopics:
            body = copy.deepcopy(subtopics["body"])
            # Collapse certain block types
            body = functions.collapse(body, ("col_group", "col"))
            item["body"] = body

        if depth < maxdepth:
            # Recurse on the loaded subtopics
            topics = functions.find_items(subtopics, "subtopics_item")
            for subitem in topics:
                Toc._apply(context, subitem, fullpath, depth + 1, maxdepth)

    def apply(self, block, context):
        basepath = paths.basepath(context.get("path"))

        # Find the subtopics section
        subtopics = functions.subblock_by_id(block, "subtopics")
        if not subtopics:
            return

        attrs = subtopics.get("attrs", {})
        maxdepth = int(attrs.get("maxdepth", "0"))
        if not maxdepth:
            return

        topics = functions.find_items(subtopics, "subtopics_item")
        for item in topics:
            self._apply(context, item, basepath, 1, maxdepth)


# Defaults

default_preprocessor_classes = (
    JoinText,
    Title,
    Hierarchy,
    Properties,
    Promote,
    SortHeadings,
    Sections,
    Includes,
    EmptyBlocks,
    RenumberHeadings,
    Groups,
    Tables,
    FullPaths,
)

default_postprocessor_classes = (
    Parents,
    RunSearches,
    # Toc,
    AnnotateLinks,
)


# Dependency graph

class CircularDependencyError(Exception):
    pass


class DependencyGraph(object):
    def __init__(self, vs=None):
        self._vs = vs or []
        self._vset = set(self._vs)
        self._prereqs = defaultdict(set)
        self._resolved = set()
        self._unresolved = set()

    def add(self, v):
        if v not in self._vset:
            self._vset.add(v)
            self._vs.append(v)

    def depends_on(self, v, prereq):
        if v not in self._vset:
            self.add(v)
        if prereq not in self._vset:
            self.add(prereq)
        self._prereqs[v].add(prereq)

    def resolve(self, vs=None):
        vs = vs or self._vs
        for v in vs:
            if v in self._resolved:
                continue
            if v in self._unresolved:
                raise CircularDependencyError

            self._unresolved.add(v)
            if v in self._prereqs:
                prevs = list(self._prereqs[v])
                prevs.sort(key=lambda x: self._vs.index(x))
                for prev in self.resolve(prevs):
                    yield prev

            self._unresolved.remove(v)
            self._resolved.add(v)
            yield v


def make_pipeline(objs):
    # Add the object names to the DG, retaining their incoming order
    dg = DependencyGraph([obj.name for obj in objs])
    # Create a dict to look up objects by their names
    byname = dict((obj.name, obj) for obj in objs)

    # For each object, look at its before and after attributes and add them
    # to the DG
    for obj in objs:
        for aftname in getattr(obj, "after", ()):
            dg.depends_on(obj.name, aftname)
        for befname in getattr(obj, "before", ()):
            dg.depends_on(befname, obj.name)

    # Resolve the dependencies
    resolved_names = dg.resolve()
    # Create a pipe from the objects in resolved order
    return Pipe([byname[name] for name in resolved_names])


def default_pre_pipeline():
    objs = [cls() for cls in default_preprocessor_classes]
    return make_pipeline(objs)


def default_post_pipeline():
    objs = [cls() for cls in default_postprocessor_classes]
    return make_pipeline(objs)
