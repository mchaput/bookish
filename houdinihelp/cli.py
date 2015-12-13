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

from __future__ import print_function
import os.path
import bisect
import codecs
import shutil

from flask.ext.script import Manager
from flask.ext.script.commands import InvalidCommand

from bookish import flaskapp, functions, paths, wikipages, util

from houdinihelp import server


manager = Manager(server.get_houdini_app)
manager.add_option("-C", "--config", dest="config_file", required=False)
manager.add_option("-O", "--object", dest="config_obj", required=False)
manager.add_option("-l", "--logfile", dest="log_file", required=False)
manager.add_option("-L", "--loglevel", dest="log_level", required=False)


def _exp(path):
    return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))


def _parse_vars(vars):
    d = {}
    for pair in vars.split(","):
        name, value = pair.split("=", 1)
        d[name] = value
    return d


def empty_cache(pages):
    cs = pages.cachestore
    if cs:
        for path in cs.list_all():
            manager.app.logger.debug("Deleting cache %s", path)
            cs.delete(path)


def get_prefixed_paths(pages, prefix):
    prefixdir = prefix if prefix.endswith("/") else paths.parent(prefix)
    for path in pages.store.list_all(prefixdir):
        if not path.startswith(prefix):
            continue
        yield path


def parse_page(path, **kwargs):
    pages = flaskapp.get_wikipages(manager.app)
    jsondata = pages.json(path, **kwargs)
    return jsondata


@manager.command
def clear_cache():
    pages = flaskapp.get_wikipages(manager.app)
    empty_cache(pages)


@manager.command
def serve(host="0.0.0.0", port=8080, debug=False, vars=None, bgindex=False):
    if vars:
        manager.app.jinja_env.globals.update(_parse_vars(vars))

    manager.app.config["ENABLE_BACKGROUND_INDEXING"] = bgindex
    manager.app.run(host=host, port=int(port), debug=debug)


@manager.command
def html(path):
    pages = flaskapp.get_wikipages(manager.app)
    print(pages.html(path))


@manager.command
def missing(images=False, links=False, unused=False, prefix="/", verbose=False):
    if not (images or links or unused):
        images = links = unused = True

    pages = flaskapp.get_wikipages(manager.app)
    all_images = set()
    used_images = set()
    for path in get_prefixed_paths(pages, prefix):
        if paths.extension(path) in (".png", ".jpg", ".jpeg", ".gif"):
            all_images.add(path)

        if not pages.is_wiki_source(path):
            continue

        if verbose:
            print(path)

        printed = False
        json = pages.json(path)
        for link in functions.find_links(json):
            value = link["value"]
            scheme = link.get("scheme")

            if value.startswith("#") or scheme in ("Icon", "Smallicon", "Largeicon"):
                continue

            fullpath = link.get("fullpath")
            if not fullpath:
                continue

            if pages.is_wiki(fullpath):
                fullpath = pages.source_path(fullpath)
            exists = pages.exists(fullpath)

            isimage = scheme in ("Image", "Anim")
            if isimage:
                used_images.add(fullpath)

            if exists:
                continue

            if (images and isimage) or (links and not isimage):
                if not verbose and not printed:
                    print(path)
                    printed = True
                print("    ", value, "  ", fullpath)

    if unused:
        unused_images = all_images - used_images
        bytes = 0
        for imgpath in sorted(unused_images):
            size = pages.size(imgpath)
            bytes += size
            print("Unused image:", imgpath, size)
        print(len(unused_images), "unused images (", bytes, ") out of", len(all_images))


@manager.command
def generate(dirpath, prefix="/", vars=None, longest=10, cache=True,
             nocache=False):
    pages = flaskapp.get_wikipages(manager.app)
    logger = manager.app.logger
    dirpath = _exp(dirpath)
    indexer = flaskapp.get_indexer(manager.app)
    searcher = indexer.searcher()

    if nocache:
        empty_cache(pages)

    count = 0
    largest = []

    if vars:
        vars = _parse_vars(vars)
        manager.app.config.setdefault("VARS", {}).update(vars)

    t = util.perf_counter()
    for path in get_prefixed_paths(pages, prefix):
        if not pages.is_wiki_source(path):
            continue

        logger.debug("Generating %s", path)
        count += 1

        tt = util.perf_counter()
        html = pages.html(path, save_to_cache=cache, searcher=searcher)
        tt = util.perf_counter() - tt

        htmlpath = paths.basepath(path) + ".html"
        filepath = os.path.join(dirpath, htmlpath[1:])

        # Make sure the destination directory exists, then create the file.
        parentdirpath = os.path.dirname(filepath)
        if not os.path.exists(parentdirpath):
            os.makedirs(parentdirpath)
        with open(filepath, "w") as f:
            f.write(html.encode("utf8"))

        # Keep track of slowest pages
        if len(largest) < longest or tt > largest[0][0]:
            if len(largest) >= longest:
                largest.pop(0)
            bisect.insort(largest, (tt, path))
    totaltime = util.perf_counter() - t

    logger.info("Generated %s files in %s secs", count, totaltime)
    logger.info("Average %s sec per page", totaltime / count)
    logger.info("Top %s longest times:")
    for gentime, path in largest:
        logger.info("%s | %03.04f secs ", path, gentime)


