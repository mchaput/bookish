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


def is_abs(path):
    return path.startswith("/")


def parts(path):
    """
    Yields the parts of the given path string::

    >>> list(parts("/a/b/c"))
    ["/", "a/", "b/", "c"]
    """

    i = 0
    while i < len(path):
        slash = path.find("/", i)
        if slash < 0:
            yield path[i:]
            return

        yield path[i:slash + 1]
        i = slash + 1


def norm_parts(path, out=None):
    """
    Returns a list of the *normalized* parts of the given path string.
    This means that special names such as "." and ".." are applied, and
    multiple adjacent slashes are replaced with a single slash.

    >>> norm_parts("/a/b//c/../d")
    ["/", "a/", "b/", "d"]
    """

    out = out or []
    for i, item in enumerate(parts(path)):
        if item in (".", "./", ""):
            pass
        elif item in ("..", "../"):
            if len(out) > 1:
                out.pop()
        elif i > 0 and item == "/":
            pass
        else:
            out.append(item)
    return out


def normalize(path):
    """
    Returns a *normalized* version of the given path string.
    This means that special names such as "." and ".." are applied, and
    multiple adjacent slashes are replaced with a single slash.

    >>> normalize("/a/b//c/../d")
    "/a/b/d"
    """

    return "".join(norm_parts(path))


def normalize_abs(path):
    """
    Like normalize() but raises an error if the given path is not absolute.
    """

    if not is_abs(path):
        raise ValueError(repr(path))
    return "".join(norm_parts(path))


def parent(path):
    """
    Returns the parent directory path of the given resource.

    >>> parent("/a/b/c")
    "/a/"
    >>> parent("/a/b/")
    "/a/"
    >>> parent("/")
    "/"
    """

    if not path:
        return ""
    if path == "/":
        return "/"

    ps = norm_parts(path)

    # If the path ends with a non-dir item, strip it first
    if ps and not ps[-1].endswith("/"):
        ps.pop()

    # Only strip the last directory if it's not the root directory
    if ps and not (len(ps) == 1 and ps[0] == "/"):
        ps.pop()

    return "".join(ps)


def directory(path):
    """
    If the given path is a directory resource (ends with a slash), this returns
    the path unchanged. If it's a file resource, returns the path of the file's
    parent directory.

    >>> parent("/a/b/")
    "/a/b/"
    >>> parent("/a/b")
    "/a/"
    """

    if path.endswith("/"):
        return path
    else:
        return "".join(norm_parts(path)[:-1])


def join(basepath, relpath):
    """
    Joins two path strings intelligently. If the first path specifies a file,
    the second path will be joined to the first path's *directory*.

    >>> join("/a/b", "c")
    "/a/b/c"
    >>> join("/a/b/c", "d")
    "/a/b/d"
    >>> join("/a/b/c/", "../d")
    "/a/b/d"
    """

    if relpath.startswith("#"):
        return basepath + relpath

    if is_abs(relpath):
        return relpath
    basepath = directory(basepath)

    # Call normalized_paths on relpath, but use the output of
    # normalized_paths(basepath) as the initial output buffer
    return "".join(norm_parts(relpath, out=norm_parts(basepath)))


def relativize(basepath, targetpath):
    """
    Returns a relative path from the "base" resource to the "target" resource.

    >>> relativize("/a/b", "c")
    "c"
    >>> relativize("/a/b/c", "/a/b/d/e")
    "d/e"
    >>> relativize("/a/b/c", "/d/e/f")
    "../../d/e/f"
    """

    a = norm_parts(basepath)
    b = norm_parts(targetpath)

    i = 0
    while i < len(a) and i < len(b) and a[i] == b[i]:
        i += 1
    common = i

    out = []
    while i < len(a) and a[i].endswith("/") and a[i] != "/":
        out.append("../")
        i += 1
    out.extend(b[common:])

    return "".join(out)


def basepath(path):
    """
    Removes the extension from the end of a path.
    """

    assert path.startswith("/")
    dot = path.rfind(".")
    slash = path.rfind("/")
    if dot > slash and dot >= 0:
        return path[:dot]
    else:
        return path


def basename(path):
    """
    Returns the base name of the file named by the path.
    If the resource is a directory, the base name is the empty string ("").

    >>> basename("/a/b")
    "b"
    >>> basename("/a/b/")
    ""
    """

    if not path:
        return ""

    last = norm_parts(path)[-1]
    if last.endswith("/"):
        return ""
    else:
        return last


def barename(path):
    """
    Returns the base name of the file named by the path, with any extension
    removed.
    If the resource is a directory, the base name is the empty string ("").

    >>> basename("/a/b.txt")
    "b"
    >>> basename("/a/b")
    "b"
    >>> basename("/a/b/")
    ""
    """

    name = basename(path)
    return strip_extension(name)


def extension(path):
    """
    Returns the "extension" part of the base name of a resource path.

    >>> extension("/a/b/foo.bar")
    "bar"
    >>> extension("/a/b/foo")
    ""
    >>> extension("/a/b/foo.")
    ""
    """
    name = basename(path)
    if "." in name:
        return name[name.rfind("."):]
    else:
        return ""


def strip_extension(name):
    """
    Removes any extension from the given string.
    """

    if "." in name:
        return name[:name.rfind(".")]
    else:
        return name


def split_dirpath(path):
    """
    Returns the parent path and the file name of a resource path.

    >>> split_dirpath("/a/b/foo.bar")
    ("/a/b/", "foo.bar")
    """

    lastslash = path.rfind("/")
    if lastslash < 0:
        return "", path
    else:
        return path[:lastslash + 1], path[lastslash + 1:]


def split_extension(path):
    """
    Returns the base part and the extension part of the base name of a resource
    path.

    >>> split_extension("/a/b/foo.bar")
    ("foo", "bar")
    """

    name = basename(path)
    dot = name.rfind(".")
    if dot >= 0:
        ext = name[dot + 1:]
        if not ext.isdigit():
            return name[:dot], ext

    return name, ""


def split_fragment(path):
    """
    Returns the path and the fragment of a path/fragment combo.

    >>> split_fragment("/a/b/foo#bar")
    ("/a/b/foo", "#bar")
    """

    hash = path.rfind("#")
    if hash >= 0:
        return path[:hash], path[hash:]
    else:
        return path, ""

