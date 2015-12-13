import nose.tools


from bookish import parser as p
from bookish.compat import unichr
from bookish.parser import bootstrap as bs


def _ctx():
    return bs.bootstrap_context()


def test_comment():
    assert bs.comment.test("#hello") == list("hello")
    assert bs.comment.test2("#a\nb") == (["a"], 2)
    assert bs.comment.test("abc") is p.Miss


def test_hspace():
    assert bs.hspace.test(" \t #blah") is not p.Miss
    assert bs.hspace.test("\n") is p.Miss


def test_vspace():
    assert bs.vspace.test("\n") is not p.Miss
    assert bs.vspace.test("\r") is not p.Miss
    assert bs.vspace.test2("\r\n")[1] == 2
    assert bs.vspace.test("\t") is p.Miss


def test_ws():
    assert bs.ws.test("  \t #hello\n\n#comment\n") is not p.Miss
    assert bs.ws.test("abc") == []


def test_emptyline():
    assert bs.emptyline.test("       \n") is not p.Miss
    assert bs.emptyline.test("\t   \t    \n") is not p.Miss
    assert bs.emptyline.test("   ") is p.Miss  # Doesn't end with newline
    assert bs.emptyline.test("   a") is p.Miss


def test_indent():
    assert bs.indent.test("     ") is not p.Miss
    assert bs.indent.test("\n  \n    ") is not p.Miss
    assert bs.indent.test("\n\n") is p.Miss


def test_noindent():
    assert bs.noindent.test("") is not p.Miss
    assert bs.noindent.test("\n\n") is not p.Miss
    assert bs.noindent.test("\n  ") is p.Miss


def test_numbers():
    assert bs.hexnum.test2("0xff") == (255, 4)
    assert bs.hexnum.test2("0x0123456789") == (4886718345, 12)
    assert bs.hexnum.test2("0xAaBbCcDdEeFf") == (187723572702975, 14)
    assert bs.hexnum.test("af") is p.Miss
    assert bs.hexnum.test("0af") is p.Miss

    assert bs.decnum.test2("1234567890") == (1234567890, 10)
    assert bs.decnum.test2("01") == (1, 2)

    assert bs.barenum.test2("0xDEADBEEF") == (3735928559, 10)
    assert bs.barenum.test2("0100") == (100, 4)

    assert bs.number.test2("12345") == (12345, 5)
    assert bs.number.test2("0xdeadbeef") == (3735928559, 10)
    assert bs.number.test2("-50") == (-50, 3)
    assert bs.number.test2("-0xdeadbeef") == (-3735928559, 11)


def test_escape():
    assert bs.escchar.test2("\\n") == ("\n", 2)
    assert bs.escchar.test2("\\r") == ("\r", 2)
    assert bs.escchar.test2("\\t") == ("\t", 2)
    assert bs.escchar.test2("\\b") == ("\b", 2)
    assert bs.escchar.test2("\\f") == ("\f", 2)
    assert bs.escchar.test2('\\"') == ('"', 2)
    assert bs.escchar.test2("\\'") == ("'", 2)
    assert bs.escchar.test2("\\xFF", context=_ctx()) == (unichr(255), 4)
    assert bs.escchar.test2("\\\\") == ("\\", 2)
    assert bs.escchar.test("\\") is p.Miss


def test_string():
    assert bs.string.test2('"abc"', context=_ctx()) == (p.String("abc"), 5)
    assert bs.string.test2('"a"', context=_ctx()) == (p.String("a"), 3)
    assert bs.string.test2('"\\n\\t"', context=_ctx()) == (p.String("\n\t"), 6)


def test_name():
    assert bs.name.test2("abc def") == ("abc", 3)
    assert bs.name.test2("k12 m16") == ("k12", 3)
    assert bs.name.test2("_abc|") == ("_abc", 4)
    assert bs.name.test2("x_y&") == ("x_y", 3)
    assert bs.name.test("12k") is p.Miss
    assert bs.name.test("|") is p.Miss


def test_args():
    assert bs.args.test2("abc", context=_ctx()) == ([], 0)
    assert bs.args.test2("(a)", context=_ctx()) == (["a"], 3)
    assert bs.args.test2("(a b)", context=_ctx()) == (["a", "b"], 5)