@manager.command
def index(prefix="/", clean=False, nocache=False, option=None, touchfile=None,
          usages=False):
    pages = flaskapp.get_wikipages(manager.app)
    indexer = flaskapp.get_indexer(manager.app)
    logger = manager.app.logger

    if usages:
        _index_usages(pages, logger)

    if option:
        key, value = option.split("=", 1)
        value = util.pyliteral(value, fallback_to_string=False)
        indexer.set_option(key, value)

    if nocache:
        empty_cache(pages)

    changed = indexer.update(pages, prefix=prefix, clean=clean)

    if changed and touchfile:
        # Touch the change file to indicate something changed.
        # This is to help the Makefile
        open(touchfile, "a").close()


@manager.command
def index_info():
    pages = flaskapp.get_wikipages(manager.app)
    indexer = flaskapp.get_indexer(manager.app)
    indexer.dump(pages)


def _index_usages(pages, logger, prefix="/examples/nodes/"):
    from houdinihelp.hsearch import usages_for_otl

    # Find all .otl files under the given prefix
    changed = False
    store = pages.store

    for path in store.list_all(prefix):
        if not pages.is_wiki_source(path):
            continue

        # Look for an hda or otl file with the same name as this wiki file
        bp = paths.basepath(path)
        exts = (".hda", ".otl")
        for ext in exts:
            p = bp + ext
            if store.exists(p):
                otlpath = p
                break
        else:
            continue

        # Check if there's a usages file already and if it's newer than the otl
        usagespath = bp + ".usages"
        if store.exists(usagespath):
            otlmod = store.last_modified(otlpath)
            usagesmod = store.last_modified(usagespath)
            if otlmod <= usagesmod:
                continue

        # Get the real file path corresponding to the OTL's virtual path
        filepath = pages.file_path(otlpath)
        if filepath:
            print("Generating usages for %s" % filepath)
            # Find all node usages in the OTL
            usages = usages_for_otl(filepath)

            # Write the usages to a file alongside the otl file
            basename = paths.basename(usagespath)
            parentdir = os.path.dirname(filepath)
            usagesfile = os.path.join(parentdir, basename)
            with open(usagesfile, "wb") as outfile:
                output = "\n".join(usages) + "\n"
                outfile.write(output.encode("utf8"))
            changed = True

    return changed


@manager.command
def index_usages(prefix="/examples/nodes/", touchfile=None):
    pages = flaskapp.get_wikipages(manager.app)
    logger = manager.app.logger

    changed = _index_usages(pages, logger)

    if changed and touchfile:
        # Touch the change file to indicate something changed.
        # This is to help the Makefile
        open(touchfile, "a").close()


@manager.command
def search(query, limit=None, stored=False):
    import pprint

    indexer = flaskapp.get_indexer(manager.app)
    q = indexer.query()
    q.set(query)
    if limit:
        q.set_limit(int(limit))

    for hit in q.search():
        if stored:
            pprint.pprint(dict(hit))
        else:
            print(hit["path"], hit["title"])


@manager.command
def textify(prefix, width=None):
    pages = flaskapp.get_wikipages(manager.app)
    txcls = flaskapp.get_textifier(manager.app, width=width)
    indexer = flaskapp.get_indexer(manager.app)
    searcher = indexer.searcher()

    for path in get_prefixed_paths(pages, prefix):
        if pages.is_wiki_source(path):
            jsondata = pages.json(path, searcher=searcher)
            output = txcls(jsondata).transform()
            print(output)


@manager.command
def prewarm(prefix="/"):
    pages = flaskapp.get_wikipages(manager.app)
    for path in pages.store.list_all(prefix):
        print(path)
        _ = pages.json(path, save_to_cache=True)


