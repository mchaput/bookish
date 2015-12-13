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
import json
import logging
import os.path
import tempfile

from bookish import compat, paths, i18n, pipeline, stores, styles, util
from bookish.functions import string
from bookish.parser import condition_string, Miss
from bookish.parser.bootstrap import bootstrap_context


default_logger = logging.getLogger(__name__)
default_logger.setLevel(logging.DEBUG)
default_logger.addHandler(logging.StreamHandler())

# def make_pipe(vs, context):
#     vs = [v for v in vs if (not v.offword or not context.get(v.offword))]
#     return pipeline.Pipe(*vs)


class Redirect(Exception):
    def __init__(self, newpath):
        self.newpath = newpath


def span(typename, text, **kwargs):
    assert isinstance(typename, compat.string_type)
    kwargs["type"] = typename
    kwargs["text"] = text
    return kwargs


def block(typename, indent, text, role=None, **kwargs):
    assert isinstance(typename, compat.string_type)
    kwargs["type"] = typename
    kwargs["indent"] = indent
    if text:
        kwargs["text"] = text
    if role is not None:
        kwargs["role"] = role
    return kwargs


def generate_id(block):
    return "id%x" % id(block)


def head(eqs, indent, text, **kwargs):
    if eqs == 1:
        rolename = "title"
        level = 0
    else:
        rolename = "h"
        level = eqs
    return block("h", indent, text, role=rolename, level=level, **kwargs)


def parse_string(src):
    from bookish.grammars.wiki import grammar

    src = condition_string(src)
    ctx = bootstrap_context()
    out, i = grammar(src, 0, ctx)
    assert out is not Miss
    jsondata = {"type": "root", "body": out, "attrs": {}}
    return jsondata


def remove_duplicates(ls):
    out = []
    seen = set()
    for item in ls:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def get_section(body, sectionid):
    for block in body:
        if block.get("role") == "section" and block.get("id") == sectionid:
            return block


