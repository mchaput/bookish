import os.path
from textwrap import dedent

import nose.tools

from bookish import pipeline, stores, util
from bookish.wikipages import WikiPages


def common_store():
    dirname = os.path.dirname(__file__)
    return stores.FileStore(os.path.join(dirname, "../bookish"))


def snippet(text):
    if text.startswith("\n"):
        text = text[1:]
    text = dedent(text.rstrip())
    return (text + "\n").encode("utf8")


def test_snippet():
    doc1 = snippet("""
    = Title =

    Foo.
    """)
    assert doc1 == b"= Title =\n\nFoo.\n"


def test_simple_include():
    doc1 = b"Para 1.\n\n[Include:b]\n\nPara 2.\n"
    doc2 = b"Foo.\n\nBar.\n"
    ds = stores.DictionaryStore({"/a.txt": doc1, "/b.txt": doc2})
    s = stores.OverlayStore(ds, common_store())
    wp = WikiPages(s, None, caching=False)

    data = wp.json("/a.txt")
    # util.dump_tree(data)
    assert data == {
        "type": "root", "attrs": {}, "included": ["/b.txt"], "parents": [],
        "body": [
            {"type": "para", "text": ["Para 1."], "indent": 0},
            {"type": "para", "text": ["Foo."], "indent": 0},
            {"type": "para", "text": ["Bar."], "indent": 0},
            {"type": "para", "text": ["Para 2."], "indent": 0},
        ]
    }


def test_circular_include():
    doc1 = b"Para 1.\n\n[Include:b]\n\nPara 2.\n"
    doc2 = b"Foo.\n\n[Include:a]\n\nBar.\n"
    ds = stores.DictionaryStore({"/a.txt": doc1, "/b.txt": doc2})
    s = stores.OverlayStore(ds, common_store())
    wp = WikiPages(s, None, caching=False)
    with nose.tools.assert_raises(pipeline.CircularIncludeError):
        wp.json("/a.txt")


def test_include_id():
    doc1 = snippet("""
    == H1 ==

    Foo.

    [Include:b#y]

    Bar.

    == H2 ==

    Baz.
    """)
    doc2 = snippet("""
    == Alfa == (x)

    Apple

    == Bravo == (y)

    Book.

    == Charlie == (z)

    Copter.
    """)

    ds = stores.DictionaryStore({"/a.txt": doc1, "/b.txt": doc2})
    s = stores.OverlayStore(ds, common_store())
    wp = WikiPages(s, None, caching=False)

    data = wp.json("/a.txt")
    # util.dump_tree(data)
    assert data["type"] == "root"
    assert data["included"] == ["/b.txt"]

    assert len(data["body"]) == 2
    h1, h2 = data["body"]

    assert h1["type"] == "h"
    assert h1["text"] == ["H1"]
    assert h1["level"] == 2
    assert len(h1["body"]) == 3
    h11, h12, h13 = h1["body"]

    assert h11["type"] == "para"
    assert h11["text"] == ["Foo."]
    assert h12["type"] == "h"
    assert h12["text"] == ["Bravo"]
    assert h12["id"] == "y"
    assert h12["level"] == 3
    assert len(h12["body"]) == 1
    assert h12["body"][0]["text"] == ["Book."]
    assert h13["type"] == "para"
    assert h13["text"] == ["Bar."]

    assert h2["type"] == "h"
    assert h2["text"] == ["H2"]
    assert h2["level"] == 2


def test_double_include():
    doc1 = snippet("""
    [Include:b]
    """)
    doc2 = snippet("""
    [Include:c]
    """)
    doc3 = snippet("""
    Hi there.
    """)
    ds = stores.DictionaryStore({
        "/a.txt": doc1,
        "/b.txt": doc2,
        "/c.txt": doc3
    })
    s = stores.OverlayStore(ds, common_store())
    wp = WikiPages(s, None, caching=False)

    data = wp.json("/a.txt")
    # util.dump_tree(data)
    assert data == {
        "type": "root", "attrs": {}, "included": ["/b.txt", "/c.txt"],
        "parents": [], "body": [
            {"type": "para", "indent": 0, "text": ["Hi there."]},
        ]
    }


def test_missing_include():
    doc1 = snippet("""
    [Include:b]
    """)

    ds = stores.DictionaryStore({
        "/a.txt": doc1,
    })
    s = stores.OverlayStore(ds, common_store())
    wp = WikiPages(s, None, caching=False)

    data = wp.json("/a.txt")
    util.dump_tree(data)
    assert data == {
        "type": "root", "included": ["/b.txt"], "attrs": {}, "parents": [],
        "body": []
    }
