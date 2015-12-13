import os.path

from bookish import parser as p
from bookish import util
from bookish.parser import bootstrap as bs
from bookish.parser import rules
from bookish.compat import unichr


def _boot_parse(inp, **extra):
    c = bs.bootstrap_context().push(extra)
    out, i = bs.rule.accept(inp, 0, c)
    if out is p.Miss:
        print(i())
    assert out is not p.Miss
    return out.snap(c)


def _test_rule(rule, inp):
    return rule.test(inp, context=bs.bootstrap_context())


def test_comment():
    r = _boot_parse('comment = "#" (~"\\n" Any)*')
    print(r.repr())
    print(bs.comment.repr())
    assert r == bs.comment

    assert _test_rule(r, "#hello") == list("hello")
    assert _test_rule(r, "#a\nb") == ["a"]
    assert _test_rule(r, "abc") is p.Miss


def test_hspace():
    rule = _boot_parse("hspace = ' ' | '\\t' | comment")
    assert rule == p.String(" ") | p.String("\t") | bs.comment

    assert _test_rule(rule, " \t #blah") is not p.Miss
    assert _test_rule(rule, "\n") is p.Miss


def test_vspace():
    rule = _boot_parse('vspace = "\\r\\n" | "\\r" | "\\n"')
    assert rule == p.String("\r\n") | p.String("\r") | p.String("\n")

    assert _test_rule(rule, "\n") is not p.Miss
    assert _test_rule(rule, "\r") is not p.Miss
    assert _test_rule(rule, "\r\n") == "\r\n"
    assert _test_rule(rule, "\t") is p.Miss


def test_ws():
    rule = _boot_parse("ws = (hspace | vspace | comment)*")
    assert type(rule) is p.Star
    t = rule.target
    assert type(t) is p.Or
    assert t[0] == bs.hspace
    assert t[1] == bs.vspace
    assert t[2] == bs.comment

    assert _test_rule(rule, "  \t #hello\n\n#comment\n") is not p.Miss
    assert _test_rule(rule, "abc") == []


def test_emptyline():
    rule = _boot_parse("emptyline = hspace* vspace")
    assert type(rule) is p.Seq
    assert type(rule[0]) is p.Star
    assert rule[0].target is bs.hspace
    assert rule[1] is bs.vspace


def test_indent():
    rule = _boot_parse("indent = emptyline* hspace+")
    assert type(rule) is p.Seq
    assert type(rule[0]) is p.Star
    assert rule[0].target is bs.emptyline
    assert type(rule[1]) is p.Plus
    assert rule[1].target is bs.hspace


def test_noindent():
    rule = _boot_parse("noindent = emptyline* ~~~hspace")
    assert type(rule) is p.Seq
    assert type(rule[0]) is p.Star
    assert rule[0].target is bs.emptyline
    assert type(rule[1]) is p.Peek
    assert type(rule[1].target) is p.Not
    assert rule[1].target.target is bs.hspace


def test_digit():
    rule = _boot_parse("digit = [0123456789]")
    assert type(rule) is p.In
    assert rule.match == "0123456789"


def test_digits():
    digit = _boot_parse("digit = [0123456789]")
    rule = _boot_parse("digits = digit+", digit=digit)
    assert type(rule) is p.Plus
    assert rule.target is digit


def test_number():
    rule = _boot_parse("""
number = ws ('-' barenum:x -> -x
             | barenum:x -> x
             )
    """)

    target = "($ws ((S'-' ($barenum):x ->(-x)) | (($barenum):x ->(x))))"
    assert rule.repr() == target

    assert _test_rule(rule, "0xff") == 255
    assert _test_rule(rule, "0x0123456789") == 4886718345
    assert _test_rule(rule, "0xAaBbCcDdEeFf") == 187723572702975
    assert _test_rule(rule, "af") is p.Miss
    assert rule.test2("0af") == (0, 1)

    assert _test_rule(rule, "1234567890") == 1234567890
    assert _test_rule(rule, "01") == 1

    assert _test_rule(rule, "0xDEADBEEF") == 3735928559
    assert _test_rule(rule, "0100") == 100

    assert _test_rule(rule, "12345") == 12345
    assert _test_rule(rule, "0xdeadbeef") == 3735928559
    assert _test_rule(rule, "-50") == -50
    assert _test_rule(rule, "-0xdeadbeef") == -3735928559


