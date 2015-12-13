# Copyright 2014 Matt Chaput. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
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

import re
import textwrap

from bookish import compat, util
from bookish.avenue import avenue
from bookish.compat import BytesIO, StringIO, string_type, unichr, text_type


default_charmap = (
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
    (unichr(9656), ">"),

    (unichr(188), "1/4"),
    (unichr(189), "1/2"),
    (unichr(190), "3/4"),

    (unichr(8230), "..."),
    (unichr(215), "x"),
    (unichr(169), "(c)"),
    (unichr(8482), "(tm)"),
    (unichr(174), "(r)"),
    (unichr(730), "deg"),
    (unichr(960), "pi"),
    (unichr(963), "sigma"),
)


def dechar(text, charmap=default_charmap):
    for char, replacement in charmap:
        text = text.replace(char, replacement)
    return text


def addindent(first, subsequent, text, trim=False):
    lines = text.split("\n")
    if trim and not lines[0]:
        lines.pop(0)
    if trim and not lines[-1]:
        lines.pop()

    buf = ""
    for i, line in enumerate(lines):
        if i == 0:
            buf += first
        else:
            buf += subsequent

        buf += line + "\n"

    return buf


normalize_exp = re.compile("[\t\r\n ]+")
lstrip_exp = re.compile("(^[ \t]*\n)+")


def format_block(text, left=0, width=72, wrap=True, first="", rest="",
                 upper=False, lower=False, xform=None, charfilter=True,
                 charmap=None, normalize=True):
    if upper:
        text = text.upper()
    elif lower:
        text = text.lower()
    if xform:
        text = xform(text)
    if charfilter:
        charmap = charmap or default_charmap
        text = dechar(text, charmap)

    t = u""
    if text.strip():
        first_indent = u" " * (left - len(first)) + first
        rest_indent = u" " * (left - len(rest)) + rest
        if wrap:
            if normalize:
                text = normalize_exp.sub(u" ", text)
            else:
                text = text.replace(u"\n", u" ")
            text = text.expandtabs(8).strip()
            wrapper = textwrap.TextWrapper()
            wrapper.width = width
            wrapper.initial_indent = first_indent
            wrapper.subsequent_indent = rest_indent
            t += wrapper.fill(text)

            if not t.strip(" ").endswith(u"\n"):
                t += u"\n"
        else:
            t += addindent(first_indent, rest_indent, text)

    return t


def join(arg, *args):
    if isinstance(arg, string_type):
        out = [arg]
    elif isinstance(arg, tuple):
        out = list(arg)
    elif isinstance(arg, list):
        out = arg
    else:
        raise TypeError(arg)

    for arg in args:
        if isinstance(arg, string_type):
            out.append(arg)
        elif isinstance(arg, (list, tuple)):
            out.extend(arg)
        else:
            raise TypeError(arg)

    return "".join(out)


class TextFrame(object):
    display_vars = "left top bottom width replacements buffered vars".split()

    def __init__(self, parent, left=0, top=0, bottom=0, width=72,
                 padding_top=0, padding_bottom=0, replacements=None,
                 buffered=False, vars=None, charfilter=None, charmap=None,
                 xform=None):
        self.parent = parent
        self.left = left
        self.top = top
        self.bottom = bottom
        self.width = width
        self.padding_top = padding_top
        self.padding_bottom = padding_bottom
        self.replacements = replacements
        # Supplying replacements implies buffering the output
        self.buffered = buffered or bool(replacements)
        self.vars = vars
        self.charmap = charmap
        self.xform = xform

        if charfilter is None:
            if self.parent:
                charfilter = self.parent.charfilter
            else:
                charfilter = True
        self.charfilter = charfilter

        if self.buffered:
            self.buffer = StringIO()
        else:
            self.buffer = None

    def __repr__(self):
        t = "%s(" % type(self).__name__
        for i, n in enumerate(self.display_vars):
            if i > 0:
                t += " "
            t += "%s=%r" % (n, self.__dict__[n])
        return t

    def emit(self, string, indent=0, wrap=True, first="", rest="", upper=False,
             lower=False, normalize=True):
        left = self.left + indent
        string = format_block(string, left, width=self.width, wrap=wrap,
                              first=first, rest=rest, upper=upper, lower=lower,
                              xform=self.xform, charfilter=self.charfilter,
                              charmap=self.charmap, normalize=normalize)
        assert isinstance(string, text_type)
        self.write(string)

    def get(self, name):
        if self.vars and name in self.vars:
            return self.vars.get(name)
        elif self.parent:
            return self.parent.get(name)
        else:
            return None

    def inc(self, name):
        if self.vars and name in self.vars:
            v = self.vars[name]
            self.vars[name] += 1
            return v
        elif self.parent:
            return self.parent.inc(name)
        else:
            raise KeyError

    def write(self, string):
        # String must be Unicode
        assert isinstance(string, text_type), repr(string)
        if self.buffered:
            self.buffer.write(string)
        else:
            self.parent.write(string)

    def getvalue(self):
        assert self.buffered
        output = self.buffer.getvalue()
        if self.replacements:
            for target, replacement in self.replacements:
                output = output.replace(target, replacement)
        return output

    def finish(self):
        if self.buffered:
            output = self.getvalue()
            assert isinstance(output, text_type)
            self.parent.write(output)