# @manager.command
# def preheat(prefix="/"):
#     pages = flaskapp.get_wikipages(manager.app)
#     for path in pages.store.list_all(prefix):
#         print(path)
#         _ = pages.html(path, save_to_cache=True)


@manager.command
def profile(path):
    # from bookish.grammars.wiki import blocks, grammar
    #
    # pages = manager.app.config.get("bookish_pages")
    # src = pages.content(path)
    # src = wiki.condition_string(src)
    #
    # ctx = wiki.bootstrap_context()
    # i = 0
    # blist = []
    # t = util.perf_counter()
    # while i < len(src):
    #     tt = util.perf_counter()
    #     out, newi = blocks(src, i, ctx)
    #     tt = util.perf_counter() - tt
    #     if not isinstance(out, dict):
    #         from bookish.parser import parser
    #         lines = parser.Lines(src)
    #         line, col = lines.line_and_col(i)
    #         print("Miss at line", line, "column", col, "(char %s)" % i)
    #         print(src[i-10:i+10])
    #         break
    #     i = newi
    #     blist.append((tt, out.get("type"),
    #                   repr(functions.string(out.get("text"))[:40])))
    # t = util.perf_counter() - t
    # blist.sort()
    # for tt, typename, txt in blist:
    #     print(tt, typename, txt)
    # print(t)

    import cProfile
    cProfile.run("parse_page(%r, conditional=False)" % path, sort="time")


@manager.command
def debug_wiki(path):
    from bookish.grammars.wiki import blocks
    from bookish.parser import parser, rules

    pages = flaskapp.get_wikipages(manager.app)
    src = wikipages.condition_string(pages.content(path))

    ctx = wikipages.bootstrap_context()
    i = 0
    blist = []
    t = util.perf_counter()
    missed = False
    while rules.streamend.accept(src, i, ctx)[0] is parser.Miss:
        tt = util.perf_counter()
        out, newi = blocks(src, i, ctx)
        tt = util.perf_counter() - tt

        if not isinstance(out, dict):
            lines = parser.Lines(src)
            line, col = lines.line_and_col(i)
            print("Miss at line", line, "column", col, "(char %s)" % i)
            print(repr(src[i:i+10]))
            missed = True
            break

        i = newi
        blist.append((tt, out.get("type"),
                      repr(functions.string(out.get("text"))[:40])))
    t = util.perf_counter() - t
    print("%0.06f" % t)

    if not missed:
        blist.sort(reverse=True)
        for tt, typename, txt in blist:
            print("%0.06f" % tt, typename, txt)


@manager.command
def archive(dirpath, zfile, force=False, include=None, exclude=None):
    import zipfile

    logger = manager.app.logger

    dirpath = _exp(dirpath)
    filepaths = list(util.file_paths(dirpath, include, exclude))

    def _up_to_date():
        if not os.path.exists(zfile):
            return False
        ziptime = os.path.getmtime(zfile)
        return not any(os.path.getmtime(p) > ziptime for p in filepaths)

    # Don't bother archiving if zip is up-to-date
    if not force and _up_to_date():
        return

    logger.info("Archiving directory %s to file %s", dirpath, zfile)
    t = util.perf_counter()
    count = 0
    zf = zipfile.ZipFile(zfile, "w", compression=zipfile.ZIP_DEFLATED)
    for path in filepaths:
        rp = os.path.relpath(path, dirpath).replace("\\", "/")
        zf.write(path, arcname=rp)
        logger.debug("Adding %s", path)
        count += 1
    logger.info("Archived %s files in %.01f sec",
                count, util.perf_counter() - t)
    zf.close()


def _copy_file(srcpath, destpath, force, logger=None):
    if (
        force
        or not os.path.exists(destpath)
        or os.path.getmtime(srcpath) > os.path.getmtime(destpath)
    ):
        parent = os.path.dirname(destpath)
        if not os.path.exists(parent):
            os.makedirs(parent)

        if logger:
            logger.debug("Copying %s to %s", srcpath, destpath)

        shutil.copy(srcpath, destpath)


def _copy_tree(srcdir, destdir, force=False, include=None, exclude=None,
               logger=None):
    count = 0
    for srcpath in util.file_paths(srcdir, include, exclude):
        relpath = os.path.relpath(srcpath, srcdir)
        destpath = os.path.join(destdir, relpath)

        if _copy_file(srcpath, destpath, force, logger=logger):
            count += 1
    return count


