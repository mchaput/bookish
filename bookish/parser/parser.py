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

from bookish import compat, util


def condition_string(c):
    c = c.replace("\r\n", "\n").replace("\r", "\n").replace("\t", " " * 8)
    c += u"\n\uffff"
    return c


def rules_from_locals(localvars, namelist):
    from bookish.parser.rules import Rule

    d = {}
    for name in namelist:
        obj = localvars[name]
        if isinstance(obj, Rule):
            obj.rulename = name
        d[name] = obj
    return d


def make_rule(name, expr, args, add=False):
    from bookish.parser.rules import Parms

    if args:
        expr = Parms(args, expr)
    expr.rulename = name
    return expr


class ParserError(Exception):
    pass


class ArgError(Exception):
    pass


def rules_from_module(mod):
    from bookish.parser import rules as r

    rules = {}
    for name in dir(mod):
        obj = getattr(mod, name)
        isruleclass = isinstance(obj, type) and issubclass(obj, r.Rule)
        if isinstance(obj, r.Rule) or isruleclass:
            rules[name] = obj
    return rules


# Marker objects

class Empty:
    def __repr__(self):
        return "<%s>" % (self.__class__.__name__, )

    def __bool__(self):
        return False

    def __nonzero__(self):
        return False

Empty = Empty()


class Miss(object):
    pass


class Failure(object):
    pass


# Lines cache

class Lines(object):
    def __init__(self, text):
        self.text = text
        self.lines = None

    def _study(self):
        if self.lines is None:
            text = self.text
            lines = []
            lstart = 0
            for i, c in enumerate(text):
                if c == "\n":
                    lines.append((lstart, i))
                    lstart = i + 1
            lines.append((lstart, len(text)))
            self.lines = lines

    def indices(self, pos):
        self._study()
        last = None
        for item in enumerate(self.lines):
            i, (lstart, lend) = item
            if pos < lstart:
                break
            last = item
        return last

    def line_and_col(self, pos):
        lineno, (startchar, endchar) = self.indices(pos)
        return lineno + 1, pos - startchar + 1


# Document object

class Document(str):
    def lines(self):
        if not hasattr(self, "_lines"):
            self._lines = Lines(self)
        return self._lines

    def line_and_col(self, i):
        return self.lines().line_and_col(i)


class ParserContext(util.Context):
    pass
    # def __init__(self, m=None):
    #     util.Context.__init__(self, m)
    #     self.tracing = False
    #
    # def __repr__(self):
    #     note = self.note or type(self).__name__
    #     return "%s(%r)" % (note, self.maps)
    #
    # # def push(self, m=None):
    # #     c = util.Context.push(self, m)
    # #     c.tracing = self.tracing
    # #     return c
    #
    # @staticmethod
    # def trace(level, pos, rule, msg=None):
    #     print(" ." * level, pos, type(rule).__name__, rule.rulename,
    #           rule.repr(), msg if msg else '')
    #
    # @staticmethod
    # def trace_msg(level, pos, rule, msg):
    #     print(" ." * level, pos, msg)
    #
    # @staticmethod
    # def trace_miss(level, pos, rule, msg=None):
    #     print(" ." * level, "MISS", msg if msg else '')
    #
    # @staticmethod
    # def trace_hit(level, pos, rule, out):
    #     print(" ." * level, "=>", pos, repr(out))


def make_ruledict(rulelist):
    return dict((rule.rulename, rule) for rule in rulelist)


def make_grammar(rulelist, rulename=None):
        ruledict = make_ruledict(rulelist)
        return Grammar(ruledict, rulename=rulename)


def parser_context():
    from bookish.parser import bootstrap

    ctx = bootstrap.bootstrap_context()

    def _make_grammar(rulelist, rulename=None):
        ruledict = make_ruledict(rulelist)
        g = Grammar(ruledict, context=ctx, rulename=rulename)
        return g
    ctx["make_grammar"] = _make_grammar

    return ctx


class BaseGrammar(object):
    def parse(self, string, **extra):
        raise NotImplementedError

    def parse_file(self, fileobj, encoding="utf8"):
        with fileobj:
            string = fileobj.read().decode(encoding)
        return self.parse(string)


class Grammar(BaseGrammar):
    def __init__(self, ruledict, context=None, rulename=None):
        context = context or parser_context()
        context = context.push(ruledict)

        self.ruledict = ruledict
        self.context = context
        self.rulename = rulename or "grammar"

    def parse(self, string, pos=0, **extra):
        c = self.context.push(extra)
        out, i = c[self.rulename].accept(string, pos, c)
        if out is Miss:
            raise ParserError(i)
        assert i == len(string)
        return out

    def push(self, m):
        self.context = self.context.push(m)

    def snap(self):
        c = self.context
        for name, rule in sorted(self.ruledict.items()):
            self.ruledict[name] = rule.snap(c)


class BootGrammar(BaseGrammar):
    def __init__(self):
        self.context = parser_context()

    def parse(self, string, pos=0, **extra):
        from bookish.parser import bootstrap

        bc = self.context.push(extra)
        out, i = bootstrap.grammar.accept(string, pos, bc)
        if out is Miss:
            chain = i()
            pos = chain[0]["pos"]
            print(repr(string[pos:pos+10]))
            raise ParserError(chain)
        assert i == len(string) or string[i] == u"\uffff"
        return out
