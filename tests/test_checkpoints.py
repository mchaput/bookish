import datetime, time

from bookish import checkpoints, stores
from bookish.util import TempDir


def test_autosave():
    with TempDir() as dirpath:
        s = stores.FileStore(dirpath)
        c = checkpoints.Checkpoints("matt", s, s)
        s.make_dir("/a/b/")
        assert s.exists("/a/b")
        path = "/a/b/c.txt"
        
        assert not c.has_autosave(path)
        assert c.get_autosave(path) is None

        content = "alfa bravo"
        c.autosave(path, content)
        assert c.has_autosave(path)
        assert c.get_autosave(path) == content

        c2 = checkpoints.Checkpoints("ryan", s, s)
        assert not c2.has_autosave(path)
        assert c2.get_autosave(path) is None


def test_checkpoints():
    with TempDir() as dirpath:
        s = stores.FileStore(dirpath)
        c = checkpoints.Checkpoints("matt", s, s)
        s.make_dir("/a/b/")
        assert s.exists("/a/b")
        path = "/a/b/c.txt"

        assert c.checkpoints(path) == []
        c.save_checkpoint(path, "alfa bravo")
        time.sleep(1)
        c.save_checkpoint(path, "alfa bravo charlie")
        checks = c.checkpoints(path)
        assert len(checks) == 2
        assert c.get_checkpoint(path, checks[0]["id"]) == "alfa bravo"
        assert c.get_checkpoint(path, checks[1]["id"]) == "alfa bravo charlie"

        c2 = checkpoints.Checkpoints("ryan", s, s)
        assert c2.checkpoints(path) == []
        c2.save_checkpoint(path, "delta echo")
        checks = c2.checkpoints(path)
        assert len(checks) == 1
        print("checks=", checks)
        assert c2.get_checkpoint(path, checks[0]["id"]) == "delta echo"

        path2 = "/a/b/d.txt"
        assert c.checkpoints(path2) == []
        assert c2.checkpoints(path2) == []
        c.save_checkpoint(path2, "foo")
        assert len(c.checkpoints(path)) == 2
        assert len(c2.checkpoints(path)) == 1
        assert len(c.checkpoints(path2)) == 1
        assert len(c2.checkpoints(path2)) == 0
