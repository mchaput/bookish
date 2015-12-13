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

from __future__ import print_function
import ast
import functools
import fnmatch
import os.path
import random
import re
import shutil
from tempfile import mkdtemp, mkstemp
from contextlib import contextmanager

import bookish
from bookish import paths
from bookish.compat import range, string_type, perf_counter, htmlparser


random_chars = "abcdefghijklmnopqrstuvwxyz0123456789"
html = htmlparser.HTMLParser()


def random_id(length=10):
    return "".join(random.choice(random_chars) for _ in range(length))


class TempDir(object):
    def __init__(self):
        self.path = None

    def __enter__(self):
        self.path = mkdtemp(prefix="bookish")
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            shutil.rmtree(self.path)


class TempDB(object):
    def __init__(self):
        self.path = ''

    def __enter__(self):
        _, self.path = mkstemp(prefix="bookish", suffix=".sqlite")
        self.db = connect(self.path)
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.db.close()
            os.remove(self.path)


def decode_named_entity(name):
    return html.unescape("&%s;" % name)


def builtin_grammar(name):
    pkgdir = os.path.dirname(bookish.__file__)
    path = os.path.join(pkgdir, "grammars", name)
    f = open(path, "rb")
    string = f.read().decode("utf8")
    f.close()
    return string


_space_regex = re.compile(r"[\r\n\t ]+")


def normalize_text(tx):
    return _space_regex.sub(" ", tx)


def join_text(text):
    """
    Joins adjacent strings in a "text" list together. This function recursively
    descends into "text" keys found on non-string spans in the list.
    """

    last = 0
    i = 0
    while i < len(text):
        span = text[i]
        if not isinstance(span, string_type):
            if i > last:
                text[last:i] = ["".join(text[last:i])]
            last = i = last + 1

            stext = span.get("text")
            if stext:
                span["text"] = join_text(stext)
        else:
            i += 1
    if last < len(text):
        text[last:] = ["".join(text[last:])]
    return text


def flatten_text(obj):
    """
    Returns a string containing just the string values from the given "text"
    list. The function recursively descends into "text" keys found on
    non-string spans in the list.
    """

    if isinstance(obj, string_type):
        return obj
    elif isinstance(obj, list) and obj:
        return "".join(flatten_text(o) for o in obj)
    elif isinstance(obj, dict):
        text = obj.get("text")
        body = obj.get("body")
        return " ".join((flatten_text(text), flatten_text(body)))
    elif obj is None:
        return ""
    else:
        return repr(obj)


def dump_tree(block, stream=None, tab=0):
    if stream is None:
        from sys import stdout
        stream = stdout

    if isinstance(block, list):
        print("---")
        for subblock in block:
            dump_tree(subblock, stream, tab)
        return

    if not isinstance(block, dict):
        print("*** ERROR non-block: %r" % block)
        return

    print("  " * tab, "*", block.get("type"), file=stream)
    for k, v in block.items():
        if k in ("body", "type"):
            continue
        print("  " * (tab + 1), k, "=", repr(v), file=stream)
    body = block.get("body")
    if body:
        for subblock in body:
            dump_tree(subblock, stream=stream, tab=tab + 2)


def dumps_tree(block):
    from bookish.compat import StringIO
    sio = StringIO()
    dump_tree(block, sio)
    return sio.getvalue()


_normalize_ws_regex = re.compile(r"\s+")


def normalize_ws(s):
    return _normalize_ws_regex.sub(" ", s.strip())


def file_paths(dirpath, include=None, exclude=None, callback=None):
    if dirpath.startswith("."):
        return
    if not os.path.isdir(dirpath):
        raise ValueError("%s is not a directory" % dirpath)

    names = os.listdir(dirpath)
    for name in names:
        if name.startswith("."):
            continue
        if exclude and fnmatch.fnmatch(name, exclude):
            continue

        path = os.path.join(dirpath, name)
        if callback and not callback(path):
            continue
        if os.path.isdir(path):
            for x in file_paths(path, include, exclude):
                yield x
        else:
            if not include or fnmatch.fnmatch(name, include):
                yield path


class Context(object):
    def __init__(self, m=None):
        self.parent = None
        self.map = m

    def __iter__(self, seen=None):
        seen = seen or set()
        if self.map:
            for key in self.map:
                if key not in seen:
                    yield key
                    seen.add(key)
        if self.parent:
            for key in self.parent.__iter__(seen):
                yield key

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self._list_maps())

    def _list_maps(self):
        out = []
        if self.map:
            out.append(self.map)
        if self.parent:
            out.extend(self.parent._list_maps())
        return out

    def keys(self):
        return iter(self)

    def values(self):
        for key, value in self.items():
            yield value

    def items(self, seen=None):
        seen = seen or set()
        if self.map:
            for key in self.map:
                if key not in seen:
                    yield key, self.map[key]
                    seen.add(key)
        if self.parent:
            for item in self.parent.__iter__(seen):
                yield item

    def __getitem__(self, key):
        if self.map:
            try:
                return self.map[key]
            except KeyError:
                pass

        if self.parent:
            return self.parent[key]

        raise KeyError(key)

    def __setitem__(self, key, value):
        if not self.map:
            self.map = {}
        self.map[key] = value

    def __contains__(self, key):
        if self.map and key in self.map:
            return True
        if self.parent:
            return key in self.parent
        return False

    def get(self, key, default=None):
        if self.map and key in self.map:
            return self.map[key]
        elif self.parent:
            return self.parent.get(key, default)
        return default

    def update(self, m):
        if not self.map:
            self.map = {}
        self.map.update(m)

    def push(self, m=None):
        c = self.__class__(m)
        if self.map:
            c.parent = self
        else:
            c.parent = self.parent
        return c

    def first(self):
        if self.map:
            return self.map
        else:
            return {}


