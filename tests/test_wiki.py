import pprint

import nose

import copy
from bookish import parser as p
from bookish import compat, wikipages, util
from bookish.parser import rules


def _metagrammar():
    gstring = util.builtin_grammar("meta.bkgrammar")

    # Use the bootstrap parser to parse the meta grammar
    mg = p.BootGrammar().parse(gstring)
    assert isinstance(mg, p.Grammar)

    # Use the meta-grammar to parse itself
    mg2 = mg.parse(gstring)
    return mg2


def _parse_wiki_grammar(gstring, debug_rule=False):
    mg = _metagrammar()
    if debug_rule:
        mg.context["rule"].debug = True
        mg.context["expr"].debug = True

    wg = mg.parse(gstring)
    if debug_rule:
        mg.context["rule"].debug = True
        mg.context["expr"].debug = False
    wg.snap()
    return wg


def _tx(out, lineno):
    return util.normalize_text("".join(out[lineno]["text"]))


wg = None


def setup_module():
    global wg

    gstring = util.builtin_grammar("wiki.bkgrammar")
    wg = _parse_wiki_grammar(gstring)


def test_title():
    title = wg.ruledict["title"]

    s = p.Document("= This is a title =")
    out, i = title.accept(s, 0, wg.context)
    assert out == {'type': 'title', 'indent': 0, 'level': 0,
                   'text': ['This is a title']}

    s = p.Document("= This is a title =\n\nHi.")
    out, i = title.accept(s, 0, wg.context)
    assert out == {'type': 'title', 'indent': 0, 'level': 0,
                   'text': ['This is a title']}

    s = """= View the scene =

#bestbet: view tumble track dolly pan zoom orbit display

"""
    out, i = title.accept(s, 0, wg.context)
    assert out == {'type': 'title', 'indent': 0, 'level': 0,
                   'text': ['View the scene']}


def test_title2():
    s = "= Crowd simulations ="
    out = wg.parse(s)
    assert out is not p.Miss


def test_titles():
    s = p.Document("= News |> User interface =")

    rule = wg.context["supertitle"]
    out, i = rule.accept(s, 2, wg.context)
    assert out == {"type": "supertitle", "text": ["News"]}

    rule = wg.context["title"]
    out, i = rule.accept(s, 0, wg.context)
    assert out == {"type": "title", "indent": 0, "level": 0, "text": [
        {"type": "supertitle", "text": ["News"]},
        " User interface",
    ]}

    s = p.Document("= Escape to Beer Mountain <| A Rope of Sand =")

    rule = wg.context["subtitle"]
    out, i = rule.accept(s, 26, wg.context)
    assert out == {"type": "subtitle", "text": ["A Rope of Sand"]}

    rule = wg.context["title"]
    out, i = rule.accept(s, 0, wg.context)
    assert out == {"type": "title", "indent": 0, "level": 0, "text": [
        "Escape to Beer Mountain ",
        {"type": "subtitle", "text": ["A Rope of Sand"]},
    ]}

    s = p.Document("= Houdini |> User interface <| An introduction =")
    rule = wg.context["title"]
    out, i = rule.accept(s, 0, wg.context)
    assert out == {"type": "title", "indent": 0, "level": 0, "text": [
        {"type": "supertitle", "text": ["Houdini"]},
        " User interface ",
        {"type": "subtitle", "text": ["An introduction"]},
    ]}


def test_property():
    prop = wg.ruledict["property"]

    s = p.Document("#foo: bar")
    out, i = prop.accept(s, 0, wg.context)
    assert out == {'type': 'prop', 'indent': 0, 'name': 'foo', 'value': 'bar'}

    s = p.Document("#foo: bar\n\nHi.")
    out, i = prop.accept(s, 0, wg.context)
    assert out == {'type': 'prop', 'indent': 0, 'name': 'foo', 'value': 'bar'}


