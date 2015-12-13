import nose.tools

from bookish import pipeline as p


def test_pipe():
    class TestProcessor(p.Processor):
        def __init__(self, name):
            self.name = name

        def apply(self, block, context):
            block["x"].append(self.name)

    a = TestProcessor("a")
    b = TestProcessor("b")
    c = TestProcessor("c")
    d = a | b | c
    assert isinstance(d, p.Pipe)

    top = {"x": []}
    d.apply(top, None)
    assert top == {"x": ["a", "b", "c"]}


def test_hierarchy():
    top = {"type": "root", "body": [
        {"name": "a", "indent": 0},
        {"name": "b", "indent": 4},
        {"name": "c", "indent": 8},
        {"name": "d", "indent": 4},
        {"name": "e", "indent": 0},
        {"name": "f", "indent": 4},
    ]}

    p.Hierarchy().apply(top, None)
    # dump_tree(top)
    assert top == {"type": "root", "body": [
        {"name": "a", "indent": 0, "body": [
            {"name": "b", "indent": 4, "body": [
                {"name": "c", "indent": 8}
            ]},
            {"name": "d", "indent": 4}
        ]},
        {"name": "e", "indent": 0, "body": [
            {"name": "f", "indent": 4}
        ]}
    ]}


def test_headings():
    top = {"type": "root", "body": [
        {"type": "h", "level": 2, "name": "a", "container": True},
        {"type": "para", "name": "b"},
        {"type": "para", "name": "c"},
        {"type": "h", "level": 3, "name": "d", "container": True},
        {"type": "para", "name": "e"},
        {"type": "h", "level": 2, "name": "f", "container": True},
        {"type": "para", "name": "g"},
    ]}

    p.SortHeadings().apply(top, None)
    # util.dump_tree(top)
    assert top == {"type": "root", "body": [
        {"type": "h", "level": 2, "name": "a", "container": True, "body": [
            {"type": "para", "name": "b"},
            {"type": "para", "name": "c"},
            {"type": "h", "level": 3, "name": "d", "container": True, "body": [
                {"type": "para", "name": "e"},
            ]},
        ]},
        {"type": "h", "level": 2, "name": "f", "container": True, "body": [
            {"type": "para", "name": "g"},
        ]},
    ]}


def test_properties():
    top = {"type": "root", "body": [
        {"type": "prop", "name": "x", "value": "foo"},
        {"type": "para", "body": [
            {"type": "prop", "name": "y", "value": "bar"}
        ]},
        {"type": "prop", "name": "z", "value": "baz"}
    ]}

    p.Properties().apply(top, None)
    # util.dump_tree(top)
    assert top == {"type": "root", "attrs": {"x": "foo", "z": "baz"}, "body": [
        {"type": "para", "attrs": {"y": "bar"}, "body": []}
    ]}


def test_emptyblocks():
    top = {"type": "root", "body": [
        {"type": "para"},
        {"type": "para", "body": [
            {"type": "para", "text": ["foo"]},
            {"type": "para", "text": ["bar"]},
            {"type": "para"},
            {"type": "para", "text": ["baz"]},
        ]},
        {"type": "para"},
        {"type": "para", "text": ["pogo"]},
        {"type": "para"},
    ]}

    p.EmptyBlocks().apply(top, None)
    assert top == {"type": "root", "body": [
        {"type": "para", "body": [
            {"type": "para", "text": ["foo"]},
            {"type": "para", "text": ["bar"]},
            {"type": "para", "text": ["baz"]},
        ]},
        {"type": "para", "text": ["pogo"]},
    ]}


