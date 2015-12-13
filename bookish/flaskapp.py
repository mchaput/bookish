# Copyright 2014 Matt Chaput. All rights reserved.
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
import os
import datetime
import logging.handlers
import mimetypes
import sys
import threading
import traceback

import flask

import werkzeug.exceptions

import bookish.config
from bookish import (
    coloring, compat, paths, i18n, search, stores, wikipages, util
)
from bookish.checkpoints import Checkpoints
from bookish.flasksupport import Scss


app = flask.Flask(__name__)

extra_types = {
    "bkgrammar": "text/plain",
}

indexing_thread = threading.Thread()


def null_rel(x):
    return x


class IndexingTimer(threading.Thread):
    """
    Call a function after a specified number of seconds:

        t = Timer(30.0, f, args=None, kwargs=None)
        t.start()
        t.cancel()     # stop the timer's action if it's still waiting

    """

    def __init__(self, interval, function, args=None):
        threading.Thread.__init__(self)
        self.daemon = True
        self.interval = interval
        self.function = function
        self.args = args
        self.finished = threading.Event()

    def cancel(self):
        self.finished.set()

    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args)
        self.finished.set()


class NotModified(werkzeug.exceptions.HTTPException):
    """
    An HTTP "304 Not Modified" response.
    """

    code = 304

    def get_response(self, environment):
        return flask.Response(status=304)


def is_unconditional():
    """
    Returns True if the given flask request is unconditional (that is, cannot
    be served from a cache).
    """

    headers = flask.request.headers
    return (headers.get("Pragma") == "no-cache"
            or headers.get("Cache-Control") == "no-cache")


def directory_page(pages, dirpath):
    """
    Renders a simple template to show the files in a directory.
    """

    store = pages.store
    names = store.list_dir(dirpath)
    files = []

    for name in names:
        path = paths.join(dirpath, name)
        link = path
        if pages.is_wiki(link):
            link = paths.basepath(link)
        isdir = store.is_dir(path)
        if isdir:
            size = -1
            mod = -1
        else:
            size = store.size(path)
            mod =  store.last_modified(path)

        files.append({
            "path": path,
            "link": link,
            "name": name,
            "ext": paths.extension(name),
            "isdir": isdir,
            "size": size,
            "modified": mod,
        })

    return flask.render_template("/templates/dir.jinja2", path=dirpath,
                                 files=files)


def get_request_language(pages, path):
    """
    Get the human language from a flask request
    """

    if flask.request.get("hl"):
        return flask.request.get("hl")

    if flask.session:
        hl = flask.session.get("i18n_language")
        if hl:
            return hl

    header_string = flask.request.headers.get("accept-languages")
    available_langs = pages.available_langauges(path)
    return i18n.parse_http_accept_language(header_string, available_langs)


def get_request_userid():
    if "userid" in flask.session:
        userid = flask.session["userid"]
    else:
        userid = flask.session["userid"] = util.random_id()
    return userid


# Error handlers

@app.errorhandler(404)
def page_not_found(e):
    path = flask.request.path
    config = flask.current_app.config

    pages = get_wikipages()
    store = pages.store

    editable = False
    isdir = store.exists(path) and store.is_dir(path)
    if config.get("EDITABLE") and not isdir:
        editable = pages.is_wiki(path)

    content = flask.render_template('/templates/404.jinja2', path=path,
                                    editable=editable, rel=null_rel, num=404)
    return content, 404


@app.errorhandler(500)
def internal_error(exception):
    from bookish.coloring import format_string

    path = flask.request.path

    trace = traceback.format_exc()
    trace = format_string(trace, "pytb")

    content = flask.render_template('/templates/500.jinja2', path=path,
                                    trace=trace, rel=null_rel, num=500)
    return content, 500


# Endpoints