def test_properties():
    prop = wg.ruledict["property"]
    s = """
#alfa: bravo
#charlie: delta
#echo: foxtrot

#india: juliet
    """.strip()

    out, i = prop.accept(s, 0, wg.context)
    assert out is not p.Miss
    assert out["name"] == "alfa"
    assert out["value"] == "bravo"
    assert i == 13

    out, i = prop.accept(s, i, wg.context)
    assert out is not p.Miss
    assert out["name"] == "charlie"
    assert out["value"] == "delta"

    out, i = prop.accept(s, i, wg.context)
    assert out is not p.Miss
    assert out["name"] == "echo"
    assert out["value"] == "foxtrot"

    out, i = prop.accept(s, i, wg.context)
    assert out is not p.Miss
    assert out["name"] == "india"
    assert out["value"] == "juliet"


def test_multiline_property():
    prop = wg.ruledict["property"]
    s = """
    #alfa:
        {
        bravo: "charlie",
        delta: "echo"
        }
    #foxtrot: india
    """

    out, i = prop.accept(s, 0, wg.context)
    assert out is not p.Miss
    assert out["name"] == "alfa"

    v = out["value"].replace(" ", "").replace("\n", "").strip()
    assert v == '{bravo:"charlie",delta:"echo"}'


def test_multiline_empty_property():
    prop = wg.ruledict["property"]
    s = """
#alfa:
    bravo
    charlie
#foxtrot: india
"""

    out, i = prop.accept(s, 0, wg.context)
    assert out is not p.Miss
    assert out["name"] == "alfa"
    assert out["value"] == "    bravo    charlie"


def test_not_multiline():
    prop = wg.ruledict["property"]
    s = """
#alfa: bravo

    charlie
"""

    out, i = prop.accept(s, 0, wg.context)
    assert out is not p.Miss
    assert out["name"] == "alfa"
    assert out["value"] == "bravo"


def test_property_single_line():
    rule = wg.ruledict["blocks"]
    s = """
:list:
    #query: type:vex
    #filter: title tags
"""

    out, i = rule.accept(s, 0, wg.context)
    assert out is not p.Miss
    assert out["type"] == "list"
    assert out["role"] == "item"

    out, i = rule.accept(s, i, wg.context)
    assert out is not p.Miss
    assert out["type"] == "prop"
    assert out["name"] == "query"
    assert out["value"] == "type:vex"

    out, i = rule.accept(s, i, wg.context)
    assert out is not p.Miss
    assert out["type"] == "prop"
    assert out["name"] == "filter"
    assert out["value"] == "title tags"


def test_paras():
    s = """
The Copy node has
two main functions:

* Create multiple copies. You can
  apply transformations.

* Copy the source geometry
  onto the points.

For example, you can arrange copies
in a spherical shape:
    Or you could copy a tree
    model onto a Grid.
When you instance, it
looks for specific attributes.
    """.strip()

    rule = p.Star(wg.context["blocks"])
    # rule = wg.context["grammar"]
    out, i = rule.accept(s, 0, wg.context)
    assert out is not p.Miss
    # pprint.pprint(out)
    assert i == len(s)
    assert len(out) == 6

    assert _tx(out, 0) == "The Copy node has two main functions:"
    assert _tx(out, 1) == "Create multiple copies. You can apply transformations."
    assert _tx(out, 2) == "Copy the source geometry onto the points."
    assert _tx(out, 3) == "For example, you can arrange copies in a spherical shape"
    assert _tx(out, 4) == "Or you could copy a tree model onto a Grid."
    assert _tx(out, 5) == "When you instance, it looks for specific attributes."

    assert [par["indent"] for par in out] == [0, 0, 0, 0, 4, 0]
    assert " ".join([par["type"] for par in out]) == "para bullet bullet dt para para"


def test_empty_para():
    rule = p.Star(wg.context["para"])
    out, i = rule.accept("", 0, wg.context)
    assert out == []