def test_jointext():
    top = {"type": "root", "body": [
        {"name": "a", "text": ["foo", "bar", {"type": "x"}]},
        {"name": "b", "text": ["foo", {"type": "x"}, "bar"]},
        {"name": "c", "text": [{"type": "x"}, "foo", "bar"]},
        {"name": "d", "text": [{"type": "x"}, {"type": "y"}, "foo", "bar"]},
        {"name": "e", "text": ["foo", {"type": "x"}, {"type": "y"}, "bar"]},
        {"name": "f", "text": ["foo", "bar", {"type": "x"}, {"type": "y"}]},
    ]}

    p.JoinText().apply(top, None)
    assert top == {"type": "root", "body": [
        {"name": "a", "text": ["foobar", {"type": "x"}]},
        {"name": "b", "text": ["foo", {"type": "x"}, "bar"]},
        {"name": "c", "text": [{"type": "x"}, "foobar"]},
        {"name": "d", "text": [{"type": "x"}, {"type": "y"}, "foobar"]},
        {"name": "e", "text": ["foo", {"type": "x"}, {"type": "y"}, "bar"]},
        {"name": "f", "text": ["foobar", {"type": "x"}, {"type": "y"}]},
    ]}


def test_groups():
    top = {"type": "root", "body": [
        {"type": "dt", "text": ["alfa"], "indent": 0},
        {"type": "dt", "text": ["bravo"], "indent": 4},
        {"type": "dt", "text": ["charlie"], "indent": 4},
        {"type": "dt", "text": ["delta"], "indent": 0},
        {"type": "dt", "text": ["echo"], "indent": 4},
        {"type": "dt", "text": ["foxtrot"], "indent": 4},
        {"type": "dt", "text": ["golf"], "indent": 0},
    ]}

    pipe = p.Hierarchy() | p.Groups(["dt"])
    pipe.apply(top, {})
    # util.dump_tree(top)
    assert top == {"type": "root", "body": [
        {"type": "dt_group", "container": True, "body": [
            {"type": "dt", "text": ["alfa"], "indent": 0, "body": [
                {"type": "dt_group", "container": True, "body": [
                    {"type": "dt", "text": ["bravo"], "indent": 4},
                    {"type": "dt", "text": ["charlie"], "indent": 4},
                ]}
            ]},
            {"type": "dt", "text": ["delta"], "indent": 0, "body": [
                {"type": "dt_group", "container": True, "body": [
                    {"type": "dt", "text": ["echo"], "indent": 4},
                    {"type": "dt", "text": ["foxtrot"], "indent": 4},
                ]}
            ]},
            {"type": "dt", "text": ["golf"], "indent": 0},
        ]},
    ]}


def test_regroup():
    top = {"type": "root", "body": [
        {"type": "foo", "id": 0},
        {"type": "foo", "id": 1},
        {"type": "foo_group", "container": True, "body": [
            {"type": "foo", "id": 2},
            {"type": "foo", "id": 3},
        ]},
        {"type": "bar_group", "container": True, "body": [
            {"type": "bar", "id": 4},
        ]},
        {"type": "bar", "id": 5},
        {"type": "baz", "id": 6},
        {"type": "baz", "id": 7},
    ]}

    pipe = p.Groups(["foo", "bar"])
    pipe.apply(top, {})
    # util.dump_tree(top)
    assert top == {"type": "root", "body": [
        {"type": "foo_group", "container": True, "body": [
            {"type": "foo", "id": 0},
            {"type": "foo", "id": 1},
            {"type": "foo", "id": 2},
            {"type": "foo", "id": 3},
        ]},
        {"type": "bar_group", "container": True, "body": [
            {"type": "bar", "id": 4},
            {"type": "bar", "id": 5},
        ]},
        {"type": "baz", "id": 6},
        {"type": "baz", "id": 7},
    ]}


def test_headings_and_groups():
    top = {"type": "root", "body": [
        {"type": "h", "level": 2, "text": ["H"], "container": True},
        {"type": "para", "text": ["Alfa"]},
        {"type": "ord", "text": ["Bravo"]},
        {"type": "ord", "text": ["Charlie"]},
        {"type": "para", "text": ["Delta"]},
    ]}
    pipe = p.SortHeadings() | p.Groups(["bullet", "ord", "dt"])
    pipe.apply(top, {})
    assert top == {"type": "root", "body": [
        {"type": "h", "level": 2, "text": ["H"], "container": True, "body": [
            {"type": "para", "text": ["Alfa"]},
            {"type": "ord_group", "container": True, "body": [
                {"type": "ord", "text": ["Bravo"]},
                {"type": "ord", "text": ["Charlie"]},
            ]},
            {"type": "para", "text": ["Delta"]},
        ]}
    ]}


