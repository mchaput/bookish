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

import inspect

import jinja2
from jinja2 import escape

from bookish import paths, util, functions
from bookish.avenue import avenue
from bookish.compat import next, iteritems


class JinjaStoreLoader(jinja2.BaseLoader):
    """
    Jinja template loader that loads templates from a Bookish storage object.
    """

    def __init__(self, store, prefix="/templates/"):
        self.store = store
        self.prefix = prefix

    def get_source(self, environment, template_path):
        store = self.store
        content = store.content(template_path)
        filepath = store.file_path(template_path)

        lastmod = store.last_modified(template_path)
        uptodate = lambda: store.last_modified(template_path) == lastmod
        return content, filepath, uptodate

    def list_templates(self, extensions=None, filter_func=None):
        for path in self.store.list_dir(self.prefix):
            if filter_func and filter_func(path):
                yield path
            elif extensions and paths.extension(path) in extensions:
                yield path


class Stylesheet(object):
    def __init__(self, store, templatename, index_page_name, globals=None):
        self.store = store
        self.loader = JinjaStoreLoader(self.store)
        self.env = self._make_env(globals)
        self.templatename = templatename
        self.index_page_name = index_page_name

        # Cache for compiled Avenue pattern objects
        self._patterns = {}

    def __repr__(self):
        return "<Stylesheet %r>" % (self.templatename,)

    def _make_env(self, globaldict):
        env = jinja2.Environment(loader=self.loader)

        # Add passed globals to the environment
        if globaldict:
            env.globals.update(globaldict)

        return env

    def template(self):
        return self.env.get_template(self.templatename)

    @staticmethod
    def default_rule(jinctx, obj, render):
        # Default action for blocks that don't have an associated rule
        if isinstance(obj, (list, tuple)):
            return functions.string(obj)
        elif isinstance(obj, dict):
            return "".join((render(jinctx, obj.get("text", ())),
                            render(jinctx, obj.get("body", ()))))
        else:
            return escape(functions.string(obj))

    def context_and_function(self, basepath, jsondata, extras=None):
        """
        Returns a Jinja context function you can use to transform a JSON
        document using the rules contained in this style's template.
        """

        template = self.template()

        # Create the render function
        @jinja2.contextfunction
        def render(jinctx, obj):
            if isinstance(obj, dict):
                # Look for a rule named <type>_rule, then <role>_rule
                rule = None
                for prefix in (obj.get("type"), obj.get("role")):
                    if not prefix:
                        continue

                    macroname = "%s_rule" % prefix
                    if macroname in jinctx.exported_vars:
                        rule = jinctx.vars[macroname]
                        break

                if rule is None:
                    if "default" in jinctx.exported_vars:
                        rule = jinctx.vars["default"]
                    else:
                        return self.default_rule(jinctx, obj, render)

                return rule(obj)

            elif isinstance(obj, (list, tuple)) or inspect.isgenerator(obj):
                return functions.string(render(jinctx, o) for o in obj)
            else:
                return escape(functions.string(obj))

        kwargs = {
            "rel": util.make_rel_fn(basepath, self.index_page_name),
            "render": render,
            "docroot": jsondata,
        }
        if extras:
            kwargs.update(extras)

        # Create a new Jinja context
        jinjactx = template.new_context(vars=kwargs)
        # Run the style template to evaluate the rule definitions
        list(template.root_render_func(jinjactx))

        return jinjactx, render

    def render(self, basepath, jsondata):
        jinjactx, renderfn = self.context_and_function(basepath, jsondata)
        return renderfn(jinjactx, jsondata)
