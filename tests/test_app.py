import jinja2

from bookish import pipeline, stores, util, wikipages


def test_parent_links():
    doc1 = b"""
= Doc 1 =

@subtopics

:: [foo]
:: [bar]
"""

    doc2 = b"""
= Doc 2 =
#parent: /

Hi there.
"""

    st = stores.DictionaryStore({
        "/_index.txt": doc1,
        "/baz/boo.txt": doc2
    })

    env = jinja2.Environment()
    wp = wikipages.WikiPages(st, env, caching=False)

    root = wp.json("/baz/boo.txt")
    parents = root["parents"]
    assert len(parents) == 1
    parent = parents[0]
    assert parent["path"] == "/_index.txt"
    assert parent["basepath"] == "/_index"
    assert parent["summary"] is None
    assert parent["title"] == ["Doc 1"]