class TextifierBase(object):
    def __init__(self, root, left=0, top=0, bottom=0, width=72, vars=None,
                 charfilter=True):
        self.root = root
        self.frames = [TextFrame(None, left=left, top=top, bottom=bottom,
                                 width=width, buffered=True, vars=vars,
                                 charfilter=charfilter)]
        self.gap = 0
        self.aves = avenue.AvenueManager()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pop()

    def transform(self):
        self.render(self.root)
        assert len(self.frames) == 1
        # if self.gap:
        #     self.blank_lines(self.gap)
        return self.frame.getvalue()

    @property
    def frame(self):
        return self.frames[-1]

    def push(self, indent=0, left=None, top=0, bottom=0, width=None,
             padding_top=0, padding_bottom=0, replacements=None,
             buffered=False, charfilter=None, charmap=None, xform=None,
             **kwargs):

        left = left if left is not None else self.frame.left
        left += indent
        width = width if width is not None else self.frame.width

        f = TextFrame(self.frame, left=left, top=top, bottom=bottom,
                      width=width, padding_top=padding_top,
                      padding_bottom=padding_bottom, replacements=replacements,
                      buffered=buffered, vars=kwargs, charfilter=charfilter,
                      charmap=charmap, xform=xform)
        self.frames.append(f)
        self.gap = max(self.gap, self.frame.top)
        return self

    def pop(self):
        assert len(self.frames) > 1
        last = self.frames.pop()
        last.finish()
        self.gap = max(self.gap, last.bottom)

    def find(self, block, ave, **vars):
        return self.aves.find(ave, self.root, block, **vars)

    def write(self, string):
        self.frame.write(string)

    def blank_lines(self, n):
        if n:
            self.write(u"\n" * n)

    def render_body(self, body, **kwargs):
        if isinstance(body, dict):
            body = body.get("body", ())

        if kwargs:
            self.push(**kwargs)
        for subblock in body:
            self.render(subblock)
        if kwargs:
            self.pop()

    def render_super(self, block):
        return self.render(block, ns=super(TextifierBase, self))

    def render(self, block, ns=None):
        if isinstance(block, list):
            return self.render_body(block)

        ns = ns or self
        # Look for a method corresponding to the block's type
        btype = block.get("type")
        if btype:
            typename = "%s_block" % btype
            if hasattr(ns, typename):
                return getattr(ns, typename)(block)

        # Look for a method corresponding to the block's role
        brole = block.get("role")
        if brole:
            rolename = "%s_block" % brole
            if hasattr(ns, rolename):
                return getattr(ns, rolename)(block)

        # Default behavior
        self.emit_block_text(block)
        for subblock in block.get("body", ()):
            self.render(subblock)

    def render_text(self, text):
        if isinstance(text, dict):
            text = text.get("text", ())
        return u"".join(self.render_span(span) for span in text)

    def render_span(self, span):
        if isinstance(span, string_type):
            return span
        
        stype = span.get("type")
        if stype:
            typename = "%s_span" % stype
            if hasattr(self, typename):
                return getattr(self, typename)(span)

        text = span.get("text")
        if text:
            return self.render_text(text)
        else:
            return u""

    def emit(self, text, indent=0, wrap=True, top=0, bottom=0, first=u"",
             rest=u"", upper=False, lower=False):
        self.blank_lines(max(self.gap, top))
        self.frame.emit(text, indent=indent, wrap=wrap, first=first, rest=rest,
                        upper=upper, lower=lower)
        self.gap = bottom

    def emit_block_text(self, block, **kwargs):
        text = self.render_text(block.get("text", u""))
        self.emit(text, **kwargs)

    # def render_columns(self, node, width, indent=0, map=None):
    #     tabs = [int(t) for t in node.get("tabs", "").split(" ")]
    #     blocks = node.findall("block")
    #     if len(tabs) != len(blocks):
    #         raise Exception("columns element has %s sub-blocks "
    #                         " but only %s tab stops"
    #                         % (len(blocks), len(tabs)))
    #     tabs.append(width)
    #
    #     texts = [self.render(block, indent=tabs[i], width=tabs[i+1]-tabs[i])
    #              for i, block in blocks]
    #
    #     linelists = [text.split("\n") for text in texts]
    #     maxlines = max(len(linelist) for linelist in linelists)
    #     buffer = [""] * maxlines
    #     for i, linelist in enumerate(linelists):
    #         left = tabs[i]
    #         right = tabs[i+1]
    #         width = right - left
    #         for lineno, line in enumerate(linelist):
    #             fragment = line[left:right]
    #             diff = width - len(fragment)
    #             if diff and i < len(texts)-1:
    #                 fragment += " " * diff
    #             buffer[lineno] += fragment
    #     return "\n".join(buffer)