def test_link():
    s = "This has [a link|Node:sop/copy] so there."
    rule = wg.context["para"]
    out, i = rule.accept(s, 0, wg.context)
    assert out is not p.Miss
    # pprint.pprint(out)
    assert out["type"] == "para"
    assert out["text"] == [
        "This has ",
        {"type": "link",
         "text": ["a link"],
         "scheme": "Node",
         "value": "sop/copy"
         },
        " so there."
    ]

    s = "[Image:/images/ui/recook_anno.png]"
    out, i = rule.accept(s, 0, wg.context)
    assert out is not p.Miss
    # print(out)
    assert out["type"] == "para"
    assert out["text"] == [
        {"type": "link",
         "text": "",
         "scheme": "Image",
         "value": "/images/ui/recook_anno.png"}
    ]


def test_em_chars():
    s = "cookbook_files cookbook_files"
    rule = wg.context["para"]
    out, i = rule.accept(s, 0, wg.context)
    assert out is not p.Miss
    assert out == {
        "type": "para", "indent": 0,
        "text": ["cookbook_files cookbook_files"],
    }

    s = "[cookbook_files.tar.gz|../cookbook_files.tar.gz]"
    rule = wg.context["textlink"]
    out, i = rule.accept(s, 0, wg.context)
    assert out is not p.Miss

    s = "_hello_"
    rule = wg.context["em"]
    out, i = rule.accept(s, 0, wg.context)
    assert out is not p.Miss

    s = "_hello__"
    rule = wg.context["para"]
    out, i = rule.accept(s, 0, wg.context)
    assert out is not p.Miss
    assert out == {
        "type": "para", "indent": 0,
        "text": ["_hello__"],
    }

    assert list(wg.context["em"].firsts()) == ["_"]


def test_link_break():
    s = "This has [a link that\n\n never ends|Node:sop/copy] so there."

    rule = wg.context["para"]
    out, i = rule.accept(s, 0, wg.context)
    assert out is not p.Miss
    assert out["type"] == "para"
    assert out["text"] == ["This has [a link that"]


def test_headings():
    s = """
= Title =

Hello there.
== Heading A ==
Hi again.
=== Heading A.a === (tag)

Why not.

== Heading B ==
    """.strip()

    rule = p.Star(wg.context["blocks"])
    out, i = rule.accept(s, 0, wg.context)
    assert out is not p.Miss
    #pprint.pprint(out)
    assert len(out) == 7
    assert _tx(out, 0) == "Title"
    assert _tx(out, 1) == "Hello there."
    assert _tx(out, 2) == "Heading A"
    assert _tx(out, 3) == "Hi again."
    assert _tx(out, 4) == "Heading A.a"
    assert _tx(out, 5) == "Why not."
    assert _tx(out, 6) == "Heading B"


def test_lone_link():
    s = """
[Include:standardvariables]

- [Node:sop/duplicate]
    """.strip()

    rule = p.Star(wg.context["blocks"])
    out, i = rule.accept(s, 0, wg.context)
    assert out is not p.Miss
    #pprint.pprint(out)
    assert out is not p.Miss
    assert out[0]["text"] == [{"scheme": "Include",
                               "text": "",
                               "type": "link",
                               "value": "standardvariables"}]
    assert out[1]["text"] == [{"scheme": "Node",
                               "text": "",
                               "type": "link",
                               "value": "sop/duplicate"}]


def test_1_item():
    s = ":foo:bar:\n"
    rule = wg.context["item"]
    ctx = copy.copy(wg.context)
    ctx.tracing = True
    out, i = rule.accept(s, 0, ctx)
    assert out == {"type": "foo", "role": "item", "text": ["bar"],
                   "indent": 0}


