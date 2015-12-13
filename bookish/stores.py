# Copyright 2013 Matt Chaput. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY MATT CHAPUT ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL MATT CHAPUT OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of Matt Chaput.

import errno
import os.path
import re
import sys
from datetime import datetime
from hashlib import md5

from bookish import compat, paths, util


def file_etag(fpath):
    stat = os.stat(fpath)
    h = md5()
    h.update(str(stat.st_ino).encode("ascii"))
    h.update(str(stat.st_size).encode("ascii"))
    h.update(str(stat.st_mtime).encode("ascii"))
    return h.hexdigest()


class ResourceNotFoundError(Exception):
    pass


class Store(object):
    """
    Base class for page storage objects.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.close()

    def file_path(self, path):
        """
        Returns the filesystem equivalent of the given virtual path, if it has
        one, otherwise None.
        """

        return None

    def etag(self, path):
        raise NotImplementedError(self.__class__.__name__)

    def exists(self, path):
        """
        Returns True if the given path exists in this store.
        """

        raise NotImplementedError(self.__class__)

    def is_dir(self, path):
        """
        Returns True if the given path represents a directory in this store.
        """

        raise NotImplementedError(self.__class__)

    def list_all(self, path="/"):
        if not path.endswith("/"):
            path += "/"
        for name in self.list_dir(path):
            p = paths.join(path, name)
            if self.is_dir(p):
                for sp in self.list_all(p):
                    yield sp
            else:
                yield p

    def list_dir(self, path):
        """
        Lists the file names under the given path.
        """

        return ()

    def last_modified(self, path):
        """
        Returns a datetime object
        """

        return datetime.utcnow()

    def size(self, path):
        """
        Returns the size (in bytes) of the file at the given path.
        """

        return len(self.content(path, encoding=None))

    def open(self, path, mode="rb"):
        """
        Returns a file-like object for *reading* the given path.
        """

        raise NotImplementedError(self.__class__)

    def writable(self, path):
        """
        Returns True if the given path can be created/overwritten.
        """

        return False

    def write_file(self, path, bytestring):
        with self.open(path, "w+b") as f:
            f.write(bytestring)

    def delete(self, path):
        """
        Deletes the underlying file for the given path.
        """

        raise NotImplementedError(self.__class__)

    def make_dir(self, path):
        """
        Creates a directory at the given path.
        """

        raise NotImplementedError(self.__class__)

    def content(self, path, encoding="utf8"):
        """
        Convenience method to return the string content of the file at the
        given path.

        :param encoding: the name of the encoding to use to decode the file's
            bytes. Default is ``"utf8"``. If you use ``encoding=None`` the
             method returns the raw bytestring.
        """

        f = self.open(path)
        string = f.read()

        if encoding:
            string = string.decode(encoding, "replace")

            # If the file starts with a BOM, throw it away
            if string.startswith(u"\ufeff"):
                string = string[1:]

        return string

    def close(self):
        pass


class FileStore(Store):
    """
    Represents a directory in the filesystem.
    """

    def __init__(self, dirpath):
        self.dirpath = os.path.abspath(dirpath)

    def __repr__(self):
        return "<%s %r>" % (type(self).__name__, self.dirpath)

    def file_path(self, path):
        path = paths.normalize_abs(path)
        return os.path.join(self.dirpath, path[1:])

    def etag(self, path):
        fpath = self.file_path(path)
        if os.path.exists(fpath):
            return file_etag(fpath)

    def exists(self, path):
        return os.path.exists(self.file_path(path))

    def is_dir(self, path):
        try:
            filepath = self.file_path(path)
            return os.path.isdir(filepath)
        except OSError:
            e = sys.exc_info()[1]
            if e.errno == errno.ENOENT:
                raise ResourceNotFoundError(path)

    def list_dir(self, path):
        try:
            return [fname for fname in os.listdir(self.file_path(path))
                    if not fname.startswith(".")]
        except OSError:
            e = sys.exc_info()[1]
            if e.errno == errno.ENOENT:
                raise ResourceNotFoundError(path)

    def last_modified(self, path):
        try:
            t = os.path.getmtime(self.file_path(path))
        except OSError:
            e = sys.exc_info()[1]
            if e.errno == errno.ENOENT:
                raise ResourceNotFoundError(path)

        return datetime.utcfromtimestamp(t)

    def size(self, path):
        try:
            return os.path.getsize(self.file_path(path))
        except OSError:
            e = sys.exc_info()[1]
            if e.errno == errno.ENOENT:
                raise ResourceNotFoundError(path)

    def open(self, path, mode="rb"):
        try:
            return open(self.file_path(path), mode)
        except OSError:
            e = sys.exc_info()[1]
            if e.errno == errno.ENOENT:
                raise ResourceNotFoundError(path)

    def writable(self, path):
        filepath = self.file_path(path)
        dirpath = os.path.dirname(filepath)
        try:
            return os.access(dirpath, os.W_OK)
        except OSError:
            e = sys.exc_info()[1]
            if e.errno == errno.ENOENT:
                raise ResourceNotFoundError(path)

    def delete(self, path):
        try:
            os.remove(self.file_path(path))
        except OSError:
            e = sys.exc_info()[1]
            if e.errno == errno.ENOENT:
                raise ResourceNotFoundError(path)

    def make_dir(self, path):
        os.makedirs(self.file_path(path))


class ZipTree(Store):
    """
    Looks for a zip file corresponding to the first part of a path, and if it
    finds one, looks inside that zip file for the rest of the path. This
    essentially makes zip files at the root level look like directories.
    """

    _top_exp = re.compile("/([^/]+)")

    def __init__(self, dirpath):
        self.dirpath = dirpath
        self.stores = {}

    @staticmethod
    def _splittable(path):
        return path.find("/", 1) > -1

    @staticmethod
    def _split_path(path):
        i = path.find("/", 1)
        assert i >= 0
        return path[1:i], path[i:]

    def _zip_filepath(self, first):
        zippath = os.path.join(self.dirpath, first + ".zip")
        if os.path.exists(zippath):
            return zippath

    def _zip_store(self, first):
        if first in self.stores:
            return self.stores[first]

        zippath = self._zip_filepath(first)
        if zippath:
            store = self.stores[first] = ZipStore(zippath)
            return store

    def _perform(self, path, fn):
        if self._splittable(path):
            first, rest = self._split_path(path)
            s = self._zip_store(first)
            if s:
                return fn(s, rest)
        raise ResourceNotFoundError(path)

    def etag(self, path):
        if self._splittable(path):
            first, _ = self._split_path(path)
            zpath = self._zip_filepath(first)
            if zpath:
                return file_etag(zpath)
        raise ResourceNotFoundError(path)

    def exists(self, path):
        if self._splittable(path):
            first, rest = self._split_path(path)
            s = self._zip_store(first)
            if s:
                if rest == "/":
                    return True
                return s.exists(rest)
        else:
            m = self._top_exp.match(path)
            if m:
                return bool(self._zip_store(m.group(1)))
            return False

    def is_dir(self, path):
        if self._splittable(path):
            return self._perform(path, lambda s, rest: s.is_dir(rest))
        else:
            m = self._top_exp.match(path)
            if m:
                s = self._zip_store(m.group(1))
                if s:
                    return True

            raise ResourceNotFoundError(path)

    def list_all(self, path="/"):
        for filename in os.listdir(self.dirpath):
            if not filename.endswith(".zip"):
                continue

            name = filename[:-4]
            base = "/" + name
            zipstore = self._zip_store(name)
            if zipstore:
                for p in zipstore.list_all():
                    pp = base + p
                    if pp.startswith(path):
                        yield pp

    def list_dir(self, path):
        return self._perform(path, lambda s, rest: s.list_dir(rest))

    def last_modified(self, path):
        return self._perform(path, lambda s, rest: s.last_modified(rest))

    def size(self, path):
        return self._perform(path, lambda s, rest: s.size(rest))

    def open(self, path, mode="rb"):
        return self._perform(path, lambda s, rest: s.open(rest, mode=mode))

    def close(self):
        for s in self.stores.values():
            s.close()


class ZipStore(Store):
    """
    Represents the files inside a zip archive.
    """

    def __init__(self, zipfilepath):
        from zipfile import ZipFile

        self.zipfilepath = zipfilepath
        self.zipfile = ZipFile(open(zipfilepath, "rb"), "r")

    @staticmethod
    def zipname(path):
        return paths.normalize_abs(path)[1:]

    def zipinfo(self, path):
        return self.zipfile.getinfo(self.zipname(path))

    def etag(self, path):
        return file_etag(self.zipfilepath)

    def exists(self, path):
        zname = self.zipname(path)
        zdirname = zname if zname.endswith("/") else zname + "/"
        for zpath in self.zipfile.namelist():
            if zpath == zname or zpath.startswith(zdirname):
                return True
        return False

    def is_dir(self, path):
        for _ in self.list_dir(path):
            return True
        return False

    def list_all(self, path="/"):
        if not path.endswith("/"):
            path += "/"
        ps = sorted(p for p in self.zipfile.namelist() if p.startswith(path))
        return ps

    def list_dir(self, path):
        if not path.endswith("/"):
            path += "/"
        zippath = self.zipname(path)
        names = set()
        for name in self.zipfile.namelist():
            if name.startswith(zippath):
                basename = name[len(zippath):].split("/")[0]
                names.add(basename)
        return sorted(names)

    def last_modified(self, path):
        return datetime(*self.zipinfo(path).date_time)

    def size(self, path):
        return self.zipinfo(path).file_size

    def open(self, path, mode="r"):
        return self.zipfile.open(self.zipname(path), "r")

    def close(self):
        self.zipfile.close()


class WrappingStore(Store):
    """
    Base class for PageStore implementations that wrap "child" stores.
    """

    def __init__(self, child):
        self.child = child

    def _xlate(self, path):
        return path

    def file_path(self, path):
        return self.child.file_path(self._xlate(path))

    def etag(self, path):
        return self.child.etag(self._xlate(path))

    def exists(self, path):
        return self.child.exists(self._xlate(path))

    def is_dir(self, path):
        return self.child.is_dir(self._xlate(path))

    def list_all(self, path="/"):
        for path in self.child.list_all():
            yield self._xlate(path)

    def list_dir(self, path):
        return self.child.list_dir(self._xlate(path))

    def last_modified(self, path):
        return self.child.last_modified(self._xlate(path))

    def size(self, path):
        return self.child.size(self._xlate(path))

    def open(self, path, mode="rb"):
        return self.child.open(self._xlate(path), mode)

    def delete(self, path):
        return self.child.delete(self._xlate(path))

    def writable(self, path):
        return self.child.writable(path)

    def close(self):
        self.child.close()


class SubStore(WrappingStore):
    """
    "Extracts" a "sub-directory" of a child store and presents it as a top-level
    store.
    """

    def __init__(self, child, prefix):
        self.child = child
        self.prefix = prefix

    def _xlate(self, path):
        return self.prefix + path


class MountStore(WrappingStore):
    """
    Mounts a child store at a "sub-directory", for use in an OverlayStore.
    """

    def __init__(self, child, prefix):
        self.child = child
        self.prefix = prefix

    def __repr__(self):
        return "<%s %r at %r>" % (type(self).__name__, self.child, self.prefix)

    def _check(self, path):
        prefix = self.prefix
        prelen = len(prefix)
        return (
            path.startswith(prefix)
            and len(path) > prelen
            and path[prelen] == "/"
        )

    def _xlate(self, path):
        if not self._check(path):
            raise Exception("%r can't translate path %r" % (self, path))
        return path[len(self.prefix):]

    def is_dir(self, path):
        if not path.startswith(self.prefix):
            return False
        return self.child.is_dir(self._xlate(path))

    def list_all(self, path="/"):
        if not path.startswith(self.prefix):
            return

        path = self._xlate(path)
        if not path.endswith("/"):
            path += "/"
        for p in self.child.list_all(path):
            yield self.prefix + p

    def list_dir(self, path):
        if self._check(path):
            return WrappingStore.list_dir(self, path)
        else:
            return []

    def exists(self, path):
        return self._check(path) and self.child.exists(self._xlate(path))


class OverlayStore(Store):
    """
    Overlays the contents of a number of sub-stores. When the methods are called
    with a path, this store tries its sub-stores in order, and fulfills the
    request using the first sub-store found that contains the path.
    """

    def __init__(self, *stores):
        self.stores = list(stores)

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__,
                           ", ".join(repr(s) for s in self.stores))

    def _store_for(self, path):
        for store in self.stores:
            if store.exists(path):
                return store

    def append(self, store):
        self.stores.append(store)

    def extend(self, stores):
        self.stores.extend(stores)

    def file_path(self, path):
        s = self._store_for(path)
        if s:
            return s.file_path(path)

    def etag(self, path):
        for store in self.stores:
            if store.exists(path):
                return store.etag(path)

    def exists(self, path):
        return any(s.exists(path) for s in self.stores)

    def is_dir(self, path):
        for s in self.stores:
            if s.exists(path):
                return s.is_dir(path)
        raise ResourceNotFoundError(path)

    def list_all(self, path="/"):
        seen = set()
        for store in self.stores:
            if store.exists(path):
                seen.update(store.list_all(path))
        return sorted(seen)

    def list_dir(self, path):
        seen = set()
        for store in self.stores:
            if store.exists(path):
                seen.update(store.list_dir(path))
        return sorted(seen)

    def last_modified(self, path):
        s = self._store_for(path)
        if not s:
            raise ResourceNotFoundError(path)
        return s.last_modified(path)

    def size(self, path):
        s = self._store_for(path)
        if not s:
            raise ResourceNotFoundError(path)
        return s.size(path)

    def open(self, path, mode="rb"):
        s = self._store_for(path)
        if not s:
            s = self.stores[0]
        return s.open(path, mode)

    def writable(self, path):
        s = self._store_for(path)
        if not s:
            s = self.stores[0]
        return s.writable(path)

    def write_file(self, path, bytestring):
        s = self._store_for(path)
        if not s:
            s = self.stores[0]
        return s.write_file(path, bytestring)

    def delete(self, path):
        s = self._store_for(path)
        if not s:
            s = self.stores[0]
        return s.delete(path)

    def close(self):
        for store in self.stores:
            store.close()


class StringStore(Store):
    """
    Base class for stores that more naturally return generate strings than
    file-like objects
    """

    def content(self, path, encoding="utf8"):
        raise NotImplementedError(self.__class__)

    def open(self, path, mode="rb"):
        assert mode == "rb"
        try:
            content = self.content(path)
        except KeyError:
            raise ResourceNotFoundError(path)
        return compat.StringIO(content)


class DictionaryStore(Store):
    """
    Presents a dictionary mapping path strings to bytes objects as a page store.

    Supports the ``list_all(path)`` method but does not support directories
    (``list_dir`` always returns ``[]`` and ``is_dir`` always returns False).

    Does not support last modified times (``last_modified`` always returns 0).
    """

    def __init__(self, dictionary, writable=False):
        self.dict = dictionary
        self._writable = writable
        self._reset_time()

    def _reset_time(self):
        self._time = datetime.utcnow()

    def _xlate(self, path):
        if not path.startswith("/"):
            raise ValueError("Paths must be absolute")
        return path

    def etag(self, path):
        if self.exists(path):
            return str(self._time)

    def exists(self, path):
        return self._xlate(path) in self.dict

    def is_dir(self, path):
        return False

    def list_all(self, path="/"):
        if not path.endswith("/"):
            path += "/"
        for p in sorted(self.dict):
            if p.startswith(path):
                yield p
            elif p > path:
                break

    def list_dir(self, path):
        return []

    def last_modified(self, path):
        return self._time

    def size(self, path):
        path = self._xlate(path)
        try:
            bytestring = self.dict[path]
        except KeyError:
            raise ResourceNotFoundError(path)
        return len(bytestring)

    def open(self, path, mode="rb"):
        assert mode == "rb"
        path = self._xlate(path)
        try:
            bytestring = self.dict[path]
        except KeyError:
            raise ResourceNotFoundError(path)
        return compat.BytesIO(bytestring)

    def writable(self, path):
        return self._writable

    def write_file(self, path, bytestring):
        assert self._writable
        self.dict[path] = bytestring
        self._reset_time()

    def make_dir(self, path):
        raise Exception("DictionaryStore doesn't support directories")


# def store_from_config(config):
#     stores = []
#
#     # virtuals = config.get("documents", "virtuals")
#     # if virtuals:
#     #     classnames = virtuals.split()
#     #     objs = []
#     #     for classname in classnames:
#     #         cls = util.class_from_name(classname)
#
#     dirs = config.get("documents", "directories")
#     stores.extend([FileStore(path.strip()) for path in dirs.split()])
#
#     resources = config.get("documents", "resources")
#     for resname in resources.split():
#         __import__(resname)
#         mod = sys.modules[resname]
#         dirpath = os.path.dirname(mod.__file__)
#         stores.append(FileStore(dirpath))
#
#     mounts = config.get("documents", "mounts")
#     if mounts:
#         mounts = mounts.split()
#         mounts = [(FileStore(mounts[i]), mounts[i + 1])
#                   for i in range(0, len(mounts), 2)]
#         for fs, prefix in mounts:
#             stores.append(MountStore(fs, prefix))
#
#
#
#
#     if len(stores) == 1:
#         store = dirs[0]
#     else:
#         store = OverlayStore(*stores)
#
#     return store
