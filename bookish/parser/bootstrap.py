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


import sys
from string import ascii_letters, digits

from bookish import compat
from bookish.parser import rules as r
from bookish.parser import parser as p


__all__ = ("comment hspace vspace ws emptyline indent noindent "
           "hexdigit hexnum decnum barenum negnum number escchar string "
           "name args application application2 rvexpr rulevalue actionexpr "
           "predicate brackets take expr1 expr2 repeattimes expr3 "
           "expr3a expr4 expr ruleend rule grammar"
           ).split()

comment = r.String("#") + r.Star(r.Not("\n") + r.Any)
hspace = r.In(" \t") | comment
vspace = r.Or(["\r\n", "\r", "\n"])
ws = r.Star(hspace | vspace | comment)

emptyline = r.Star(hspace) + vspace
indent = r.Star(emptyline) + r.Plus(hspace)
noindent = r.Star(emptyline) + r.Not(r.Peek(hspace))

hexdigit = r.In(digits + "abcdefABCDEF")
hexnum = (
    r.String("0")
    + r.In("xX")
    + r.Bind("ds", r.Plus(hexdigit))
    + r.Do("int(''.join(ds), 16)")
)
decnum = r.Bind("ds", r.Plus(r.In(digits))) + r.Do("int(''.join(ds))")
barenum = hexnum | decnum
negnum = "-" + r.Bind("x", barenum) + r.Do("-x")
number = ws + (negnum | barenum)

escchar = r.Match("\\") + r.Or([
    "n" + r.Do("'\\n'"),
    "r" + r.Do("'\\r'"),
    "t" + r.Do("'\\t'"),
    "b" + r.Do("'\\b'"),
    "f" + r.Do("'\\f'"),
    '"' + r.Do("'\\\"'"),
    "'" + r.Do("'\\''"),
    "x" + r.Bind("hs", hexdigit * 2) + r.Do("compat.unichr(int(''.join(hs), 16))"),
    "\\" + r.Do("'\\\\'")
])

string = (
    ws
    + r.Bind("s", r.Or([
        r.Seq([
            '"',
            r.Bind("s", r.Star(r.Not('"') + (escchar | r.Any))),
            '"',
            r.Do("s")
        ]),
        r.Seq([
            "'",
            r.Bind("s", r.Star(r.Not("'") + (escchar | r.Any))),
            "'",
            r.Do("s")
        ])
    ]))
    + r.Do("String(''.join(s))")
)

category = (
    ws
    + '['
    + r.Bind("xs", r.Plus(r.Not(']') + (escchar | r.Any)))
    + "]"
    + r.Do("In(set(xs))")
)

name = r.Take(
    r.In("_" + ascii_letters)
    + r.Star(r.In("_" + ascii_letters + digits))
)

args = r.Or(["(" + r.Bind("args", r.appargs) + ")" + r.Do("args"),
             r.Do("[]")])
application = (
    r.Opt(indent)
    + r.Bind("rule", name)
    + r.Bind("args", args)
    + r.Do("Call(rule, args)")
)
application2 = (
    r.Opt(indent)
    + r.Bind("mod", name)
    + "." + r.Bind("rule", name)
    + r.Bind("args", args)
    + r.Do("Call2(mod, rule, args)")
)

rvexpr = r.PythonExpr("\r\n)]")
rulevalue = ws + "->" + r.Bind("code", rvexpr) + r.Do("Do(''.join(code).strip())")

actionexpr = r.PythonExpr(")")
action = ws + "!(" + r.Bind("code", actionexpr) + ")" + r.Do("Do(code)")

predicate = ws + "?(" + r.Bind("code", actionexpr) + ")" + r.Do("If(code)")

brackets = (ws + "(" + r.Bind("e", r.Call("expr")) + ws + ")" + r.Do("e"))
take = (ws + "<" + r.Bind("e", r.Call("expr")) + ws + ">" + r.Do("Take(e)"))

expr1 = (
    application2
    | application
    | rulevalue
    | predicate
    | action
    | number
    | string
    | category
    | brackets
    | take
)

expr2 = (
    (
        ws
        + "~"
        + r.Or([
            "~" + r.Bind("e2", r.Call("expr2")) + r.Do("Peek(e2)"),
            r.Bind("e2", r.Call("expr2")) + r.Do("Not(e2)")
        ])
    )
    | expr1
)

repeattimes = r.Seq([
    "{",
    r.Bind("mn", barenum),
    r.Bind("mx", (',' + (barenum | r.Do("None")) | r.Do("mn"))),
    "}"
])

expr3a = r.Bind("e2", expr2) + r.Or(["*" + r.Do("Star(e2)"),
                                     "+" + r.Do("Plus(e2)"),
                                     "?" + r.Do("Opt(e2)"),
                                     r.Do("e2")
                                     ])
expr3 = (
    r.Bind("r", expr3a)
    + (
        (r.String(":") + r.Bind("n", name) + r.Do("Bind(n, r)"))
        | r.Do("r")
    )
)

expr4 = (
    r.Bind("e3s", r.Plus(expr3))
    + r.Do("e3s[0] if len(e3s) == 1 else Seq(e3s)")
)

expr = (
    r.Bind("e4", expr4)
    + r.Bind("e4s", r.Star(ws + "|" + expr4))
    + r.Do("Or([e4] + e4s) if e4s else e4")
)

ruleend = (r.Star(hspace) + r.Plus(vspace)) | r.streamend

rule = (
    noindent
    + r.Bind("n", name)
    + ws + r.Bind("args", args)
    + ws + "="
    + r.Bind("e", expr) + ruleend
    + r.Do("r.make_rule(n, e, args)")
)

grammar = (
    r.Bind("rs", r.Star(rule))
    + ws
    + r.streamend
    + r.Do("make_grammar(rs)")
)


bootstrap_rules = p.rules_from_locals(locals(), __all__)


def bootstrap_context():
    from bookish.parser.parser import ParserContext

    m = {"r": r, "compat": compat}
    m.update(bootstrap_rules)
    m.update(r.basic_rules)
    ctx = ParserContext(m)

    def _add_import(modname, bindname):
        __import__(modname)
        ctx[bindname] = sys.modules[modname]
    ctx["add_import"] = _add_import

    return ctx
