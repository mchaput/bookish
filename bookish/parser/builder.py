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

from __future__ import print_function
import sys
from textwrap import dedent

from bookish.compat import string_type, indent
from bookish.parser import bootstrap, rules, Lines
from bookish.parser.parser import condition_string, BootGrammar, Miss


def _fill_args(context, names, values):
    return context.push(dict(zip(names, values)))


def build_meta(content, outfile):
    content = condition_string(content)
    # content = Document(content)
    bg = BootGrammar()
    mg = bg.parse(content)
    b = Builder(file=outfile)
    b.run(mg.ruledict.values())


def parse_string(content, ctx):
    from bookish.grammars import meta as mg

    content = condition_string(content)
    # content = Document(content)
    g, i = mg.grammar(content, 0, ctx)
    if g is Miss:
        ls = Lines(content)
        i = 225
        line, col = ls.line_and_col(i)
        print("i=", i, "line=", line, "col=", col)

    assert g is not Miss
    g.snap()
    return g


class Builder(object):
    def __init__(self, globals=None, file=None, context=None):
        self.globals = globals
        self.file = file or sys.stdout

        self.imports = []
        self.assignments = {}
        self.computed_assignments = {}
        self.args = {}
        self.rules = {}
        self.methods = {}
        self.aliases = {}
        self.assertions = []
        self.binding = {}
        self.context = context

    def add_import(self, modname, bindname):
        self.imports.append((modname, bindname))

    def add_assignment(self, rule, suffix, expr):
        name = "%s_%s" % (self.name(rule), suffix)
        self.assignments[name] = expr
        return name

    def add_computed_assignment(self, rule, suffix, fn):
        name = "%s_%s" % (self.name(rule), suffix)
        self.computed_assignments[name] = fn
        return name

    def add_parms(self, name, argnames):
        self.args[name] = argnames

    def arity(self, rulename):
        return len(self.args.get(rulename, []))

    def add_alias(self, callname, realname):
        self.aliases[callname] = realname

    def add_assertion(self, fn, msgfn):
        self.assertions.append((fn, msgfn))

    def _run_assertions(self):
        for fn, msgfn in self.assertions:
            if fn(self):
                raise Exception(msgfn(self))

    def get_method(self, n):
        if isinstance(n, string_type):
            return self.methods[n]
        else:
            return n

    def name(self, rule):
        if isinstance(rule, rules.Call2) and not rule.args:
            return rule.qname()
        elif isinstance(rule, rules.Call) and not rule.args:
            t = rule.target
            if isinstance(t, string_type):
                return t
            else:
                return self.name(t)
        else:
            return rule.getname()

    def qname(self, rule):
        if isinstance(rule, rules.Call2) and not rule.args:
            return rule.qname()
        else:
            return self.name(rule)

    def build_rule(self, rule):
        if isinstance(rule, rules.Call):
            name = rule.getname()
        else:
            name = self.name(rule)

        if name in self.rules:
            return

        self.rules[name] = rule
        code = rule.build(self)
        if code:
            i = code.find("\n")
            if i >= 0 and not code[:i]:
                code = code[i + 1:]
            code = dedent(code.rstrip())
        self.methods[name] = code

    def build_string(self, content):
        content = condition_string(content)
        ctx = bootstrap.bootstrap_context()
        ctx["add_import"] = self.add_import
        g = parse_string(content, ctx)
        g.snap()
        self.run(g.ruledict.values())

    def run(self, rulelist):
        f = self.file

        for rule in rulelist:
            if isinstance(rule, rules.Parms):
                self.add_parms(rule.getname(), rule.args)

        for rule in rulelist:
            self.build_rule(rule)
        self._run_assertions()

        print("#encoding: utf8\n", file=f)
        print("import re", file=f)
        print("from bookish import compat", file=f)
        print("from bookish.parser.builder import _fill_args", file=f)
        print("from bookish.parser.parser import make_grammar", file=f)
        print("from bookish.parser.parser import Empty, Failure, Miss", file=f)
        print("from bookish.parser.parser import ParserError", file=f)
        print("from bookish.parser import rules as r", file=f)

        if self.imports:
            print(file=f)
            for modname, bindname in sorted(self.imports):
                if not bindname or modname == bindname:
                    print("import %s" % modname, file=f)
                else:
                    print("import %s as %s" % (modname, bindname), file=f)
        print("\n", file=f)

        count = 0
        for name, code in sorted(self.methods.items()):
            if not code:
                continue

            print("# " + repr(self.rules[name]), file=f)
            print("def %s(stream, i, context):" % name, file=f)
            print(indent(code, "    "), file=f)
            print("\n", file=f)
            count += 1
        print("# %s functions" % len(self.methods), file=f)

        if self.assignments or self.computed_assignments:
            print("\n", file=f)

            for name, code in sorted(self.assignments.items()):
                print("%s = %s" % (name, code), file=f)

            for name, fn in sorted(self.computed_assignments.items()):
                print("%s = %s" % (name, fn(self)), file=f)

        if self.aliases:
            print("\n", file=f)
            for name, value in sorted(self.aliases.items()):
                print("%s = %s" % (name, value), file=f)