def test_item():
    s = """
Alfa:
    Bravo
:Charlie:Delta:
    Echo
Foxtrot
:Golf::
::Hotel:
    """.strip()

    rule = p.Star(wg.context["blocks"])
    out, i = rule.accept(s, 0, wg.context)
    util.dump_tree(out)
    assert i == len(s)
    assert out == [
        {'indent': 0, 'text': ['Alfa'], 'type': 'dt'},
        {'indent': 4, 'text': ['Bravo'], 'type': 'para'},
        {'indent': 0, 'role': 'item', 'text': ['Delta'], 'type': 'Charlie'},
        {'indent': 4, 'text': ['Echo'], 'type': 'para'},
        {'indent': 0, 'text': ['Foxtrot'], 'type': 'para'},
        {'indent': 0, 'role': 'item', 'type': 'Golf'},
        {'indent': 0, 'role': 'item', 'text': ['Hotel'], 'type': 'item'},
    ]


def test_item2():
    s = """
:foo:
:bar:baz
::qux
    """.strip()

    rule = p.Star(wg.context["blocks"])
    out, i = rule.accept(s, 0, wg.context)
    util.dump_tree(out)
    assert i == len(s)
    assert out == [
        {'indent': 0, 'type': 'foo', 'role': 'item'},
        {'indent': 0, 'type': 'bar', 'role': 'item', 'text': ['baz']},
        {'indent': 0, 'type': 'item', 'role': 'item', 'text': ['qux']},
    ]


def test_code():
    s = "This is a `method()` call."
    rule = wg.context["para"]
    out, i = rule.accept(s, 0, wg.context)
    assert i == len(s)
    # pprint.pprint(out["text"])
    assert out['text'] == [
        'This is a ',
        {'text': ['method()'], 'type': 'code'},
        ' call.'
    ]


def test_code_break():
    s = """
# `openport [-e] [-q]
  <<port_number>>`
"""
    rule = wg.context["blocks"]
    out, i = rule.accept(s, 0, wg.context)
    assert isinstance(out, dict)
    assert out.get("type") == "ord"


def test_pseudoxml():
    s = """
table>>
    tr>>
        td width="50%">>Hi
        td bgcolor="red">>
            This is the end
    tr>>
        td>>
            My only friend
        td>>the end
    """.strip()

    rule = p.Star(wg.context["blocks"])
    out, i = rule.accept(s, 0, wg.context)
    #pprint.pprint(out)
    assert i == len(s)
    assert out == [
        {'attrs': {}, 'indent': 0, 'tag': 'table', 'type': 'pxml'},
        {'attrs': {}, 'indent': 4, 'tag': 'tr', 'type': 'pxml'},
        {'attrs': {'width': '50%'},
         'indent': 8,
         'tag': 'td',
         'text': ['Hi'],
         'type': 'pxml'},
        {'attrs': {'bgcolor': 'red'},
         'indent': 8,
         'tag': 'td',
         'type': 'pxml'},
        {'indent': 12, 'text': ['This is the end'], 'type': 'para'},
        {'attrs': {}, 'indent': 4, 'tag': 'tr', 'type': 'pxml'},
        {'attrs': {}, 'indent': 8, 'tag': 'td', 'type': 'pxml'},
        {'indent': 12, 'text': ['My only friend'], 'type': 'para'},
        {'attrs': {}, 'indent': 8, 'tag': 'td', 'text': ['the end'], 'type': 'pxml'}
    ]


def test_xml():
    s = """
This is a <span style="text-decoration: strikethrough">good idea</span>.
    """.strip()

    rule = wg.context["para"]
    out, i = rule.accept(s, 0, wg.context)
    # pprint.pprint(out)
    assert i == len(s)
    assert out == {
        'type': 'para',
        'indent': 0,
        'text': ['This is a ',
                 {'attrs': {'style': 'text-decoration: strikethrough'},
                  'tag': 'span',
                  'text': ['good idea'],
                  'type': 'xml'},
                 '.'],
    }