@app.route('/', defaults={'path': ''})
@app.route("/<path:path>")
def show(path):
    app = flask.current_app
    config = app.config

    pages = get_wikipages()
    indexer = get_indexer()
    searcher = indexer.searcher()
    editable = config["EDITABLE"]

    store = pages.store
    path = paths.normalize("/" + path)
    pathexists = store.exists(path)
    spath = pages.source_path(path)
    cond = not is_unconditional()
    # print("path=", path, "cond=", cond)
    isdir = pathexists and store.is_dir(path)

    if isdir:
        if not path.endswith("/"):
            return flask.redirect(path + "/", 302)
        if not store.exists(spath):
            return directory_page(pages, path)

    ext = paths.extension(path)
    if pathexists and not isdir:
        fpath = store.file_path(path)
        if fpath:
            return flask.send_file(fpath, add_etags=True, conditional=cond)
        else:
            try:
                fp = pages.store.open(path)
                if hasattr(fp, "name"):
                    fp.name = None
                mimetype, encoding = mimetypes.guess_type(path)
                resp = flask.send_file(fp, conditional=cond, mimetype=mimetype)
                etag = "%s.%s" % (path, str(store.last_modified(path)))
                resp.set_etag(etag)
                return resp
            except stores.ResourceNotFoundError:
                raise werkzeug.exceptions.NotFound

    elif not ext and store.exists(spath):
        etag = pages.etag(spath)
        if cond and etag:
            inm = flask.request.if_none_match
            if etag in inm:
                raise NotModified()

        try:
            extras = {
                "editable": editable,
                "q": flask.request.args.get('q', ''),
                "pages": pages, "searcher": searcher,
                "paths": paths,
            }
            try:
                html = pages.html(path, conditional=cond, searcher=searcher,
                                  extras=extras, allow_redirect=True)
            except wikipages.Redirect:
                e = sys.exc_info()[1]
                return flask.redirect(e.newpath, 302)

            resp = flask.Response(html)
            if etag:
                resp.set_etag(etag)
            return resp

        except stores.ResourceNotFoundError:
            e = sys.exc_info()[1]
            app.logger.error(e)
            raise werkzeug.exceptions.NotFound
    else:
        raise werkzeug.exceptions.NotFound


@app.route("/_search")
def search_page():
    request = flask.request
    config = flask.current_app.config

    indexer = get_indexer()
    searcher = indexer.searcher()
    qobj = searcher.query()

    cat_order = config.get("CATEGORIES", "").split()

    shortcuts = list(config.get("SHORTCUTS", ()))
    shortcuts.extend(config.get("EXTRA_SHORTCUTS", ()))

    qstring = request.args.get("q", "")
    # startpos = request.args.get("startpos", "")
    # endpos = request.args.get("endpos", "")
    category = request.args.get("category", None)
    templatepath = request.args.get("template", config["SEARCH_TEMPLATE"])

    r = qobj.results(qstring, cat_order, category=category,
                     shortcuts=shortcuts)
    return flask.render_template(templatepath, **r)


@app.route("/_tag/<tag>")
def tag_page(tag):
    pages = get_wikipages()
    indexer = get_indexer()

    pagepath = "/tags/" + tag
    spath = pages.source_path(pagepath)
    if pages.exists(spath):
        return show(pagepath)
    else:
        searcher = indexer.searcher()
        docs = searcher.documents(tags=tag)
        tagcloud = searcher.tag_cloud()
        rel = util.make_rel_fn(pagepath, pages.index_page_name)
        return flask.render_template("/templates/tag.jinja2", rel=rel, tag=tag,
                                     docs=docs, tagcloud=tagcloud)


@app.route("/_edit/<path:path>")
def edit_wiki(path):
    config = flask.current_app.config

    editable = config["EDITABLE"]
    if not editable:
        flask.abort(500)

    pages = get_wikipages()
    path = paths.normalize("/" + path)
    path = pages.source_path(path)
    if paths.extension(path) != config["WIKI_EXT"]:
        # TODO: better error here!
        flask.abort(500)

    userid = get_request_userid()
    cp = Checkpoints(userid, pages.store, pages.cachestore)

    from_autosave = False
    if pages.exists(path):
        lastmod = pages.last_modified(path)
        if cp.has_autosave_after(path, lastmod):
            source = cp.get_autosave(path)
            from_autosave = True
        else:
            source = pages.content(path, reformat=True)
    else:
        lastmod = 0
        source = ""

    return flask.render_template("/templates/edit.jinja2", source=source,
                                 path=path, rel=null_rel, lastmod=lastmod,
                                 from_autosave=from_autosave)


@app.route("/_preview/", methods=["GET", "POST"])
def preview_wiki():
    request = flask.request
    config = flask.current_app.config

    pages = get_wikipages()
    indexer = get_indexer()
    searcher = indexer.searcher()
    autosave_seconds = config.get("AUTOSAVE_SECONDS", 10)
    autosave = (
        config.get("AUTOSAVE", True) and request.form.get("autosave") != "false"
    )

    assert "path" in request.form
    path = request.form["path"]
    assert path
    source = request.form.get("source", "")
    scrollTop = int(request.form.get("scrollTop") or "0")

    lastmod = 0
    if pages.exists(path):
        lastmod = pages.last_modified(path)

    last_autosave = 0
    if autosave:
        session = flask.session
        userid = get_request_userid()

        if "last_autosave" in session:
            last_autosave = session.get("last_autosave")
        else:
            last_autosave = datetime.datetime.utcnow()

        cp = Checkpoints(userid, pages.store, pages.cachestore)
        now = datetime.datetime.utcnow()
        if now - last_autosave >= datetime.timedelta(seconds=autosave_seconds):
            cp.autosave(path, source)
            last_autosave = session["last_autosave"] = now

    def rel(p):
        if p.startswith("http:") or p.startswith("https:"):
            return p
        return paths.join(path, p)

    extras = {"rel": rel}

    html = pages.preview(path, source, searcher=searcher, extras=extras,
                         templatename="/templates/preview.jinja2")
    return flask.jsonify(html=html, last_modified=lastmod,
                         last_autosave=last_autosave, scrollTop=scrollTop)