def test_escape():
    rule = _boot_parse(r"""
escchar = '\\' ('n' -> "\n"
                | 'r' -> "\r"
                | 't' -> "\t"
                | 'b' -> "\b"
                | 'f' -> "\f"
                | '"' -> '"'
                | '\'' -> "'"
                | 'x' <hexdigit hexdigit>:d -> compat.unichr(int(d, 16))
                | '\\' -> "\\")
    """)

    assert _test_rule(rule, "\\n") == "\n"
    assert _test_rule(rule, "\\r") == "\r"
    assert _test_rule(rule, "\\t") == "\t"
    assert _test_rule(rule, "\\b") == "\b"
    assert _test_rule(rule, "\\f") == "\f"
    assert _test_rule(rule, '\\"') == '"'
    assert _test_rule(rule, "\\'") == "'"
    assert _test_rule(rule, "\\xFF") == unichr(255)
    assert _test_rule(rule, "\\\\") == "\\"
    assert _test_rule(rule, "\\") is p.Miss


def test_char():
    rule = _boot_parse(r"char = ws '\'' (~'\'' (escchar | Any)):c '\'' -> c")

    assert _test_rule(rule, "'a'") == "a"
    assert _test_rule(rule, "'\\n'") == "\n"
    assert _test_rule(rule, "'a") is p.Miss
    assert _test_rule(rule, "a'") is p.Miss


def test_string():
    rule = _boot_parse("""
    string = ws '\"' (escchar | ~('\"') Any)*:c '\"' -> ''.join(c)
    """.strip())

    target = "($ws S'\"' (($escchar | ((~S'\"') Any))*):c S'\"' ->(''.join(c)))"
    assert rule.repr() == target

    assert _test_rule(rule, '"abc"') == "abc"
    assert _test_rule(rule, '"a"') == "a"
    assert _test_rule(rule, '"\\n\\t"') == "\n\t"


def test_category():
    rule = _boot_parse("category = ws '[' (escchar | ~(']') Any)*:xs ']' -> In(set(xs))")
    assert rule.repr() == "($ws S'[' (($escchar | ((~S']') Any))*):xs S']' ->(In(set(xs))))"

    assert _test_rule(rule, "[abc]") == p.In("abc")


def test_args():
    rule = _boot_parse("""
args = ('(' r.appargs:aa ')' -> aa
        | -> [])
    """)
    rule.dump()

    assert _test_rule(rule, "abc") == []
    assert _test_rule(rule, "(a)") == ["a"]
    assert _test_rule(rule, "(a b)") == ["a", "b"]


def test_grammar():
    def calculate(start, pairs):
        result = start
        for op, value in pairs:
            if op == '+':
                result += value
            elif op == '-':
                result -= value
            elif op == '*':
                result *= value
            elif op == '/':
                result /= value
        return result

    bg = p.BootGrammar()
    mathg = bg.parse("""
digit = [0123456789]
number = <digit+>:ds -> int(ds)
parens = '(' ws mexpr:e ws ')' -> e
value = number | parens
ws = ' '*
add = '+' ws mexpr2:n -> ('+', n)
sub = '-' ws mexpr2:n -> ('-', n)
mul = '*' ws value:n -> ('*', n)
div = '/' ws value:n -> ('/', n)

addsub = ws (add | sub)
muldiv = ws (mul | div)

mexpr = mexpr2:left addsub*:right -> calculate(left, right)
mexpr2 = value:left muldiv*:right -> calculate(left, right)
    """)

    gc = mathg.context.push({"calculate": calculate})
    mexpr = gc["mexpr"]

    assert mexpr.test("4", context=gc) == 4
    assert mexpr.test("456", context=gc) == 456
    assert mexpr.test("6+5", context=gc) == 11
    assert mexpr.test("6-5", context=gc) == 1
    assert mexpr.test("6+1+3", context=gc) == 10
    assert mexpr.test("15*3", context=gc) == 45
    assert mexpr.test("(1+3)", context=gc) == 4
    assert mexpr.test("3 * (5 + 6) + 7", context=gc) == 40


