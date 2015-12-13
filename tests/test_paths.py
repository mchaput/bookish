import nose.tools

from bookish import paths


def test_normalize():
    assert paths.normalize("/") == "/"
    assert paths.normalize("/a/../") == "/"
    assert paths.normalize("/a/b/c") == "/a/b/c"
    assert paths.normalize("/a/b/c/") == "/a/b/c/"
    assert paths.normalize("/a/b/../c") == "/a/c"
    assert paths.normalize("/a/b/../c/") == "/a/c/"
    assert paths.normalize("/.") == "/"
    assert paths.normalize("/./") == "/"
    assert paths.normalize("/a/.") == "/a/"
    assert paths.normalize("/a/b/./c") == "/a/b/c"
    assert paths.normalize("/a/b/./c/") == "/a/b/c/"

    assert paths.normalize("/a/b//c") == "/a/b/c"
    assert paths.normalize("//a/b//c") == "/a/b/c"
    assert paths.normalize("//a/b//c//") == "/a/b/c/"

    with nose.tools.assert_raises(ValueError):
        _ = paths.normalize_abs("")
    with nose.tools.assert_raises(ValueError):
        _ = paths.normalize_abs("a/b/c")

    assert paths.normalize("/../a") == "/a"
    assert paths.normalize("/a/b/../../..") == "/"


def test_parts():
    parts = paths.norm_parts("/a/b/c")
    assert len(parts) == 4
    assert parts[0] == "/"
    assert parts[1] == "a/"
    assert parts[2] == "b/"
    assert parts[3] == "c"

    parts = paths.norm_parts("/a/b/")
    assert len(parts) == 3
    assert parts[0] == "/"
    assert parts[1] == "a/"
    assert parts[2] == "b/"


def test_parent():
    assert paths.parent("/") == "/"
    assert paths.parent("a") == ""
    assert paths.parent("a/b") == ""
    assert paths.parent("/a/b") == "/"
    assert paths.parent("/a/b/") == "/a/"
    assert paths.parent("/a") == "/"
    assert paths.parent("/a/") == "/"

    assert paths.parent("/a/b/c/..") == "/a/"


def test_directory():
    assert paths.directory("/") == "/"
    assert paths.directory("/a/b/") == "/a/b/"
    assert paths.directory("/a/b/c") == "/a/b/"

    assert paths.directory("a") == ""
    assert paths.directory("a/b") == "a/"


def test_join():
    assert paths.join("a", "b") == "b"
    assert paths.join("/a", "/b") == "/b"
    assert paths.join("/a/b/c", "../d") == "/a/d"
    assert paths.join("/a/b/c", "./d") == "/a/b/d"


def test_relativize():
    assert paths.relativize("/", "a") == "a"
    assert paths.relativize("/a/b", "/a/c") == "c"
    assert paths.relativize("/a/b/c", "/a/d") == "../d"
    assert paths.relativize("/a/b/c/", "/a/b/c/d") == "d"
    assert paths.relativize("/a/b/c", "/a/b/d/e") == "d/e"
    assert paths.relativize("/a/b/c", "/d/e/f") == "../../d/e/f"

    assert paths.relativize("/a/b/c", "./d") == "d"

    assert paths.relativize("/credts", "/index") == "index"


def test_basename():
    assert paths.basename("") == ""
    assert paths.basename("/") == ""
    assert paths.basename("/a") == "a"
    assert paths.basename("/a/") == ""
    assert paths.basename("/a/b") == "b"


def test_extension():
    assert paths.extension("") == ""
    assert paths.extension("/") == ""
    assert paths.extension("/a") == ""
    assert paths.extension("/a/b") == ""
    assert paths.extension("/a/b.") == "."
    assert paths.extension("/a/b.c") == ".c"
    assert paths.extension("/a/b.txt") == ".txt"
    assert paths.extension("/a/b.abcdefghijklmnop") == ".abcdefghijklmnop"
    assert paths.extension("/a/b.ABCDEFGHIJKLM") == ".ABCDEFGHIJKLM"
    assert paths.extension("/a/b.c/") == ""


def test_splitext():
    assert paths.split_extension("") == ("", "")
    assert paths.split_extension("/") == ("", "")
    assert paths.split_extension("/a") == ("a", "")
    assert paths.split_extension("/a/b") == ("b", "")
    assert paths.split_extension("/a/b.") == ("b", "")
    assert paths.split_extension("/a/b.c") == ("b", "c")
    assert paths.split_extension("/a/b.txt") == ("b", "txt")
    assert paths.split_extension("/a/b.abcdef") == ("b", "abcdef")
    assert paths.split_extension("/a/b.ABCDEF") == ("b", "ABCDEF")
    assert paths.split_extension("/a/b.c/") == ("", "")



