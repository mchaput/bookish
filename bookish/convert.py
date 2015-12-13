# Copyright 2014 Matt Chaput. All rights reserved.
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
import re
import textwrap

try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

from bookish.compat import StringIO
from bookish.compat import string_type
from bookish.compat import unichr


_charmap = [
    (unichr(8221), '"'),
    (unichr(8220), '"'),

    (unichr(8217), "'"),
    (unichr(8212), "---"),
    (unichr(8211), "--"),

    (unichr(8592), "<-"),
    (unichr(8594), "->"),
    (unichr(8804), "<="),
    (unichr(8805), ">="),
    (unichr(8660), "<=>"),

    (unichr(188), "1/4"),
    (unichr(189), "1/2"),
    (unichr(190), "3/4"),

    (unichr(8230), "..."),
    (unichr(215), "x"),
    (unichr(169), "(c)"),
    (unichr(8482), "(tm)"),
    (unichr(174), "(r)"),
    # (unichr(730), "deg"),
]


def dechar(text, charmap=_charmap):
    for char, replacement in charmap:
        text = text.replace(char, replacement)
    return text


class WikiWriter(object):
    def __init__(self, stream):
        self.stream = stream

    def process_text(self, run):
        return run

    def text(self, run):
        self.stream.write(self.process_text(run))

    def markup(self, run):
        self.stream.write(run)

    def indent(self, spaces):
        self.markup(" " * spaces)

    def span(self, obj):
        if isinstance(obj, list):
            for sub in obj:
                self.span(sub)
        elif isinstance(obj, dict):
            t = obj.get("type")
            methodname = "do_%s_span" % t
            method = getattr(self, methodname, self.default_span)
            method(obj)
        elif isinstance(obj, string_type):
            self.text(obj)
        else:
            raise Exception(obj)

    def block(self, obj, indent=0):
        if isinstance(obj, list):
            for sub in obj:
                self.block(sub)
        elif isinstance(obj, dict):
            t = obj.get("type")
            methodname = "do_%s_block" % t
            method = getattr(self, methodname, self.default_block)
            method(obj, indent=indent)
        else:
            raise Exception(obj)

    def default_span(self, obj):
        for span in obj.get("text", []):
            self.span(span)

    def default_block(self, obj, indent=0):
        text = obj.get("text", [])
        if text:
            self.indent(indent)
            self.span(text)
            self.markup("\n")
        self._do_body(obj, indent + 4)

    #

    def do_quote_span(self, obj):
        self.markup('"')
        for x in obj.get("text", []):
            self.span(x)
        self.markup('"')

    def do_comment_span(self, obj):
        self.markup("<!--" + obj.get("content", "") + "-->")

    def _do_span(self, pre, obj, post):
        self.markup(pre)
        self.span(obj.get("text", []))
        self.markup(post)

    def do_var_span(self, obj):
        self._do_span("<<", obj, ">>")

    def do_ui_span(self, obj):
        self._do_span("__", obj, "__")

    def do_strong_span(self, obj):
        self._do_span("*", obj, "*")

    def do_em_span(self, obj):
        self._do_span("_", obj, "_")

    def do_code_span(self, obj):
        self._do_span("`", obj, "`")

    def do_xml_span(self, obj):
        tag = obj["tag"]
        self.markup("<" + tag)
        attrs = obj.get("attrs")
        if attrs:
            for k, v in attrs:
                self.markup(" %s=%r" % (k, v))
        self.markup(">")
        self.span(obj.get("text", []))
        self.markup("</%s>" % tag )

    def do_keys_span(self, obj):
        self.markup("((")
        for i, keyname in enumerate(obj.get("keys", [])):
            if i > 0:
                self.markup(" + ")
            self.markup(keyname)
        self.markup("))")

    def do_link_span(self, obj):
        self.markup("[")
        text = obj.get("text", [])
        if text:
            self.span(text)
            self.markup("|")
        scheme = obj.get("scheme", None)
        if scheme:
            self.text(scheme)
            self.markup(":")
        self.markup(obj.get("value", ""))
        self.markup("]")

    #

    def _do_body(self, obj, indent):
        for block in obj.get("body", []):
            self.block(block, indent)

    def _do_block(self, pre, obj, post, indent, delta=4):
        self.indent(indent)
        self.markup(pre)
        self.span(obj.get("text", []))
        self.markup(post + "\n")
        self._do_body(obj, indent + delta)

    def do_para_block(self, obj, indent):
        self._do_block("", obj, "", indent)

    def do_dt_block(self, obj, indent):
        self._do_block("", obj, ":", indent)

    def do_hcell_block(self, obj, indent):
        self._do_block("", obj, "||", indent)

    def do_cell_block(self, obj, indent):
        self._do_block("", obj, "|", indent)

    def do_bullet_block(self, obj, indent):
        self._do_block("* ", obj, "", indent)

    def do_ord_block(self, obj, indent):
        self._do_block("# ", obj, "", indent)

    def do_code_block(self, obj, indent):
        lang = obj.get("lang")
        self.indent(indent)
        self.markup("{{{\n")
        if lang:
            self.markup("#!%s\n" % lang)
        self.span(obj.get("text", []))
        self.indent(indent)
        self.markup("}}}\n")

    def do_h_block(self, obj, indent):
        level = obj.get("level", 1)
        idtag = obj.get("id")
        text = obj.get("text", [])
        self.indent(indent)
        if level:
            eqs = "=" * level
            self.markup(eqs + " ")
            self.span(text)
            self.markup(" " + eqs)
            if idtag:
                self.markup(" (%s)" % idtag)
        else:
            self.markup("@" + idtag)
            if text:
                self.markup(" ")
                self.span(text)
        self.markup("\n")
        self._do_body(obj, indent)

    def do_summary_block(self, obj, indent):
        self.indent(indent)
        self.markup('"""')
        self.span(obj.get("text", []))
        self.markup('"""\n')

    def do_item_block(self, obj, indent):
        it = obj.get("itemtype", "")
        self._do_block(":%s:" % it, obj, ":", indent)

    def do_prop_block(self, obj, indent):
        self.indent(indent)
        self.markup("#%s: " % obj["name"])
        self.span(obj.get("text", []))
        self.markup("\n")

    def do_pxml_block(self, obj, indent):
        self.indent(indent)
        self.markup(obj["tag"])
        attrs = obj.get("attrs")
        if attrs:
            for k, v in attrs:
                self.markup(" %s=%r" % (k, v))
        self.markup(">>")
        self.span(obj.get("text", []))
        self.markup("\n")
        self._do_body(obj, indent)