def test_parse_regex_rule():
    # Use the bootstrap rules to parse the rule
    rulestring = """
regex = ws "/" (~"/" (("\\\\/" -> "/") | r.Any))*:pattern "/"
        -> ''.join(pattern)
    """
    c = bs.bootstrap_context()
    rrule, i = bs.rule.accept(rulestring, 0, c)
    # rrule.dump()

    # Use the new rule to parse an example
    estr = "/(.*?)\\/\\w+/"
    assert rrule.test(estr, context=c) == "(.*?)/\\w+"


def test_parse_string_rule():
    rulestring = p.Document(r"""
string = ws "\"" (escchar | ~"\"" r.Any)+:c "\""
         -> String(''.join(c))
    """.strip())

    c = bs.bootstrap_context()
    rule, i = c["rule"].accept(rulestring, 0, c)
    assert i == len(rulestring)

    assert rule.test('"a"', context=c) == p.String("a")
    assert rule.test('"a"', context=c) == p.String("a")
    assert rule.test('"ab"', context=c) == p.String("ab")
    assert rule.test('"ab"', context=c) == p.String("ab")


def test_parse_entity_rule():
    # Use the bootstrap rules to parse the rule
    rulestring = p.Document("""
charhex = 'x' [0123456789abcdefABCDEF]+:h -> int(''.join(h), 16)
chardec = [0123456789]+:d -> int(''.join(d))
charnum = (charhex | chardec)
entity = "&#" charnum:num ';' -> compat.unichr(num)
    """.strip())
    c = bs.bootstrap_context()
    rulelist, i = rules.Star(bs.rule).accept(rulestring, 0, c)
    ruledict = dict((rule.rulename, rule) for rule in rulelist)

    xc = c.push(ruledict)
    # Use the new rule to parse an example
    assert ruledict["entity"].test("&#1024;", context=xc) == u"\u0400"
    assert ruledict["entity"].test("&#x1024;", context=xc) == u"\u1024"


def test_parse_mixed_rule():
    rulestring = p.Document("""
mixed = ws "@(" expr1:until (ws ',' expr1:e -> e
                             | -> None
                             ):aim ')' -> Mixed(until, aim)
    """.strip())
    c = bs.bootstrap_context()
    rule, i = bs.rule.accept(rulestring, 0, c)
    assert i == len(rulestring)


def test_parse_meta_string():
    gstring = util.builtin_grammar("meta.bkgrammar")
    bg = p.BootGrammar()
    #bg.context.tracing = True
    out, i = bg.context["rule"].accept(gstring, 0, bg.context)
    assert out is not p.Miss


def test_parse_meta():
    gstring = util.builtin_grammar("meta.bkgrammar")

    # Use the bootstrap parser to parse the meta grammar
    mg = p.BootGrammar().parse(gstring)
    assert isinstance(mg, p.Grammar)

    # Use the meta-grammar to parse itself
    mg2 = mg.parse(gstring)

    rd1 = mg.ruledict
    rd2 = mg2.ruledict

    # Check that the results are the same
    assert rd1.keys() == rd2.keys()
    pairs = [(rd1[k], rd2[k]) for k in sorted(rd1.keys())]
    for r1, r2 in pairs:
        if r1 != r2:
            r1.dump()
            r2.dump()
        assert r1 == r2