@app.route("/_save/", methods=["POST"])
def save_wiki():
    request = flask.request
    config = flask.current_app.config

    maxnum = config.get("CHECKPOINT_MAX", 10)

    pages = get_wikipages()
    path = request.form["path"]
    source = request.form["source"]
    # encoding = request.form.get("encoding", "utf8")

    userid = get_request_userid()
    cp = Checkpoints(userid, pages.store, pages.cachestore, maxnum)
    cp.save_checkpoint(path, source, encoding="utf8")
    return source


@app.route("/_restore/", methods=["POST"])
def restore_wiki():
    request = flask.request
    config = flask.current_app.config

    pages = get_wikipages()
    path = request.form["path"]
    checkpointid = request.form["id"]
    # encoding = request.form.get("encoding", "utf8")

    userid = get_request_userid(request)
    cp = Checkpoints(userid, pages.store, pages.cachestore)
    return cp.restore_checkpoint(path, checkpointid, encoding="utf8")


@app.route("/_tooltip/<path:path>")
def debug_tooltip(path):
    pages = get_wikipages()
    indexer = get_indexer()
    searcher = indexer.searcher()

    path = paths.normalize("/" + path)
    path = pages.source_path(path)

    html = pages.html(
        path, templatename="/templates/plain.jinja2",
        stylesname="/templates/tooltip.jinja2",
        conditional=False, searcher=searcher,
    )
    return html


# @app.route("/_headers")
# def show_headers():
#     out = "<table>"
#     for key, value in flask.request.headers:
#         out += "<tr><td>%s</td><td>%s</td><tr>" % (key, value)
#     out += "</table>"
#     return out


@app.route("/_wiki/<path:path>")
def debug_wiki_structure(path):
    pages = get_wikipages()
    indexer = get_indexer()
    searcher = indexer.searcher()

    path = paths.normalize("/" + path)
    path = pages.source_path(path)

    jsondata = pages.json(paths.basepath(path), conditional=False,
                          extra_context=flask.request.args, searcher=searcher)
    return flask.render_template("/templates/debug_wiki.jinja2",
                                 path=path, root=jsondata, searcher=searcher)


@app.route("/_indexed/<path:path>")
def debug_search(path):
    pages = get_wikipages()
    indexer = get_indexer()
    sables = indexer.searchables

    path = paths.normalize("/" + path)
    path = pages.source_path(path)

    jsondata = pages.json(path, conditional=False)
    docs = list(sables.documents(pages, path, jsondata, flask.request.args))
    return flask.render_template("/templates/debug_search.jinja2",
                                 path=path, docs=docs)


@app.route("/_text/<path:path>")
def debug_textify(path):
    pages = get_wikipages()
    txcls = get_textifier()
    indexer = get_indexer()
    searcher = indexer.searcher()

    path = paths.normalize("/" + path)
    path = pages.source_path(path)

    jsondata = pages.json(path, searcher=searcher, conditional=False)
    output = txcls(jsondata).transform()
    return flask.Response(output, mimetype="text/plain")


@app.route("/_load_example", methods=['POST'])
def load_example():
    request = flask.request
    if request.method == "POST":
        from houdinihelp.api import load_example

        url = request.form.get("url")
        launch = request.form.get("launch") == "true"
        load_example(url, launch)
        return "", 200

    flask.abort(400)


# Misc functions

def reindex(app=None, clean=False):
    app = app or flask.current_app
    indexer = get_indexer(app)
    pages = get_wikipages(app)
    try:
        indexer.update(pages)
    except search.LockError:
        pass


def reindex_threaded(timeout, app=None, clean=False, first=False):
    global indexing_thread

    reindex(app, clean)
    indexing_thread = IndexingTimer(timeout, reindex_threaded,
                                    (timeout, app, clean))
    indexing_thread.start()