def find_object(name, blacklist=None, whitelist=None):
    """
    Imports and returns an object given a fully qualified name.

    >>> find_object("whoosh.analysis.StopFilter")
    <class 'whoosh.analysis.StopFilter'>
    """

    if blacklist:
        for pre in blacklist:
            if name.startswith(pre):
                raise TypeError("%r: can't instantiate names starting with %r"
                                % (name, pre))
    if whitelist:
        passes = False
        for pre in whitelist:
            if name.startswith(pre):
                passes = True
                break
        if not passes:
            raise TypeError("Can't instantiate %r" % name)

    lastdot = name.rfind(".")

    assert lastdot > -1, "Name %r must be fully qualified" % name
    modname = name[:lastdot]
    clsname = name[lastdot + 1:]

    mod = __import__(modname, fromlist=[clsname])
    cls = getattr(mod, clsname)
    return cls


def pyliteral(value, fallback_to_string=False):
    if value is None:
        return None

    try:
        value = ast.literal_eval(value)
    except ValueError:
        if fallback_to_string:
            pass
        else:
            raise
    except SyntaxError:
        if fallback_to_string:
            pass
        else:
            raise

    return value


def json_file(filename):
    import json

    with open(filename) as f:
        return json.load(f)


def class_from_name(name, namespace=None, classdict=None):
    if "." in name:
        cls = find_object(name)
    elif namespace:
        cls = getattr(namespace, name)
    elif classdict:
        cls = classdict[name]
    else:
        raise ValueError("Unknown class name %r" % name)
    return cls


def object_from_item(config, section, option, cls=None, namespace=None,
                     classdict=None):
    prefix = option + "."
    kwargs = {}
    for key, value in config.items(section):
        if key == option or key.startswith(prefix):
            if "." in key:
                objname, attr = key.split(".", 1)
                value = pyliteral(value, fallback_to_string=True)
                kwargs[attr] = value
            else:
                cls = class_from_name(value, namespace, classdict)
    return cls(**kwargs)


def objects_from_items(items, namespace=None, classdict=None):
    classes = {}
    args = {}
    for key, value in items:
        value = value.strip()
        if "." in key:
            objname, attr = key.split(".", 1)
            value = pyliteral(value, fallback_to_string=True)
            args.setdefault(objname, {})[attr] = value
        else:
            classes[key] = class_from_name(value, namespace, classdict)

    objects = {}
    for objname, cls in classes.items():
        argdict = args.get(objname, {})
        obj = cls(**argdict)
        objects[objname] = obj
    return objects


@contextmanager
def timing(name=""):
    t = perf_counter()
    yield
    print("%s: %0.06f" % (name, perf_counter() - t))


def memoize(f):
    memo = {}
    def helper(x):
        if x in memo:
            return memo[x]
        else:
            r = memo[x] = f(x)
            return r
    return helper


def make_rel_fn(basepath, index_page_name):
    def rel(pathstring):
        if not pathstring:
            return ""
        if pathstring.startswith("http:") or pathstring.startswith("https:"):
            return pathstring

        if pathstring.startswith("/") and pathstring.endswith("/"):
            pathstring += index_page_name
        return paths.relativize(basepath, pathstring)
    return rel


namere1 = re.compile("[ \t\r\n]+")
namere2 = re.compile("\W+")


def make_id(name):
    name = name.strip().lower()
    name = namere1.sub("_", name)
    name = namere2.sub("", name)
    return name


class DbLruCache(object):
    """
    Double-barrel least-recently-used cache decorator. This is a simple
    LRU algorithm that keeps a primary and secondary dict. Keys are checked
    in the primary dict, and then the secondary. Once the primary dict fills
    up, the secondary dict is cleared and the two dicts are swapped.

    Keys must be hashable.
    """

    def __init__(self, maxsize=100):
        self.maxsize = maxsize
        self.caches = [{}, {}]
        self.ptr = 0

    def __contains__(self, key):
        caches = self.caches
        return key in caches[0] or key in caches[1]

    def __delitem__(self, key):
        a, b = self.caches
        if key in a:
            del a[key]
        if key in b:
            del b[key]

    def get(self, key):
        caches, ptr = self.caches, self.ptr
        a = caches[ptr]
        b = caches[not ptr]
        if key in a:
            return a[key]
        elif key in b:
            return b[key]

    def put(self, key, value):
        caches, ptr = self.caches, self.ptr
        a = caches[ptr]
        b = caches[not ptr]

        a[key] = value
        if len(a) >= self.maxsize:
            b.clear()
            self.ptr = not ptr