def test_promote():
    top = {"type": "root", "body": [
        {"type": "para", "text": ["alfa"]},
        {"type": "bullet", "text": [
            {"type": "link", "scheme": "Include", "value": "/foo"}
        ], "body": [
            {"type": "para", "text": ["Foo!"]}
        ]},
        {"type": "para", "text": ["bravo"]},
    ]}

    p.Promote().apply(top, None)
    assert top == {"type": "root", "body": [
        {"type": "para", "text": ["alfa"]},
        {"type": "link", "scheme": "Include", "value": "/foo", "body": [
            {"type": "para", "text": ["Foo!"]}
        ]},
        {"type": "para", "text": ["bravo"]},
    ]}


def test_section_items():
    top = {
        "type": "root",
        "body": [
            {
                "type": "foo_section", "role": "section", "id": "foo",
                "container": True, "body": [
                    {
                        "type": "item", "role": "item", "text": ["alfa"],
                        "body": [
                            {"type": "para", "text": ["bravo"]}
                        ]
                    }
                ]
            },
            {
                "type": "item", "role": "item", "text": "charlie", "body": [
                    {"type": "para", "text": ["delta"]}
                ]
            }
        ],
    }

    p.Sections().apply(top, None)

    assert top == {
        "type": "root",
        "body": [
            {
                "type": "foo_section", "role": "section", "id": "foo",
                "text": "Foo", "container": True, "body": [
                    {
                        "type": "foo_item", "role": "item", "text": ["alfa"],
                        "body": [
                            {"type": "para", "text": ["bravo"]}
                        ]
                    }
                ]
            },
            {
                "type": "item", "role": "item", "text": "charlie", "body": [
                    {"type": "para", "text": ["delta"]}
                ]
            }
        ],
    }


def test_annotate_fragment():
    from bookish.stores import DictionaryStore
    from bookish.wikipages import WikiPages
    from jinja2 import Environment

    top = {"type": "root", "body": [
        {"type": "para", "text": [
            {"type": "link", "value": "#polygons", "scheme": None, "text": []}
        ]}
    ]}

    path = "/model/primitives.txt"
    st = DictionaryStore({path: top})
    pages = WikiPages(st, Environment())
    ctx = pages.wiki_context(path, conditional=False, save_to_cache=False)

    p.FullPaths().apply(top, ctx)
    p.AnnotateLinks().apply(top, ctx)
    # util.dump_tree(top)
    assert top == {"type": "root", "body": [
        {"type": "para", "text": [
            {
                "type": "link", "value": "#polygons", "scheme": None,
                "text": [], "fullpath": "/model/primitives#polygons",
                "fragment": "#polygons", "exists": True,
            }
        ]}
    ]}


def test_dependencies():
    hier = p.Hierarchy()
    sorth = p.SortHeadings()
    props = p.Properties()
    empt = p.EmptyBlocks()
    prom = p.Promote()

    dg = p.DependencyGraph([hier, sorth, props, empt, prom])
    assert list(dg.resolve()) == [hier, sorth, props, empt, prom]

    dg = p.DependencyGraph([hier, sorth, props, empt, prom])
    # props -> hier -> sorth
    #    \
    #     ---> empt
    # prom
    dg.depends_on(hier, props)
    dg.depends_on(sorth, hier)
    dg.depends_on(empt, props)
    assert list(dg.resolve()) == [props, hier, sorth, empt, prom]

    dg = p.DependencyGraph([hier, sorth, props, empt, prom])
    #             ---> sorth
    #            /
    # props -> empt -> prom -> hier
    #
    dg.depends_on(hier, prom)
    dg.depends_on(sorth, empt)
    dg.depends_on(empt, props)
    dg.depends_on(prom, empt)
    assert list(dg.resolve()) == [props, empt, prom, hier, sorth]

    # dg = p.DependencyGraph([hier, sorth, props, empt])
    # with pytest.raises(ValueError):
    #     dg.depends_on(hier, prom)

    dg = p.DependencyGraph([hier, sorth])
    dg.depends_on(hier, sorth)
    dg.depends_on(sorth, hier)
    with nose.tools.assert_raises(p.CircularDependencyError):
        list(dg.resolve())