def format_code(source, lexername=None, pre=False):
    from jinja2 import Markup

    app = flask.current_app
    lexer = None
    lexername = lexername or source.get("lang")

    if lexername:
        key = "%s_LEXER" % lexername.upper()
        if lexername and key in app.config:
            cls = app.config[key]
            if isinstance(cls, compat.string_type):
                cls = util.find_object(cls)
            lexer = cls()

    html = coloring.format_block(source, lexername=lexername, lexer=lexer,
                                 pre=pre)
    return Markup(html)


# Functions to create useful objects based on the current app

def get_store(app=None):
    app = app or flask.current_app
    storelist = app.config["DOCUMENTS"]
    if len(storelist) == 1:
        store = storelist[0]
    else:
        store = stores.OverlayStore(*storelist)
    return store


def get_wikipages(app=None):
    from bookish import wikipages

    app = app or flask.current_app
    config = app.config
    store = get_store(app)

    cls = config.get("PAGES_CLASS", wikipages.WikiPages)
    return cls(
        store=store,
        env=app.jinja_env,
        cachedir=config.get("CACHE_DIR"),
        page_template=config.get("DEFAULT_TEMPLATE", "/templates/page.jinja2"),
        index_page_name=config.get("INDEX_PAGE_NAME", "_index"),
        wiki_ext=config.get("WIKI_EXT", ".txt"),
        default_language=config.get("DEFAULT_LANGAUGE", "en-us"),
        logger=app.logger,
    )


def get_indexer(app=None):
    from bookish import search

    app = app or flask.current_app
    config = app.config
    sables = config.get("SEARCHABLES", search.Searchables())
    cls = config.get("INDEXER_CLASS", search.WhooshIndexer)

    main_dir = config["INDEX_DIR"]
    static_dir = config.get("STATIC_INDEX_DIR")
    return cls(main_dir, sables, logger=app.logger, staticdir=static_dir)


def get_textifier(app=None, width=None):
    app = app or flask.current_app
    config = app.config

    cls = config["TEXTIFY_CLASS"]
    if isinstance(cls, compat.string_type):
        cls = util.find_object(cls)

    return cls


# Init function

def init_app(app):
    from bookish.styles import JinjaStoreLoader
    from bookish.functions import functions_dict

    store = get_store(app)

    env = app.jinja_env
    env.loader = JinjaStoreLoader(store)
    env.globals.update(functions_dict)
    env.globals["format_code"] = format_code
    env.globals["exists"] = store.exists

    # app.teardown_appcontext(teardown)


# Factory

def configure_app(config_obj=bookish.config.DefaultConfig,
                  config_file=None, log_file=None, log_level=None):
    app.config.from_object(config_obj)
    if config_file:
        app.config.from_pyfile(config_file, silent=False)
    app.config.from_envvar("BOOKISH_CONFIG", silent=True)

    # Configure logging
    handler = logging.StreamHandler()

    # If we weren't passed a log file path, see if there's one in the config
    if not log_file:
        log_file = app.config.get("LOGFILE")

    # If we have a log file, set up a handler for it
    if log_file:
        log_file = bookish.config.expandpath(log_file)
        try:
            handler = logging.FileHandler(log_file)
        except IOError:
            pass

    # Set a formatter because the default is awful
    from logging import Formatter
    handler.setFormatter(Formatter("%(asctime)s: %(message)s"))

    # Set the handler in flask and werkzeug
    app.logger.addHandler(handler)
    werk_logger = logging.getLogger('werkzeug')
    if not werk_logger.handlers:
        werk_logger.addHandler(handler)

    # If we weren't passed a log level, see if it's in the config
    if not log_level:
        log_level = app.config.get("LOGLEVEL", "INFO")
    # If the log level is a string, convert it
    if isinstance(log_level, compat.string_type):
        log_level = getattr(logging, log_level.upper())
    # Set the log level
    app.logger.setLevel(log_level)
    werk_logger.setLevel(log_level)

    # Initialize app
    init_app(app)

    # Background indexing
    @app.before_first_request
    def reindex():
        app.logger.info("Starting background indexer")
        if app.config.get("ENABLE_BACKGROUND_INDEXING"):
            global indexing_thread
            seconds = app.config["BACKGROUND_INDEXING_INTERVAL"]
            reindex_threaded(seconds, app, first=True)

    if app.config.get("AUTO_COMPILE_SCSS"):
        Scss(app, get_store(app))

    return app


def set_werkzeug_logging(dir):
    # Configure werkzeug logging

    w_logger = logging.getLogger('werkzeug')
    w_logger.setLevel(logging.INFO)
    w_logfile = os.path.join(dir, "werkzeug.log")
    w_handler = logging.handlers.RotatingFileHandler(w_logfile,
                                                     maxBytes=4 * 1024 * 1024,
                                                     backupCount=4)