class BookishTextifier(TextifierBase):
    def para_block(self, block):
        self.emit_block_text(block, top=1, bottom=1)

    def ord_group_block(self, block):
        self.render_body(block, indent=4)

    def bullet_block(self, block):
        self.emit_block_text(block, top=1, bottom=1, first=u" *  ", rest=u"    ")
        self.render_body(block, indent=4)

    def ord_group_block(self, block):
        self.render_body(block, ord_counter=1, indent=4)

    def ord_block(self, block):
        count = self.frame.inc("ord_counter")
        self.emit_block_text(block, top=1, bottom=1, first=u"%2d. " % count,
                             rest="    ")
        self.render_body(block, indent=4)

    def section_block(self, block):
        text = self.render_text(block.get("text") or block.get("id"))
        self.emit(text, top=1, upper=True)
        self.render_body(block, top=1, bottom=1, indent=4)

    def h_block(self, block):
        self.emit_block_text(block, top=1, bottom=1, upper=True)
        self.render_body(block, bottom=1, indent=4)

    def note_block(self, block):
        self.emit(u"Note", upper=True, top=1)
        self.render_body(block, indent=4)

    def tip_block(self, block):
        self.emit(u"Tip", upper=True, top=1)
        self.render_body(block, indent=4)

    def warning_block(self, block):
        self.emit(u"Warning", upper=True, top=1)
        self.render_body(block, indent=4)

    def dt_block(self, block):
        self.emit_block_text(block, top=1)
        self.render_body(block, indent=4)

    def item_block(self, block):
        self.emit_block_text(block, top=1)
        self.render_body(block, indent=4)

    def list_block(self, block):
        pass

    def subtopics_block(self, block):
        pass

    def pre_block(self, block):
        text = self.render_text(block.get("text", u""))
        text = lstrip_exp.sub(u"", text).rstrip()
        text = textwrap.dedent(text)
        self.emit(text, wrap=False, top=0, bottom=0, first=u"> ", rest=u"> ")

    def var_span(self, span):
        return u"<" + self.render_text(span) + u">"

    def strong_span(self, span):
        return u"*" + self.render_text(span) + u"*"

    def em_span(self, span):
        return u"_" + self.render_text(span) + u"_"

    # def code_span(self, span):
    #     return "`" + self.render_text(span) + "`"

    def keys_span(self, span):
        keylist = span.get("keys")
        if keylist:
            out = ["["]
            for i, keyname in enumerate(keylist):
                if i > 0:
                    out.append(" + ")
                out.append(keyname)
            out.append("]")
            return u"".join(out)
        else:
            return u""
