import os.path
from datetime import datetime
from zipfile import ZipFile

import nose.tools

from bookish import stores
from bookish.util import TempDir


def test_filestore():
    with TempDir() as dirpath:
        s = stores.FileStore(dirpath)

        assert s.file_path("/b") == os.path.join(dirpath, "b")
        with nose.tools.assert_raises(ValueError):
            _ = s.exists("a")
        assert not s.exists("/a")
        assert not s.exists("/b")

        content = b"Hello there"
        writetime = datetime.utcnow().replace(microsecond=0)
        with s.open("/b", "wb") as f:
            f.write(content)

        assert not s.exists("/a")
        assert s.exists("/b")

        assert s.content("/b") == content.decode("utf8")
        assert s.size("/b") == len(content)

        delta = s.last_modified("/b") - writetime
        assert 0 <= delta.total_seconds() < 1

        assert s.list_dir("/") == ["b"]
        assert s.is_dir("/")
        assert not s.is_dir("/b")

        s.make_dir("/a")
        content2 = b"foo bar baz"
        with s.open("/a/c", "wb") as f:
            f.write(content2)

        assert s.exists("/a")
        assert s.exists("/b")
        assert s.exists("/a/c")
        assert s.content("/a/c", None) == content2
        assert s.size("/a/c") == len(content2)

        delta = s.last_modified("/a/c") - s.last_modified("/b")
        assert 0 <= delta.total_seconds() < 1

        assert s.is_dir("/a")
        assert not s.is_dir("/a/c")


def test_zipstore():
    with TempDir() as dirpath:
        contents = {
            "a.txt": "alfa",
            "bad": "wolf",
            "b/b.txt": "bravo",
            "b/c.txt": "charlie",
            "d.txt": "delta",
        }

        zippath = os.path.join(dirpath, "x.zip")
        zf = ZipFile(zippath, "w")
        writetime = datetime.utcnow()
        for name, content in contents.items():
            zf.writestr(name, content)
        zf.close()

        assert os.path.exists(zippath)
        zs = stores.ZipStore(zippath)
        assert zs.exists("/a.txt")
        assert not zs.exists("/b.txt")
        assert zs.exists("/b/b.txt")

        assert zs.list_dir("/") == ["a.txt", "b", "bad", "d.txt"]
        assert zs.list_dir("/b/") == ["b.txt", "c.txt"]

        delta = zs.last_modified("/b/b.txt") - writetime
        assert delta.total_seconds() <= 1

        assert not zs.is_dir("/a.txt")
        assert zs.is_dir("/b")
        assert not zs.is_dir("/d")

        assert zs.size("/bad") == 4
        assert zs.size("/b/c.txt") == 7

        assert zs.content("/b/c.txt") == "charlie"
        zs.close()


def test_missing():
    with TempDir() as dirpath:
        store = stores.FileStore(dirpath)
        assert not store.exists("/a.txt")
        with nose.tools.assert_raises(stores.ResourceNotFoundError):
            store.last_modified("/a.txt")
