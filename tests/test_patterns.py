from bookish.avenue import avenue, patterns
from bookish import functions


def ctx(data, **kwargs):
    return avenue.AvenueContext(data, **kwargs)


def test_root():
    data = {
        "type": "root",
        "body": [
            {"type": "para", "text": ["hello"]}
        ]
    }
    c = ctx(data)

    rt = patterns.Root()
    assert list(rt.pull(c, data)) == [data]
    assert rt.matches(c, data)
    assert not rt.matches(c, data["body"])


def test_lookup():
    data = {"foo": "bar", "boo": "baz"}
    assert list(patterns.Lookup("foo").pull(None, data)) == ["bar"]
    assert list(patterns.Lookup("xxx").pull(None, data)) == []

    it = patterns.Lookup("foo")
    assert it.matches(ctx(data), data["foo"])

    data = ["alfa", "bravo", "charlie"]
    assert list(patterns.Lookup(1).pull(None, data)) == ["bravo"]
    assert list(patterns.Lookup(-1).pull(None, data)) == ["charlie"]
    assert list(patterns.Lookup(4).pull(None, data)) == []

    it = patterns.Lookup(1)
    assert it.matches(ctx(data), data[1])


def test_star():
    data = ["foo", "bar", "baz"]

    a = patterns.Star()
    assert list(a.pull(None, data)) == data
    assert a.matches(ctx(data), data[0])
    assert a.matches(ctx(data), data[1])

    data = {
        "alfa": "bravo",
        "charlie": "delta",
        "echo": "foxtrot",
    }
    assert sorted(a.pull(None, data)) == ["bravo", "delta", "foxtrot"]
    assert a.matches(ctx(data), data["alfa"])
    assert a.matches(ctx(data), data["charlie"])


def test_comparison():
    data = {
        "alfa": 10,
        "bravo": 20,
        "charlie": 30,
    }
    c = ctx(data)

    eq = patterns.Comparison("alfa", "==", 10)
    assert list(eq.pull(None, data)) == [data]
    assert eq.matches(c, data)

    gt = patterns.Comparison("bravo", ">", 10)
    assert list(gt.pull(None, data)) == [data]
    assert gt.matches(c, data)

    lte = patterns.Comparison("charlie", "<=", 5)
    assert list(lte.pull(None, data)) == []
    assert not lte.matches(c, data)

    eq = patterns.Comparison("delta", "==", 10)
    assert list(eq.pull(None, data)) == []
    assert not eq.matches(c, data)


def test_regex_comparison():
    data = [
        {"x": "00"},
        {"x": "01"},
        {"x": "10"},
        {"x": "11"},
    ]
    c = ctx(data)

    rx = patterns.Comparison("x", "=~", ".1")
    assert [d["x"] for d in rx.pull(None, data)] == ["01", "11"]
    assert not rx.matches(c, data[0])
    assert rx.matches(c, data[1])
    assert not rx.matches(c, data[2])
    assert rx.matches(c, data[3])


def test_predicate():
    d1 = {
        "alfa": 20,
    }
    d2 = {
        "bravo": 10,
    }

    pr = patterns.Predicate("alfa == 20")
    assert list(pr.pull({}, d1)) == [d1]
    assert pr.matches(ctx(d1), d1)

    assert list(pr.pull({}, d2)) == []
    assert not pr.matches(ctx(d2), d2)


def test_union():
    data = {"alfa": "bravo", "charlie": "delta", "echo": "foxtrot"}
    c = ctx(data)

    p1 = patterns.Lookup("charlie")
    p2 = patterns.Lookup("echo")
    un = patterns.Union([p1, p2])
    assert list(un.pull(None, data)) == ["delta", "foxtrot"]

    assert p1.matches(c, data["charlie"])
    assert un.matches(c, data["charlie"])

    assert p2.matches(c, data["echo"])
    assert un.matches(c, data["echo"])