@manager.command
def copy_files(srcdir, destdir, force=False, include=None, exclude=None):
    logger = manager.app.logger
    srcdir = _exp(srcdir)
    destdir = _exp(destdir)

    logger.info("Copying %s to %s", srcdir, destdir)
    t = util.perf_counter()
    count = _copy_tree(srcdir, destdir, force, include, exclude, logger)
    logger.info("Copied %s files in %.01f sec", count, util.perf_counter() - t)


@manager.command
def copy_help(srcdir, destdir, force=False, zipdirs=None, include=None,
              exclude=None):
    logger = manager.app.logger
    srcdir = _exp(srcdir)
    destdir = _exp(destdir)

    logger.info("Copying help from %s to %s", srcdir, destdir)
    t = util.perf_counter()
    zipset = set()
    if zipdirs:
        zipdirfile = _exp(zipdirs)
        with open(zipdirfile) as f:
            zipset = set(line.strip() for line in f)

    # Iterate over the top-level items in the srcdir. If it's a directory,
    # check if it should be zipped. If it should, archive it, if not use
    # _copy_tree. If it's a file, use _copy_file.
    for name in os.listdir(srcdir):
        if name.startswith("."):
            continue

        srcpath = os.path.join(srcdir, name)
        destpath = os.path.join(destdir, name)
        if os.path.isdir(srcpath):
            if name in zipset:
                zfile = destpath + ".zip"
                archive(srcpath, zfile, force=force, include=include,
                        exclude=exclude)
            else:
                _copy_tree(srcpath, destpath, force, include, exclude, logger)
        else:
            _copy_file(srcpath, destpath, force, logger)

    logger.info("Copied help in %.01f sec", util.perf_counter() - t)


@manager.command
def trace(path):
    from bookish.grammars.wiki import blocks
    from bookish.parser import parser, rules

    pages = flaskapp.get_wikipages(manager.app)
    src = pages.content(path)
    src = wikipages.condition_string(src)
    lines = parser.Lines(src)

    ctx = wikipages.bootstrap_context()
    i = 0
    while not rules.streamend.at_end(src, i):
        out, newi = blocks(src, i, ctx)
        print(i, out, newi)
        if not isinstance(out, dict):
            line, col = lines.line_and_col(i)
            print("Miss at line", line, "column", col, "(char %s)" % i)
            print(repr(src[i:]))
            break
        if newi == i:
            line, col = lines.line_and_col(i)
            print("Stall at line", line, "column", col, "(char %s)" % i)
            print(repr(src[i:]))
            break
        i = newi


@manager.command
def dump(path):
    from bookish.util import dump_tree

    jsondata = parse_page(path, process=False, conditional=False)
    dump_tree(jsondata)


@manager.command
def sass(path):
    import glob
    import sass

    for filename in sorted(glob.glob(path)):
        print("SCSS compiling %s" % filename)
        sass.compile(filename=filename, precision=3)


@manager.command
def grammar(path, all=False, byname=True, meta=False, output=None):
    import os.path
    from bookish.parser.builder import build_meta, Builder

    path = os.path.abspath(path)

    if all and output:
        raise InvalidCommand("Can't specify output on multiple input files")

    if all:
        print("Compiling all grammars in", path)
        if not os.path.isdir(path):
            raise InvalidCommand("%r is not a directory" % path)

        paths = []
        for name in os.listdir(path):
            if name.endswith("bkgrammar"):
                p = os.path.abspath(os.path.join(path, name))
                paths.append(p)
    else:
        paths = [path]

    if not paths:
        print("No grammars affected")

    for p in paths:
        dirpath, filename = os.path.split(p)
        basename, ext = os.path.splitext(filename)

        if output:
            outpath = os.path.abspath(output)
        else:
            outpath = os.path.join(dirpath, basename + ".py")

        print("Compiling", p)
        with open(p) as f:
            gstring = f.read()

        print("Writing", outpath)
        with open(outpath, "w") as o:
            if meta or (byname and basename == "meta"):
                build_meta(gstring, o)
            else:
                Builder(file=o).build_string(gstring)


def runhelp(*args):
    def _patched_handle(self, prog, args=None):
        return self._old_handle(self._prog, args)

    # Quick monkey patching for flask.ext.script.Manager so that
    # we can pass in the hhelp executable path as argv[0]
    Manager._old_handle = Manager.handle
    Manager.handle = _patched_handle
    manager._prog = args[0]
    __import__('sys').argv = [__file__] + list(args[1:])
    manager.run()


if __name__ == "__main__":
    manager.run()
