# Copyright 2014 Matt Chaput. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
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

import os
import datetime
import difflib
import shutil

from bookish import paths
from bookish.stores import ResourceNotFoundError
from bookish.util import random_id

CHECKPOINT_DIR = "/_checkpoints"
CHECKPOINT_EXT = "._cp"
AUTOSAVE_EXT = "._auto"


class Checkpoints(object):
    def __init__(self, userid, store, cachestore, maxnum=10):
        self.userid = userid
        self.store = store
        self.cachestore = cachestore
        self.maxnum = maxnum

    def _autosave_path(self, path):
        assert path.startswith("/")
        return "%s%s.%s%s" % (CHECKPOINT_DIR, path, self.userid, AUTOSAVE_EXT)

    def _checkpoint_path(self, path, checkpointid=None):
        assert path.startswith("/")
        checkpointid = checkpointid or random_id()
        return "%s%s.%s.%s%s" % (CHECKPOINT_DIR, path, self.userid,
                                 checkpointid, CHECKPOINT_EXT)

    def autosave(self, path, content):
        aspath = self._autosave_path(path)
        asdir = paths.directory(aspath)
        if not self.cachestore.exists(asdir):
            self.cachestore.make_dir(asdir)
        self.cachestore.write_file(aspath, content.encode("utf8"))

    def save_checkpoint(self, path, content, encoding="utf8"):
        self.store.write_file(path, content.encode(encoding))

        cppath = self._checkpoint_path(path)
        cpdir = paths.directory(cppath)
        if not self.cachestore.exists(cpdir):
            self.cachestore.make_dir(cpdir)

        self.cachestore.write_file(cppath, content.encode(encoding))
        asp = self._autosave_path(path)
        if self.cachestore.exists(asp):
            self.cachestore.delete(asp)

    def restore_checkpoint(self, path, checkpointid, encoding="utf8"):
        content = self.get_checkpoint(path, checkpointid, encoding=encoding)
        self.store.write_file(path, content, encoding=encoding)
        return content

    def has_autosave(self, path):
        return self.cachestore.exists(self._autosave_path(path))

    def has_autosave_after(self, path, dt):
        if not self.has_autosave(path):
            return False

        try:
            modtime = self.cachestore.last_modified(path)
        except ResourceNotFoundError:
            return False

        return modtime > dt

    def get_autosave(self, path, encoding="utf8"):
        aspath = self._autosave_path(path)
        if self.cachestore.exists(aspath):
            return self.cachestore.content(aspath, encoding=encoding)
        else:
            return None

    def checkpoints(self, path):
        cachestore = self.cachestore
        dirpath = paths.directory(path)
        cpdirpath = CHECKPOINT_DIR + dirpath
        if cachestore.exists(cpdirpath):
            names = cachestore.list_dir(cpdirpath)
        else:
            return []

        cps = []
        for name in names:
            if not name.endswith(CHECKPOINT_EXT):
                continue
            basename = name[:0 - len(CHECKPOINT_EXT)]

            fname, userid, cpid = basename.rsplit(".", 2)
            if userid != self.userid:
                continue

            cppath = paths.join(cpdirpath, name)
            fpath = paths.join(dirpath, fname)
            if fpath != path:
                continue

            cps.append({
                "path": cppath,
                "modified": cachestore.last_modified(cppath),
                "id": cpid,
            })
        cps.sort(key=lambda d: d["modified"])
        return cps

    def get_checkpoint(self, path, checkpointid, encoding="utf8"):
        cppath = self._checkpoint_path(path, checkpointid)
        return self.cachestore.content(cppath, encoding=encoding)

    def clean_checkpoints(self, path):
        cachestore = self.cachestore
        cps = self.checkpoints(path)
        while len(cps) > self.maxnum:
            oldest = cps.pop(0)
            cachestore.delete(oldest["path"])


def drop_inline_diffs(diff):
    return [line for line in diff if not line.startswith("?")]


def merge_files(a, x, b):
    dxa = difflib.Differ()
    dxb = difflib.Differ()
    xa = drop_inline_diffs(dxa.compare(x, a))
    xb = drop_inline_diffs(dxb.compare(x, b))

    outlines = []
    index_a = 0
    index_b = 0
    had_conflict = False

    while (index_a < len(xa)) and (index_b < len(xb)):
        # no changes or adds on both sides
        if (xa[index_a] == xb[index_b] and
            (xa[index_a].startswith('  ') or xa[index_a].startswith('+ '))):
            outlines.append(xa[index_a][2:])
            index_a += 1
            index_b += 1
            continue

        # removing matching lines from one or both sides
        if ((xa[index_a][2:] == xb[index_b][2:])
            and (xa[index_a].startswith('- ') or xb[index_b].startswith('- '))):
            index_a += 1
            index_b += 1
            continue

        # adding lines in A
        if xa[index_a].startswith('+ ') and xb[index_b].startswith('  '):
            outlines.append(xa[index_a][2:])
            index_a += 1
            continue

        # adding line in B
        if xb[index_b].startswith('+ ') and xa[index_a].startswith('  '):
            outlines.append(xb[index_b][2:])
            index_b += 1
            continue

        # conflict - list both A and B, similar to GNU's diff3
        outlines.append("<<<<<<< A\n")
        while (index_a < len(xa)) and not xa[index_a].startswith('  '):
            outlines.append(xa[index_a][2:])
            index_a += 1
        outlines.append("=======\n")
        while (index_b < len(xb)) and not xb[index_b].startswith('  '):
            outlines.append(xb[index_b][2:])
            index_b += 1
        outlines.append(">>>>>>> B\n")
        had_conflict = True

    # append remining lines - there will be only either A or B
    for i in range(len(xa) - index_a):
        outlines.append(xa[index_a + i][2:])
    for i in range(len(xb) - index_b):
        outlines.append(xb[index_b + i][2:])

    return had_conflict, outlines

