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

from textwrap import dedent

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.formatters.html import escape_html
from pygments.util import ClassNotFound

from bookish import functions, util


class CustomHtmlFormatter(HtmlFormatter):
    def __init__(self, hl_lines=None):
        HtmlFormatter.__init__(self, hl_lines=hl_lines or [])

    def wrap(self, source, outfile):
        for x, line in source:
            yield x, "<span class='line'>" + line + "</span>"


def lexer_for(name):
    try:
        lexer = get_lexer_by_name(name)
    except ClassNotFound:
        lexer = None
    return lexer


def format_block(block, lexername=None, lexer=None, pre=False):
    attrs = block.get("attrs", {})
    source = functions.string(block.get("text", ""))
    look = attrs.get("display", "")
    lexername = lexername or block.get("lang")
    lexer = lexer or lexer_for(lexername)

    if "linenos" in attrs and attrs["linenos"] == "true":
        look += " linenos"

    if "hl_lines" in attrs:
        hl_lines = [int(n) for n
                    in attrs["hl_lines"].strip("[]").split(",")]
    else:
        hl_lines = None

    return format_string(source, lexername, lexer, look, hl_lines, pre)


def format_string(source, lexername=None, lexer=None, look="",
                  hl_lines=None, pre=False):
    source = dedent(source.strip("\r\n"))
    lexer = lexer or lexer_for(lexername)
    if lexer:
        hf = CustomHtmlFormatter(hl_lines=hl_lines)
        hi = highlight(source, lexer, hf)
    else:
        hi = escape_html(source)

    if pre:
        hi = "<pre class='pre codehilite %s'>%s</pre>" % (look, hi)

    return hi


# Command line colors

def code_chars(code):
    return "\033[%sm" % str(code)


class Ansi(object):
    black = code_chars(30)
    red = code_chars(31)
    green = code_chars(32)
    yellow = code_chars(33)
    blue = code_chars(34)
    magenta = code_chars(35)
    cyan = code_chars(36)
    white = code_chars(37)
    reset = code_chars(39)

    black_back = code_chars(40)
    red_back = code_chars(41)
    green_back = code_chars(42)
    yellow_back = code_chars(43)
    blue_back = code_chars(44)
    magenta_back = code_chars(45)
    cyan_back = code_chars(46)
    white_back = code_chars(47)
    reset_back = code_chars(49)

    bright = code_chars(1)
    dim = code_chars(2)
    normal = code_chars(22)
    reset_all = code_chars(0)


def cstring(code, string):
    return code + string + Ansi.reset_all

