import sys

from bookish import parser as p


def test_context():
    c = p.ParserContext()
    c["a"] = 5
    assert "a" in c
    assert c.get("a") == 5

    c2 = c.push()
    assert c2.get("a") == 5
    c2["b"] = 15
    assert c2.get("a") == 5
    assert c2.get("b") == 15

    assert c.get("a") == 5
    assert not ("b" in c)


def test_any():
    r = p.Any
    assert r.test("a") == "a"
    assert r.test("b") == "b"
    # assert r.test([None]) is None
    # assert r.test([0]) == 0


def test_Match():
    r = p.Match("a")
    assert r.test("a") == "a"
    assert r.test("b") is p.Miss


def test_in():
    r = p.In("ab")
    assert r.test("a") == "a"
    assert r.test("b") == "b"
    assert r.test("c") is p.Miss


def test_not():
    r = p.Not("b")
    assert r.test("a") is p.Empty
    assert r.test("b") is p.Miss
    assert r.test("c") is p.Empty


def test_opt():
    r = p.Opt("a")
    assert r.test("a") == ["a"]
    assert r.test("b") == []


def test_repeat():
    r = p.Repeat("a", mintimes=1, maxtimes=None)
    assert r.test("bbbb") is p.Miss
    assert r.test2("aaab") == (["a", "a", "a"], 3)

    r = p.Repeat("a", mintimes=0, maxtimes=2)
    assert r.test("bbbb") == []
    assert r.test2("aaab") == (["a", "a"], 2)

    r = p.Repeat("a", mintimes=2, maxtimes=3)
    assert r.test("bbbb") is p.Miss
    assert r.test("abbb") is p.Miss
    assert r.test2("aabb") == (["a", "a"], 2)
    assert r.test2("aaab") == (["a", "a", "a"], 3)
    assert r.test2("aaaa") == (["a", "a", "a"], 3)


def test_lookahead():
    r = p.Peek("a")
    assert r.test("a") is p.Empty
    assert r.test("b") is p.Miss


def test_bind():
    r1 = p.In("abc")
    assert r1.test("abcd") == "a"

    r2 = p.Repeat(r1, 1)
    assert r2.test("abcd") == ["a", "b", "c"]

    r3 = p.Bind("x", r2)
    c = p.ParserContext()
    assert r3.test("abcd", context=c) == ["a", "b", "c"]
    assert c["x"] == ["a", "b", "c"]

    r4a = p.In("abc")
    r4b = p.Bind("e2", r4a)
    r4c = p.Or(["*" + p.Do("'x' + e2"),
                "+" + p.Do("'y' + e2"),
                "?" + p.Do("'z' + e2")
                ])
    r4 = r4b + r4c

    c = p.ParserContext()
    assert r4b.test("a*", context=c)
    assert "e2" in c

    c = p.ParserContext()
    assert r4.test("a*", context=c) == "xa"
    c = p.ParserContext()
    assert r4.test("a+", context=c) == "ya"
    c = p.ParserContext()
    assert r4.test("a?", context=c) == "za"


def test_predicate():
    r = p.Seq([p.Bind("x", p.Repeat(p.In("abc"), 1)),
                    p.If("x and x[0] == 'a'"),
                    "z"])
    assert r.test2("abcz") == ("z", 4)
    assert r.test("bcz") is p.Miss


def test_or():
    r = p.Or(["a", "b"])
    assert r.test("a") == "a"
    assert r.test("b") == "b"
    assert r.test("c") is p.Miss

    r = p.Or(["0", p.Repeat("1", 0, 2)])
    assert r.test2("0111") == ("0", 1)
    assert r.test2("111") == (["1", "1"], 2)
    assert r.test("2") == []


def test_regex():
    r = p.Regex("a[bc]d")
    assert r.test("abd")
    assert r.test("acd")
    assert r.test("add") is p.Miss
    assert r.test("ab") is p.Miss

    c = p.ParserContext()
    r = p.Regex("a(?P<foo>[abc]+)d")
    assert r.test("abcbbcd", context=c)
    assert c["foo"] == "bcbbc"


def test_fixedwidth():
    c = p.ParserContext()
    assert p.Any.fixed_length(c) == 1
    assert p.streamstart.fixed_length(c) == 0
    assert p.linestart.fixed_length(c) == 0
    assert p.lineend.fixed_length(c) == 0
    assert p.streamend.fixed_length(c) == 0
    assert p.Match("a").fixed_length(c) == 1
    assert p.String("abc").fixed_length(c) == 3
    assert p.In("abc").fixed_length(c) == 1
    assert p.Or(["a", "bc", "def"]).fixed_length(c) == -1
    assert p.Or(["ab", "bc", "cd"]).fixed_length(c) == 2
    assert p.Seq(["a", "bc", "def"]).fixed_length(c) == 6
    assert p.Seq([p.streamstart, "bc", p.lineend]).fixed_length(c) == 2
    assert p.Seq([p.Or(["a", "b"]), "c"]).fixed_length(c) == 2
    assert p.Seq([p.Or(["a", "bc"]), "d"]).fixed_length(c) == -1
    assert p.Not("a").fixed_length(c) == 0
    assert p.Repeat("a").fixed_length(c) == -1
    assert p.Repeat("a", mintimes=2, maxtimes=2).fixed_length(c) == 2
    assert p.Peek("a").fixed_length(c) == 0
    assert p.Bind("foo", "abc").fixed_length(c) == 3
    assert p.Take("abc").fixed_length(c) == 3
    assert p.Do("a + b").fixed_length(c) == 0
    assert p.If("a == b").fixed_length(c) == 0
    assert p.Regex("a[bc]d").fixed_length(c) == -1
    assert p.LookBehind("abc").fixed_length(c) == 0


def test_lookbehind():
    r = p.Plus(p.In("abcdefgh")) + p.LookBehind(p.In("abc")) + p.Or(["!", "?"])
    assert r.test("a!")
    assert r.test("b?")
    assert r.test("defghb?")
    assert r.test("abcdef!") is p.Miss
    assert r.test("g") is p.Miss
    assert r.test("g!") is p.Miss

    r = (p.Plus(p.In("abcd")) + p.LookBehind(p.Bind("foo", p.In("ab")))
         + "!" + p.Do("foo"))
    c = p.ParserContext()
    assert r.test("bc!") is p.Miss
    assert r.test("ab!", context=c) == "b"


# def test_mixed():
#     r1 = p.Or(["a", "b", "c"])
#
#     r2 = p.Mixed(r1, runoff=False)
#     assert r2.test("12a34b56c0") is p.Miss
#
#     r3 = p.Mixed(r1, runoff=True)
#     assert (r3.test("12a34b56c7")
#             == (["12", "a", "34", "b", "56", "c", "7"], 10))
#
#     r4 = p.Mixed(r1, "d")
#     assert r4.test("12a34d56c7") == (["12", "a", "34"], 5)


def test_do():
    r1 = p.Bind("eqs", p.Repeat("=", 2))
    r2 = p.Seq([r1, p.Do("len(eqs) - 1")])
    assert r2.test2("====", context=p.ParserContext()) == (3, 4)


def test_pythonexpr():
    r = p.PythonExpr(" )")
    assert r.test2("a)") == ("a", 1)
    assert r.test2("foo[1])") == ("foo[1]", 6)


def test_appargs():
    r = p.appargs
    assert r.test2("a)") == (["a"], 1)