def test_html():
    s = """
<img name="ui" src="/images/ui/ui_imagemap.png" width="450" height="275" border="0" id="ui_imagemap" usemap="#m_ui_imagemap" alt="" />
    """.strip()

    rule = wg.context["xml"]
    out, i = rule.accept(s, 0, wg.context)
    assert out is not p.Miss
    assert i == len(s)


def test_spans():
    s = """
If _you_ want to *come down [here|http://canada.ca]* and talk about <<thing>>
you need to call `here()` in the __Blah__ menu.
    """.strip()

    rule = wg.context["blocks"]
    out, i = rule.accept(s, 0, wg.context)
    #pprint.pprint(out)
    assert i == len(s)
    assert out == {
        'type': 'para',
        'indent': 0,
        'text': [
            'If ',
            {'text': ['you'], 'type': 'em'},
            ' want to ',
            {'text': ['come down ',
                      {'scheme': None,
                       'text': ['here'],
                       'type': 'link',
                       'value': 'http://canada.ca'}],
             'type': 'strong'},
            ' and talk about ',
            {'text': ['thing'], 'type': 'var'},
            '\nyou need to call ',
            {'text': ['here()'], 'type': 'code'},
            ' in the ',
            {'text': ['Blah'], 'type': 'ui'},
            ' menu.'],
    }


def test_split_span():
    s = """
Alfa bravo *charlie delta
echo foxtrot* golf hotel
""".lstrip()
    blocks = wg.parse(s)
    text = blocks[0]["text"]
    assert text == [
        "Alfa bravo ",
        {"type": "strong", "text": ["charlie delta\necho foxtrot"]},
        " golf hotel"
    ]


def test_bullet_indent():
    s = """
* Item 1
    * Item 1.1
    * Item 1.2
    """.strip()

    rule = p.Star(wg.context["blocks"])
    out, i = rule.accept(s, 0, wg.context)
    # pprint.pprint(out)
    assert i == len(s)
    assert out == [
        {'indent': 0, 'text': ['Item 1'], 'type': 'bullet', 'blevel': 2},
        {'indent': 4, 'text': ['Item 1.1'], 'type': 'bullet', 'blevel': 6},
        {'indent': 4, 'text': ['Item 1.2'], 'type': 'bullet', 'blevel': 6},
    ]


def test_bullets():
    s = """
* Item 1
* Item 2
    - Item 2.1
    - Item 2.2

        Sub paragraph 2.2.1
    - Item 2.3
- Item 3

    Sub paragraph 3.1

** Item 3.2
--- Item 3.2.1
* Item 4
    """.strip()

    rule = p.Star(wg.context["blocks"])
    out, i = rule.accept(s, 0, wg.context)
    # pprint.pprint(out)
    assert i == len(s)
    assert out == [
        {'indent': 0, 'text': ['Item 1'], 'type': 'bullet', 'blevel': 2},
        {'indent': 0, 'text': ['Item 2'], 'type': 'bullet', 'blevel': 2},
        {'indent': 4, 'text': ['Item 2.1'], 'type': 'bullet', 'blevel': 6},
        {'indent': 4, 'text': ['Item 2.2'], 'type': 'bullet', 'blevel': 6},
        {'indent': 8, 'text': ['Sub paragraph 2.2.1'], 'type': 'para'},
        {'indent': 4, 'text': ['Item 2.3'], 'type': 'bullet', 'blevel': 6},
        {'indent': 0, 'text': ['Item 3'], 'type': 'bullet', 'blevel': 2},
        {'indent': 4, 'text': ['Sub paragraph 3.1'], 'type': 'para'},
        {'indent': 0, 'text': ['Item 3.2'], 'type': 'bullet', 'blevel': 3},
        {'indent': 0, 'text': ['Item 3.2.1'], 'type': 'bullet', 'blevel': 4},
        {'indent': 0, 'text': ['Item 4'], 'type': 'bullet', 'blevel': 2}
    ]