def test_application():
    bt = bs.application.test
    assert bt("foo", context=_ctx()) == p.Call("foo", [])
    assert bt("foo(bar)", context=_ctx()) == p.Call("foo", ["bar"])
    assert bt("foo(bar baz)", context=_ctx()) == p.Call("foo", ["bar", "baz"])


def test_rulevalue():
    rvt = bs.rulevalue.test
    assert rvt("-> 123", context=_ctx()) == p.Do("123")
    assert rvt("  -> dict()", context=_ctx()) == p.Do("dict()")
    with nose.tools.assert_raises(p.ParserError):
        rvt("->", context=_ctx())


def test_action():
    assert bs.action.test("!(foo(2, 3))", context=_ctx()) == p.Do("foo(2, 3)")
    assert bs.action.test("!", context=_ctx()) is p.Miss
    with nose.tools.assert_raises(p.ParserError):
        bs.action.test("!()", context=_ctx())


def test_predicate():
    pt = bs.predicate.test
    assert pt("?(foo['fi'])", context=_ctx()) == p.If("foo['fi']")
    assert pt("?", context=_ctx()) is p.Miss
    with nose.tools.assert_raises(p.ParserError):
        pt("?()", context=_ctx())


def test_expr1():
    c = _ctx()
    ex1t = bs.expr1.test
    assert ex1t("foo(bar baz)", context=c) == p.Call("foo", ["bar", "baz"])
    assert ex1t("  -> dict()", context=c) == p.Do("dict()")
    assert ex1t("?(foo['fi'])", context=c) == p.If("foo['fi']")
    assert ex1t("!(foo(2, 3))", context=c) == p.Do("foo(2, 3)")
    assert ex1t("-0xdeadbeef", context=c) == -3735928559
    assert ex1t('"\\n"', context=c) == p.String("\n")
    assert ex1t('"\\n\\t"', context=c) == p.String("\n\t")
    assert ex1t("<!(foo)>", context=c) == p.Take(p.Do("foo"))


def test_expr2():
    c = _ctx()
    assert bs.expr2.test('"a"', context=c) == p.String('a')
    assert bs.expr2.test('~"a"', context=c) == p.Not(p.String("a"))
    assert bs.expr2.test('~~"a"', context=c) == p.Peek(p.String("a"))
    assert bs.expr2.test('~~~"a"', context=c) == p.Peek(p.Not(p.String("a")))


def test_expr3():
    c = _ctx()
    assert bs.expr3.test('"a"', context=c) == p.String('a')
    assert bs.expr3.test('"a"*', context=c) == p.Star('a')
    assert bs.expr3.test('"a"*', context=c) == p.Star('a')
    assert bs.expr3.test('"a"+', context=c) == p.Plus('a')
    assert bs.expr3.test('"a"?', context=c) == p.Opt('a')


def test_expr4():
    c = _ctx()
    assert bs.expr4.test('"a"', context=c) == p.String('a')
    assert bs.expr4.test('"a" "b"', context=c) == p.String("a") + p.String("b")
    assert bs.expr4.test('"a"* "b"+', context=c) == (p.Star(p.String("a"))
                                                     + p.Plus(p.String("b")))


def test_expr():
    c = _ctx()
    assert bs.expr.test('"a"', context=c) == p.String('a')
    assert bs.expr.test('"a" | "b"', context=c) == p.String("a") | p.String("b")
    assert bs.expr.test('"a"|"b"', context=c) == p.String("a") | p.String("b")

    target = (
        (p.Plus(p.String("a")) + p.Opt(p.String("x")))
        | (p.Star(p.String("b")) + p.Not(p.String("y")))
    )
    assert bs.expr.test("'a'+ 'x'?|'b'* ~'y'", context=c) == target


def test_rule():
    c = _ctx()
    inp = 'xyz = "a" ~"b" -> foo'
    rule, pos = bs.rule.accept(inp, 0, c)
    assert pos == len(inp)
    assert rule.rulename == "xyz"
    assert type(rule) == p.Seq
    assert rule == p.Seq([p.String("a"), p.Not(p.String("b")), p.Do("foo")])

    c = _ctx()
    inp = 'qux (arg1 arg2) = "a" "b"'
    rule, pos = bs.rule.accept(inp, 0, c)
    assert pos == len(inp)
    assert rule.rulename == "qux"
    assert type(rule) == p.Parms
    assert rule == p.Parms(["arg1", "arg2"], p.String("a") + p.String("b"))