def test_filter():
    data = {
        "alfa": {"id": 1, "x": 10},
        "bravo": {"id": 2, "x": 20},
        "charlie": {"id": 3, "x": 30},
        "delta": {"id": 4, "x": 40},
    }
    c = ctx(data)

    f = patterns.Filter(
        patterns.Star(),
        patterns.Comparison("x", ">", 25)
    )
    assert sorted(d["id"] for d in f.pull(None, data)) == [3, 4]
    assert not f.matches(c, data["alfa"])
    assert f.matches(c, data["charlie"])


def test_action():
    data = {
        "foo": 10,
        "bar": 20
    }
    a = patterns.Action("foo * baz")
    assert list(a.pull({"baz": 4}, data)) == [40]


def test_child():
    data = {
        "alfa": {
            "bravo": "charlie",
            "delta": "echo"
        },
        "foxtrot": "golf"
    }
    c = ctx(data)

    ch = patterns.Child(patterns.Lookup("alfa"), patterns.Lookup("delta"))
    assert list(ch.pull(None, data)) == ["echo"]
    assert ch.matches(c, data["alfa"]["delta"])
    assert not ch.matches(c, data["alfa"]["bravo"])


def test_sequence():
    data = {
        "alfa": {
            "bravo": "charlie",
            "delta": {
                "echo": "foxtrot",
                "golf": "hotel"
            },
            "india": "juliet",
        },
        "kilo": "lima"
    }
    c = ctx(data)

    seq = patterns.Sequence([
        patterns.Lookup("alfa"),
        patterns.Lookup("delta"),
        patterns.Lookup("golf")
    ])
    assert list(seq.pull(None, data)) == ["hotel"]

    assert seq.matches(c, data["alfa"]["delta"]["golf"])
    assert not seq.matches(c, data["alfa"]["delta"])


def test_ancestor():
    data = {
        "alfa": {
            "bravo": "charlie",
            "delta": {
                "echo": "foxtrot",
                "golf": "hotel"
            },
            "india": "juliet",
            "kilo": {
                "echo": "lima",
            }
        },
        "kilo": {
            "echo": "mike"
        }
    }
    c = ctx(data)

    an = patterns.Ancestor(
        patterns.Lookup("alfa"),
        patterns.Lookup("echo")
    )
    assert sorted(an.pull(None, data)) == ["foxtrot", "lima"]

    assert an.matches(c, data["alfa"]["delta"]["echo"])
    assert an.matches(c, data["alfa"]["kilo"]["echo"])
    assert not an.matches(c, data["kilo"]["echo"])


def test_combine():
    data = {"type": "root", "attrs": {"type": "node", "context": "sop"}, "body": [
        {"type": "h", "level": 1, "text": ["Hello ", "there"]},
        {"type": "summary", "text": ["This is the summary"]},
        {"type": "para", "attrs": {"id": "foo"}, "text": ["This is a test"]},
        {"type": "h", "level": 2, "text": ["First heading"]},
        {"type": "para", "text": ["Foo bar."]}
    ]}
    c = ctx(data)

    p1 = patterns.Lookup("body")
    assert list(p1.pull(None, data)) == [data["body"]]

    p = patterns.Child(
        p1,
        patterns.Comparison("level", ">", 1)
    )
    assert list(p.pull(None, data)) == [data["body"][3]]

    assert not p.matches(c, data["body"][0])
    assert p.matches(c, data["body"][3])


def test_string_function():
    ls = ["01", "11"]
    assert functions.string(ls) == "0111"


def test_apply():
    from bookish.functions import functions_dict

    data = [
        {"x": "00"},
        {"x": "01"},
        {"x": "10"},
        {"x": "11"},
    ]

    p = patterns.Comparison("x", "=~", ".1")
    a = patterns.App("first", [p])
    assert list(a.pull(functions_dict, data)) == [{"x": "01"}]

    a = patterns.App("last", [p])
    assert list(a.pull(functions_dict, data)) == [{"x": "11"}]