def test_dash_bullet():
    s = """
The following details are important to note:

- `bool` parameter types are only
  supported in Python 2.6 and up.
""".lstrip()

    out = wg.parse(s)
    assert out[1]["text"] == [
        {"type": "code", "text": ["bool"]},
        " parameter types are only\n  supported in Python 2.6 and up."
    ]


def test_ords():
    s = """
# Item 1
# Item 2
    # Item 2.1
    # Item 2.2

        Sub paragraph 2.2.1
    # Item 2.3
# Item 3

    Sub paragraph 3.1

## Item 3.2
### Item 3.2.1
# Item 4
    """.strip()

    rule = p.Star(wg.context["blocks"])
    out, i = rule.accept(s, 0, wg.context)
    # pprint.pprint(out)
    assert i == len(s)
    assert out == [
        {'indent': 0, 'text': ['Item 1'], 'type': 'ord', 'blevel': 2},
        {'indent': 0, 'text': ['Item 2'], 'type': 'ord', 'blevel': 2},
        {'indent': 4, 'text': ['Item 2.1'], 'type': 'ord', 'blevel': 6},
        {'indent': 4, 'text': ['Item 2.2'], 'type': 'ord', 'blevel': 6},
        {'indent': 8, 'text': ['Sub paragraph 2.2.1'], 'type': 'para'},
        {'indent': 4, 'text': ['Item 2.3'], 'type': 'ord', 'blevel': 6},
        {'indent': 0, 'text': ['Item 3'], 'type': 'ord', 'blevel': 2},
        {'indent': 4, 'text': ['Sub paragraph 3.1'], 'type': 'para'},
        {'indent': 0, 'text': ['Item 3.2'], 'type': 'ord', 'blevel': 3},
        {'indent': 0, 'text': ['Item 3.2.1'], 'type': 'ord', 'blevel': 4},
        {'indent': 0, 'text': ['Item 4'], 'type': 'ord', 'blevel': 2}
    ]


def test_section():
    s = """
= Title =

== H 1 ==

@alfa

== H 2 ==

@bravo
    """.strip()

    rule = p.Star(wg.context["blocks"])
    out, i = rule.accept(s, 0, wg.context)
    # pprint.pprint(out)
    assert i == len(s)
    util.dump_tree(out)
    assert out == [
        {'indent': 0, 'level': 0, 'text': ['Title'], 'type': 'title'},
        {'indent': 0, 'container': True, 'level': 2, 'text': ['H 1'], 'type': 'h', 'id': None},
        {'indent': 0, 'container': True, 'type': 'alfa_section', 'level': 1, 'role': 'section', 'id': 'alfa'},
        {'indent': 0, 'container': True, 'level': 2, 'text': ['H 2'], 'type': 'h', 'id': None},
        {'indent': 0, 'container': True, 'type': 'bravo_section', 'level': 1, 'role': 'section', 'id': 'bravo'}
    ]


def test_codeblock():
    s = """
Alfa

{{{
#!python
a == 2
}}}

Bravo
    """.strip()

    rule = p.Star(wg.context["blocks"])
    out, i = rule.accept(s, 0, wg.context)
    #pprint.pprint(out)
    assert i == len(s)
    assert out == [
        {'indent': 0, 'text': ['Alfa'], 'type': 'para'},
        {'indent': 0, 'text': ['\na == 2\n'], 'type': 'pre', 'lang': 'python'},
        {'indent': 0, 'text': ['Bravo'], 'type': 'para'}
    ]

    s = """
Alfa
{{{
#!python
a == 2
}}}
Bravo
    """.strip()

    rule = p.Star(wg.context["blocks"])
    out, i = rule.accept(s, 0, wg.context)
    #pprint.pprint(out)
    assert i == len(s)
    assert out == [
        {'indent': 0, 'text': ['Alfa'], 'type': 'para'},
        {'indent': 0, 'text': ['\na == 2\n'], 'type': 'pre', 'lang': 'python'},
        {'indent': 0, 'text': ['Bravo'], 'type': 'para'}
    ]


