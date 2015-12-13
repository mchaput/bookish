from bookish import textify, functions
from bookish.avenue import patterns as pt


# var_finder = parse('body.0.text..@type="var"')
var_finder = pt.Ancestor(
    pt.Sequence([
        pt.Lookup("body"),
        pt.Lookup(0),
        pt.Lookup("text"),
    ]),
    pt.Comparison("type", "==", "var")
)


repl_quotes = [(u'"', u'\\"')]


class HoudiniTextifier(textify.BookishTextifier):
    def root_block(self, block):
        attrs = block.get("attrs", {})
        self.pagetype = pagetype = attrs.get("type")
        body = block.get("body", ())

        if pagetype == "hscript":
            # Command help has the title at column 0 and all other text
            # indented. We'll indent everything here, and then outdent the
            # title
            with self.push(indent=4):
                self.render(body)

        elif pagetype == "expression" or pagetype == "vex":
            self.emit(u"{")
            self.render_body(body)
            self.emit(u"}")

        elif pagetype == "hompackage":
            self.emit(u'%define MODULE_DOCSTRING /**/ "', top=1)
            with self.push(replacements=repl_quotes):
                self.render(body)
            self.emit(u'" %enddef', bottom=1)

        elif pagetype in (u"homclass", u"homfunction", u"hommodule"):
            cppname = attrs["cppname"]
            self.emit(u'%%feature("docstring") %s "' % cppname)
            nonsect = list(subb for subb in body
                           if subb.get("role") != "section")
            with self.push(replacements=repl_quotes):
                self.render(nonsect)
            self.emit(u'";')

            for subblock in body:
                sid = subblock.get("id")
                if sid in (u"methods", u"functions"):
                    itemtype = sid + "_item"
                    for itemblock in functions.find_items(subblock, itemtype):
                        self._homfn(itemblock)

        elif pagetype == u"hom_module":
            self.emit(u'%define MODULE_DOCSTRING /**/ "')
            with self.push(replacements=repl_quotes):
                self.render(body)
            self.emit(u'" %enddef')

        else:
            self.render(body)

    def title_block(self, block):
        if self.pagetype == "hscript":
            self.emit_block_text(block, indent=-4)
            self._replaced_by()
        elif self.pagetype == "expression":
            name = functions.string(block.get("text"))
            # Pull out the usage section
            usage = functions.subblock_by_id(self.root, "usage")
            if usage and "body" in usage and usage["body"]:
                firstb = usage["body"][0]
                varnames = [functions.string(span) for span
                            in functions.find_spans_of_type(firstb, "var")]
                self.emit(name + u" " + u" ".join(varnames))
            else:
                self.emit(name)
            self._replaced_by()
        else:
            self.render_super(block)
            self._replaces()

    def summary_block(self, block):
        self.emit_block_text(block, top=1, bottom=1)

    def _homfn(self, block):
        attrs = block.get("attrs", {})
        status = attrs.get("status")
        if status in (u"nd", u"ni"):
            return

        cppname = attrs["cppname"]
        self.emit(u'%%feature("docstring") %s "' % cppname)
        with self.push(replacements=repl_quotes):
            self.render(block.get("body", ()))
        self.emit(u'";')

    def _replaces(self):
        repls = self.root.get("attrs", {}).get("replaces")
        if repls:
            with self.push(bottom=1):
                self.emit(u"Replaces", top=1, upper=True)
                with self.push(indent=4):
                    for repl in repls:
                        self.emit(repl["title"], first="- ",
                                  rest="  ")

    def _replaced_by(self):
        repls = self.root.get("replacedby")
        if repls:
            with self.push(bottom=1):
                self.emit(u"Replaced by", top=1, upper=True)
                with self.push(indent=4):
                    for repl in repls:
                        self.emit(repl["title"], first="- ",
                                  rest="  ")


class HoudiniFormattedTextifier(HoudiniTextifier):
    def var_span(self, span):
        return u"<i>" + self.render_text(span) + u"</i>"

    def strong_span(self, span):
        return u"<b>" + self.render_text(span) + u"</b>"

    def em_span(self, span):
        return u"<i>" + self.render_text(span) + u"</i>"

    def code_span(self, span):
        return u"<tt>" + self.render_text(span) + u"</tt>"