class WikiPages(object):
    default_template = "/templates/page.jinja2"
    default_style = "/templates/wiki.jinja2"

    def __init__(self, store, env, cachedir=None, caching=True, languages=None,
                 page_template=None, page_style=None, mem_cache_size=10,
                 index_page_name="_index", wiki_ext=".txt",
                 default_language="en-us", logger=None):
        self.store = store
        self.env = env
        self.caching = caching
        self.index_page_name = index_page_name
        self.wiki_ext = wiki_ext
        self.logger = logger or default_logger

        self._prepipe = pipeline.default_pre_pipeline()
        self._postpipe = pipeline.default_post_pipeline()

        languages = ([i18n.normalize_language_name(ln) for ln in languages]
                     if languages else [])
        self.default_language = default_language
        self.languages = remove_duplicates([default_language] + languages)
        # print("languages=", languages)

        self.page_template = page_template or self.default_template
        self.page_style = page_style or self.default_style

        self.cachedir = None
        self.cachestore = None
        if caching:
            if not cachedir:
                cachedir = tempfile.mkdtemp(prefix="bookish", suffix=".cache")
            self.cachedir = cachedir
            self.cachestore = stores.FileStore(cachedir)
            # Small "level 1" in-memory cache
            self.memcache = util.DbLruCache(mem_cache_size)
        self._styles = {}

    def pre_pipe(self):
        return self._prepipe

    def post_pipe(self):
        return self._postpipe

    def style(self, templatename):
        if templatename in self._styles:
            style = self._styles[templatename]
        else:
            style = styles.Stylesheet(self.store, templatename,
                                      self.index_page_name, self.env.globals)
            self._styles[templatename] = style
        return style

    def full_path(self, origin, relpath):
        path = paths.join(origin, relpath)
        base, frag = paths.split_fragment(path)
        if base.endswith("/"):
            base += self.index_page_name
        return base + frag

    def source_path(self, path, locale=None):
        path, frag = paths.split_fragment(path)

        if (
            not path.endswith("/") and self.store.exists(path) and
            self.store.is_dir(path)
        ):
            path += "/"
        if path.endswith("/"):
            path += self.index_page_name + self.wiki_ext

        basepath, ext = paths.split_extension(path)
        if not ext:
            if locale:
                path = "%s.%s%s" % (basepath, locale, ext)
            path += self.wiki_ext

        return path

    def is_wiki(self, path):
        ext = paths.extension(path)
        return (not ext) or ext == self.wiki_ext

    def is_wiki_source(self, path):
        return paths.extension(path) == self.wiki_ext

    def is_index_page(self, path):
        assert path.startswith("/")
        dirpath, filename = paths.split_dirpath(path)
        return (filename == self.index_page_name
                or filename.startswith(self.index_page_name + "."))

    def find_source(self, path, locales=None):
        locales = locales or (None,)
        for locale in locales:
            locale = locale if locale != "en" else None
            spath = self.source_path(path, locale)
            if self.store.exists(spath):
                return spath
        return None

    def file_path(self, path):
        """
        Takes a virtual server path and translates it into a "real" file path,
        or None if the resource does not exist in a file.
        """

        return self.store.file_path(path)

    def exists(self, path):
        return self.store.exists(self.source_path(path))

    def last_modified(self, path):
        return self.store.last_modified(self.source_path(path))

    def size(self, path):
        return self.store.size(path)

    def etag(self, path, locale=None):
        spath = self.source_path(path, locale=locale)
        etag = self.store.etag(spath)
        # TODO: mix in the etags for the style and templates
        return etag

    def reformat_text(self, text):
        text = text.replace("\t", " " * 4)
        return text

    def content(self, path, reformat=False, encoding="utf8"):
        text = self.store.content(path, encoding=encoding)
        if reformat:
            text = self.reformat_text(text)
        return text

    def _check_source(self, path):
        spath = self.source_path(path)
        # assert spath.endswith(self.wiki_ext)
        if not self.store.exists(spath):
            raise stores.ResourceNotFoundError(path)
        return spath

    def wiki_context(self, path, conditional=True, save_to_cache=True,
                     searcher=None):
        m = dict(path=path, conditional=conditional,
                 save_to_cache=save_to_cache)
        wcontext = util.Context(m)
        wcontext.pages = self
        wcontext.searcher = searcher
        return wcontext

    def available_languages(self, path):
        store = self.store
        dirpath, filename = paths.split_dirpath(path)
        basename, ext = paths.split_extension(filename)
        result = []
        for lang in self.langauges:
            if lang == self.default_language:
                langfilename = filename
            else:
                langfilename = "%s.%s.%s" % (basename, lang, ext)
            if store.exists(paths.join(dirpath, langfilename)):
                result.append(lang)
        return result

    def _cache_file_dt(self, sourcepath, cachepath):
        # If the file exists in the cache...
        store = self.store
        cstore = self.cachestore
        if store.exists(sourcepath) and cstore.exists(cachepath):
            # Check the date on the original
            srcdt = store.last_modified(sourcepath)
            # If the date on the cached version isn't older, return it
            cachedt = cstore.last_modified(cachepath)
            # print("path=", sourcepath, "src=", srcdt, "c=", cachedt)
            if not cachedt < srcdt:
                return cachedt

    def put_cache_file(self, cachepath, bytestring):
        assert cachepath.startswith("/")

        filepath = os.path.join(self.cachedir, cachepath[1:])
        parent = os.path.dirname(filepath)
        if not os.path.exists(parent):
            os.makedirs(parent)
        with open(filepath, "wb") as f:
            f.write(bytestring)

    def get_cached_json(self, sourcepath, cachepath):
        # If the file exists in the cache and isn't older than the original...
        cachedt = self._cache_file_dt(sourcepath, cachepath)
        # print("path=", sourcepath, "cachedt=", cachedt)
        if cachedt is not None:
            # Check for the file in the memory cache
            if cachepath in self.memcache:
                # print(sourcepath, "from mem cache")
                return self.memcache.get(cachepath)

            # Load and parse the cached JSON
            jsonstring = self.cachestore.content(cachepath, "utf8")
            jsondata = json.loads(jsonstring)

            # Check the includes for changes
            includes = frozenset(jsondata.get("includes", ()))
            for incpath in includes:
                # If the include is missing, the cached data is invalid
                if not self.store.exists(incpath):
                    return None
                # If the include is newer, the cached data is invalid
                if cachedt < self.store.last_modified(incpath):
                    return None

            # Put it in the memcache and return it
            self.memcache.put(cachepath, jsondata)
            return jsondata

        elif cachepath in self.memcache:
            del self.memcache[cachepath]

    def json(self, path, wcontext=None, ext=".json", conditional=True,
             postprocess=True, save_to_cache=True, extra_context=None,
             searcher=None, allow_redirect=False):
        store = self.store
        path = self._check_source(path)
        jsonpath = paths.basepath(path) + ext

        if wcontext is None:
            wcontext = self.wiki_context(
                path, conditional=conditional, save_to_cache=save_to_cache,
                searcher=searcher
            )
            if extra_context:
                wcontext.update(extra_context)
        else:
            old_context = wcontext
            wcontext = wcontext.push({"path": path})
            wcontext.searcher = searcher or old_context.searcher
            wcontext.pages = self

        # Set up holders for cached and parse times in the context; these may
        # be useful for debugging
        if "parse_time" not in wcontext:
            wcontext["parse_time"] = {}
        if "cached" not in wcontext:
            wcontext["cached"] = set()
        times = wcontext["parse_time"]
        cached = wcontext["cached"]
        jsondata = None

        # Try to get the JSON data from the cache
        if wcontext.get("conditional") and self.caching:
            jsondata = self.get_cached_json(path, jsonpath)
            if jsondata is not None:
                # print("From cache", path)
                # Add the file to the context's debug list of cached files
                cached.add(path)

        if jsondata is None:
            # It wasn't in the cache, so we'll have to load and parse it
            t = compat.perf_counter()
            # Load the content of the file
            source = store.content(path, "utf8")
            # Parse the wiki markup
            jsondata = parse_string(source)
            # Run preprocessers
            self.pre_pipe().apply(jsondata, wcontext)
            # Store the parsing time in the context for debugging
            times[path] = compat.perf_counter() - t

            # If we're caching, save the parsed JSON to a file in the cache.
            # Note that we don't add the json data to the mem cache here; we
            # only do that when a cached json file is loaded. This has the
            # effect of only caching a document in memory if it's been accessed
            # at least *twice*.
            if self.caching and save_to_cache:
                jsonified = json.dumps(jsondata)
                self.put_cache_file(jsonpath, jsonified.encode("utf8"))

        if postprocess:
            # Run postprocessors
            self.post_pipe().apply(jsondata, wcontext)

        attrs = jsondata.get("attrs")
        if allow_redirect and attrs and "redirect" in attrs:
            fullpath = self.full_path(path, attrs["redirect"])
            raise Redirect(fullpath)

        return jsondata

    def string_to_json(self, path, content, wcontext=None, searcher=None,
                       extras=None, postprocess=True):
        path = self.source_path(path)
        assert path.endswith(self.wiki_ext), path
        extras = extras or {}

        # Parse the content string
        jsondata = parse_string(content)

        if not wcontext:
            wcontext = self.wiki_context(path, save_to_cache=False,
                                         searcher=searcher)

        # Run preprocessors
        self.pre_pipe().apply(jsondata, wcontext)
        # Run postprocessors
        if postprocess:
            self.post_pipe().apply(jsondata, wcontext)

        return jsondata

    def _template_for_page(self, templatename, jsondata):
        if not templatename:
            pagetype = string(jsondata.get("attrs", {}).get("type"))
            typetemplate = "/templates/%s.jinja2" % pagetype
            if pagetype and self.store.exists(typetemplate):
                templatename = typetemplate
        if not templatename:
            templatename = self.page_template
        return self.env.get_template(templatename)

    def _render_json(self, path, stylesname, templatename, jsondata, extras,
                     searcher):
        # Render the page template
        kwargs = {
            "path": path,
            "basepath": paths.basepath(path),
            "is_index_page": self.is_index_page(path),
            "rel": util.make_rel_fn(path, self.index_page_name),
            "searcher": searcher,
        }
        if extras:
            kwargs.update(extras)

        # Create a function to render JSON to HTML
        stylesname = stylesname or self.page_style
        styleobj = self.style(stylesname)
        stylectx, render = styleobj.context_and_function(path, jsondata, kwargs)

        # Create a function to apply the stylesheet to a given object
        def render_styles(obj):
            return render(stylectx, obj)

        # Get the page template
        template = self._template_for_page(templatename, jsondata)

        html = template.render(docroot=jsondata, render_styles=render_styles,
                               **kwargs)
        return html

    def preview(self, path, content, templatename=None, stylesname=None,
                language=None, searcher=None, extras=None):
        path = self.source_path(path)
        if extras:
            extras["preview"] = True
        jsondata = self.string_to_json(path, content, searcher=searcher,
                                       extras=extras)
        return self._render_json(path, stylesname, templatename, jsondata,
                                 extras, searcher)

    def html(self, path, templatename=None, stylesname=None,
             conditional=True, save_to_cache=True, language=None,
             searcher=None, extras=None, allow_redirect=False):
        path = self.source_path(path)
        assert path.endswith(self.wiki_ext), path

        # Load and parse file
        wctx = self.wiki_context(
            path, conditional=conditional, save_to_cache=save_to_cache,
            searcher=searcher
        )
        jsondata = self.json(path, wctx, save_to_cache=save_to_cache,
                             searcher=searcher, allow_redirect=allow_redirect)
        return self._render_json(path, stylesname, templatename, jsondata,
                                 extras, searcher)