def test_nolang_codeblock():
    s = """
Alfa

{{{
a == 2
}}}

Bravo
    """.strip()

    rule = p.Star(wg.context["blocks"])
    out, i = rule.accept(s, 0, wg.context)
    #pprint.pprint(out)
    assert i == len(s)
    assert out == [
        {'indent': 0, 'text': ['Alfa'], 'type': 'para'},
        {'indent': 0, 'text': ['\na == 2\n'], 'type': 'pre', 'lang': None},
        {'indent': 0, 'text': ['Bravo'], 'type': 'para'}
    ]


def test_entity():
    sigma = compat.unichr(963)

    rule = wg.context["entity"]
    out, i = rule.accept("&sigma;", 0, wg.context)
    assert out == sigma

    rule = wg.context["entity"]
    out, i = rule.accept("&#963;", 0, wg.context)
    assert out == sigma

    rule = wg.context["entity"]
    out, i = rule.accept("&#x3c3;", 0, wg.context)
    assert out == sigma


def test_embedded_entity():
    rule = wg.context["blocks"]
    s = "(&sigma;<sup>2</sup>)"
    out, i = rule.accept(s, 0, wg.context)
    assert out is not p.Miss
    assert out["text"] == [
        "(",
        compat.unichr(963),
        {"type": "xml", "tag": "sup", "attrs": {}, "text": [
            "2"
        ]},
        ")"
    ]


def test_keyname():
    s = "foo"
    rule = wg.context["keyname"]
    out, i = rule.accept(s, 0, wg.context)
    assert out == "foo"

    s = "foo bar"
    rule = wg.context["keyname"]
    out, i = rule.accept(s, 0, wg.context)
    assert out == "foo"

    s = "foo bar"
    rule = wg.context["keyname"]
    out, i = rule.accept(s, 0, wg.context)
    assert out == "foo"

    s = "'"
    rule = wg.context["keyname"]
    out, i = rule.accept(s, 0, wg.context)
    assert out == "'"

    s = "["
    rule = wg.context["keyname"]
    out, i = rule.accept(s, 0, wg.context)
    assert out == "["

    s = "Esc"
    rule = wg.context["keyname"]
    out, i = rule.accept(s, 0, wg.context)
    assert out == "Esc"


def test_keys():
    s = "((Esc))"
    rule = wg.context["keys"]
    out, i = rule.accept(s, 0, wg.context)
    assert out == {"type": "keys", "keys": ["Esc"], "text": None}

    s = "(( ) ))"
    out, i = rule.accept(s, 0, wg.context)
    assert out == {"type": "keys", "keys": [")"], "text": None}


def test_keys2():
    s = """
    Press ((Esc)) or ((Shift + Enter)) to finish.
    """.strip()

    rule = wg.context["para"]
    out, i = rule.accept(s, 0, wg.context)
    # pprint.pprint(out)
    assert out is not p.Miss
    assert out == {
        'type': 'para',
        'indent': 0,
        'text': [
            'Press ',
            {'text': None, 'type': 'keys', 'keys': ['Esc']},
            ' or ',
            {'text': None, 'type': 'keys', 'keys': ['Shift', 'Enter']},
            ' to finish.',
        ]
    }


def test_key_parens():
    # Make sure you can put key markup (e.g. "((Q))") inside parentheses.

    s = "Jump key (((MMB)))"
    rule = wg.context["para"]
    out, i = rule.accept(s, 0, wg.context)
    assert out == {"type": "para", "indent": 0, "text": [
        "Jump key (", {"type": "keys", "keys": ["MMB"], "text": None}, ")"
    ]}

    s = "Jump key ((( ( )))"
    rule = wg.context["para"]
    out, i = rule.accept(s, 0, wg.context)
    assert out == {"type": "para", "indent": 0, "text": [
        "Jump key (", {"type": "keys", "keys": ["("], "text": None}, ")"
    ]}


