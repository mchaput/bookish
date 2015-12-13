# Copyright 2015 Matt Chaput. All rights reserved.
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

from bookish import paths


class Scss(object):
    def __init__(self, app, store):
        self.app = app

        try:
            import sass
        except ImportError:
            self.app.logger.warning("libsass not available")
            return

        self.store = store
        self.asset_dir = self.app.config.get("SCSS_ASSET_DIR")

        if not self.asset_dir:
            self.app.logger.warning("No SCSS_ASSET_DIR configured.")
            return
        if not self.store.exists(self.asset_dir):
            self.app.logger.error("SCSS asset dir %r does not exist",
                                  self.asset_dir)
            return

        self.update_scss()
        if self.app.testing or self.app.debug:
            self.set_hooks()

    def set_hooks(self):
        # self.app.logger.info("Pyscss watching %r", self.asset_dir)
        self.app.before_request(self.update_scss)

    def find_scss(self, partials=False):
        for name in self.store.list_dir(self.asset_dir):
            if paths.extension(name) == ".scss":
                ispartial = name.startswith("_")
                if ispartial and not partials:
                    continue
                yield self.asset_dir + name, ispartial

    def output_path(self, path):
        assert path.endswith(".scss")
        return path.replace(".scss", ".css")

    def out_of_date(self, path):
        s = self.store
        mtime = self.store.last_modified(path)
        opath = self.output_path(path)
        if not s.exists(opath) or mtime > s.last_modified(opath):
            return True

    def partials_have_changed(self):
        for path, ispartial in self.find_scss(partials=True):
            if not ispartial:
                continue

            if self.out_of_date(path):
                return True

    def recompile_all(self):
        for path, _ in self.find_scss(partials=True):
            self.compile_scss(path)

    def update_scss(self):
        if self.partials_have_changed():
            return self.recompile_all()

        for path, _ in self.find_scss():
            if self.out_of_date(path):
                self.compile_scss(path)

    def compile_scss(self, path):
        import os.path

        name = paths.barename(path)

        fp = self.store.file_path(path)
        outfp = os.path.join(os.path.dirname(fp), name + ".css")

        self.app.logger.info("SCSS compiling %s", fp)
        try:
            import sass
            css = sass.compile(filename=fp, precision=3)
        except:
            import sys
            e = sys.exc_info()[1]
            self.app.logger.error(str(e))
            raise
        else:
            with open(outfp, "w") as f:
                f.write(css)