# def pages_from_config(config, env, store=None):
#     if store is None:
#         store = stores.store_from_config(config)
#
#     cachedir = compat.config_get(config, "documents", "cache_dir")
#     caching = compat.config_getboolean(config, "documents", "caching", True)
#
#     page_template = compat.config_get(config, "templates", "default")
#     page_style = compat.config_get(config, "templates", "styles")
#
#     languages = compat.config_get(config, "documents", "languages")
#     if languages:
#         languages = languages.split()
#
#     classname = compat.config_get(config, "pages", "class",
#                                   "bookish.wikipages.Pages")
#     cls = util.class_from_name(classname)
#
#     return cls(store, env, cachedir=cachedir, caching=caching,
#                languages=languages, page_template=page_template,
#                page_style=page_style)
#
#
# def envvars_from_config(config, section="environment", prefixkey="-prefix"):
#     envvars = {}
#
#     # Grab variables from os environment based on prefix
#     if config.has_option(section, prefixkey):
#         prefix = config.get(section, prefixkey)
#         for key, value in os.environ:
#             if key.startswith(prefix):
#                 envvars[key] = value
#
#     # Grab variables from [environment] section of configuration file
#     if config.has_section("environment"):
#         for key, value in config.items("environment"):
#             if key != prefixkey:
#                 envvars[key] = os.path.expandvars(value)
#
#     return envvars