def test_plus_key():
    s = "a ((+)) b"
    rule = wg.context["para"]
    out, i = rule.accept(s, 0, wg.context)
    assert out == {"type": "para", "indent": 0, "text": [
        "a ", {"type": "keys", "keys": ["+"], "text": None}, " b"
    ]}


def test_note():
    s = """
You can convert types.

TIP:
    Press MMB.
"""
    out = wg.parse(s)
    assert out == [
        {"type": "para", "indent": 0,
         "text": ["You can convert types."]},
        {"type": "tip", "role": "item", "indent": 0},
        {"type": "para", "indent": 4, "text": ["Press MMB."]},
    ]


def test_mult():
    s = "1024x768"
    rule = wg.context["mult"]
    out, i = rule.accept(s, 4, wg.context)
    assert out == compat.unichr(215)

    s = "Up to 3x faster"
    rule = wg.context["mult"]
    out, i = rule.accept(s, 7, wg.context)
    assert out == compat.unichr(215)

    s = "Up to 3x faster"
    rule = wg.context["para"]
    out, i = rule.accept(s, 0, wg.context)
    assert out == {
        "type": "para", "indent": 0,
        "text": [u"Up to 3", u"\u00d7", u" faster"]
    }

    from bookish.grammars.wiki import mult, para
    from bookish.parser import condition_string
    from bookish.parser.bootstrap import bootstrap_context

    s = condition_string(s)
    ctx = bootstrap_context()

    out, i = mult(s, 7, ctx)
    assert out is not p.Miss
    assert out == compat.unichr(215)

    out, i = para(s, 0, ctx)
    assert out == {
        "type": "para", "indent": 0,
        "text": [u"Up to 3", u"\u00d7", u" faster"]
    }


def test_glyph():
    s = "This is a +(fa-beer) day"
    rule = wg.context["glyph"]
    out, i = rule.accept(s, 10, wg.context)
    span = {"type": "link", "scheme": "Glyph", "text": None, "value": "fa-beer"}
    assert out == span

    rule = wg.context["para"]
    out, i = rule.accept(s, 0, wg.context)
    assert out == {"type": "para", "indent": 0, "text": [
        "This is a ",
        span,
        " day"
    ]}


def test_divider():
    rule = wg.context["divider"]
    out, i = rule.accept("~~", 0, wg.context)
    assert out is not p.Miss
    assert out["type"] == "divider"
    assert out["indent"] == 0

    out, i = rule.accept("\n\n  ~~\n", 0, wg.context)
    assert out is not p.Miss
    assert out["type"] == "divider"
    assert out["indent"] == 2


def test_titled_sep():
    rule = wg.context["sep"]

    s = """
Hello there
~~~~~~
This is a thing
""".strip()
    out, i = wg.context["grammar"].accept(s, 0, wg.context)
    assert len(out) == 3
    assert out[0]["type"] == "para"
    assert out[1]["type"] == "sep"
    assert out[2]["type"] == "para"

    out, i = rule.accept("~~~ ~~~", 0, wg.context)
    assert out is not p.Miss
    assert out["type"] == "sep"
    assert out["indent"] == 0

    s = """
= Hello there =

    ~~ foobar ~~

This is a thing
""".strip()
    out, i = wg.context["grammar"].accept(s, 0, wg.context)
    assert len(out) == 3
    assert out[0]["type"] == "title"
    assert out[1]["type"] == "sep"
    assert out[1]["text"] == [" foobar "]
    assert out[1]["indent"] == 4
    assert out[1]["level"] == 2
    assert out[2]["type"] == "para"


def test_firsts():
    hc = rules.Match("<")
    lc = rules.Seq([
        rules.linestart,
        rules.Star(" "),
        rules.Match("/"),
    ])
    c = rules.Or([hc, lc])

    fsts = c.firsts()
    assert fsts is not None
    assert sorted(fsts) == [" ", "/", "<"]