def _metagrammar():
    gstring = util.builtin_grammar("meta.bkgrammar")

    # Use the bootstrap parser to parse the meta grammar
    mg = p.BootGrammar().parse(gstring)
    assert isinstance(mg, p.Grammar)

    # Use the meta-grammar to parse itself
    mg2 = mg.parse(gstring)
    return mg2


def test_parse_lookbehind():
    rulestring = p.Document("""
lookbehind = '^' expr1:e -> LookBehind(e)
    """)
    c = bs.bootstrap_context()
    rule, i = bs.rule.accept(rulestring, 0, c)

    assert rule.test("^'a'", context=c) == p.LookBehind(p.String("a"))


def test_parse_lookbehind_in_grammar():
    mg = _metagrammar()
    xc = mg.context
    expr = xc["expr"]

    assert expr.accept("^'a'", 0, xc) == (p.LookBehind(p.String("a")), 4)
    assert expr.accept("'a' ^'a'", 0, xc) == (p.Seq([p.String("a"), p.LookBehind("a")]), 8)

    gram = rules.Star(xc["rule"])
    rulelist, i = gram.accept(p.Document("""
foo = [ab]+ ^'c' 'd'
bar = ^' ' | linestart 'x'
baz = ~^' ':c
    """), 0, xc)
    d = dict((rule.rulename, rule.snap(xc)) for rule in rulelist)
    assert d["foo"] == p.Plus(p.In("ab")) + p.LookBehind("c") + p.String("d")
    assert d["bar"] == p.LookBehind(" ") | (p.linestart + p.String("x"))
    assert d["baz"] == p.Bind("c", p.Not(p.LookBehind(" ")))


# def test_error():
#     gstring = p.Document("""
# x = [0123456789]
# y = [abc]
# expr =
#       | x
#       | y
#     """)
#
#     c = _ctx()
#     rule = c.rule("grammar")
#     try:
#         rule.accept(gstring, 0, c)
#     except p.NoMatch as e:
#         assert e.pos == 28
#         # The row and col returned by line_and_col are 0-based
#         assert gstring.line_and_col(e.pos) == (3, 0)
#     else:
#         assert False


def test_metaparse_regex():
    mg = _metagrammar()
    print(mg.ruledict)
    assert "ws" in mg.context

    gstring = p.Document("""
    x = /foo(?P<num>[0-9]+)/
    """.strip())
    rg = mg.parse(gstring, context=p.parser_context())

    assert len(rg.ruledict) == 1
    rule = rg.ruledict["x"]
    assert type(rule) is p.Regex
    assert rule.match == "foo(?P<num>[0-9]+)"

    xc = p.ParserContext()
    out, i = rule.accept("foo123", 0, xc)
    assert xc["num"] == "123"
    assert out == "foo123"
    assert i == 6


def test_repeat():
    mg = _metagrammar()
    gstring = """
y = 'b'{3}
z = 'z'{4,}
x = 'a'{2,5}
    """.strip()
    rg = mg.parse(gstring, context=p.parser_context())

    x = rg.ruledict["x"]
    assert type(x) is p.Repeat
    assert x.mintimes == 2
    assert x.maxtimes == 5

    y = rg.ruledict["y"]
    assert type(y) is p.Repeat
    assert y.mintimes == 3
    assert y.maxtimes == 3

    z = rg.ruledict["z"]
    assert type(z) is p.Repeat
    assert z.mintimes == 4
    assert z.maxtimes is None


def test_action():
    mg = _metagrammar()
    gstring = """
    x = !(None)
    """.strip()
    rg = mg.parse(gstring, context=p.parser_context())

    x = rg.ruledict["x"]
    assert type(x) is p.Do
    assert x.source == "None"


def test_take():
    mg = _metagrammar()
    gstring = """
    paren = "(" <(~")" Any)+>:tag ")" -> tag
    """.strip()
    rg = mg.parse(gstring, context=p.parser_context())
    paren = rg.ruledict["paren"]

    out, i = paren.accept("(hi)", 0, p.parser_context())
    assert out == "hi"
