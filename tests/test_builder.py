from bookish.compat import StringIO
from bookish.grammars import meta
from bookish.parser import Miss
from bookish.parser.bootstrap import bootstrap_context
from bookish.parser.builder import Builder


def test_parameterized_rule():
    gs = """
import bookish.wikipages as w

xchar = [ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_0123456789]
xname = ~~xchar </[A-Za-z_0-9]+/>
attr = " "+ xname:k "=\\"" <(~'"' r.Any)*>:v '"' -> (k, v)
attrlist = attr*:attrs -> dict(attrs)
ctag(n) = "</" xname:name ?(n == name) ">"
xml = "<" xname:n attrlist:alist ">" @("</", spans):tx ctag(n) -> w.span("xml", tx, tag=n, attrs=alist)
"""

    # ctx = bootstrap_context()
    # g, _ = meta.grammar(gs, 0, ctx)
    # assert g is not Miss
    # sio = StringIO()
    # b = Builder(file=sio)
    # b.run(g.ruledict.values())
    # print(sio.getvalue())
    # assert False