class ReWiki(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tagstack = []

    def handle_starttag(self, tag, attrs):
        print("  " * len(self.tagstack), tag, attrs)
        self.tagstack.append((tag, attrs))

    def handle_endtag(self, tag):
        self.tagstack.pop()

    def handle_data(self, data):
        if data.strip():
            print("  " * (len(self.tagstack) + 1), repr(data))

    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        print("  " * (len(self.tagstack) + 1), "ENT", name)

    def handle_charref(self, name):
        if name.startswith('x'):
            num = int(name[1:], 16)
        else:
            num = int(name)
        print("  " * (len(self.tagstack) + 1), "CHR", num)

    def handle_decl(self, data):
        print("  " * (len(self.tagstack)), "DEC", data)


if __name__ == "__main__":
    import sys

    ww = WikiWriter(sys.stdout)
    ww.block([
        {"type": "para", "text": ["Hello there!"]},
        {"type": "para", "text": ["What up?"]},
        {"type": "bullet", "text": ["Item 1."], "body": [
            {"type": "prop", "name": "id", "text": ["foobar"]},
        ]},
        {"type": "bullet", "text": ["Item 2."]},
        {"type": "para", "text": "The end."},
    ])

#     p = ReWiki()
#     p.feed("""
# <!DOCTYPE html>
# <html>
#     <head><title>Hello</head>
#     <link rel="stylesheet" href="&quot;style&quot;.css" >
#     <body>
#         <p>This is a test
#         <p>of HTML parsing<br>
#         <p>Third para
#     </body>
# </html>
# """)


