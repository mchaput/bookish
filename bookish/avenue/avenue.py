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

from bookish.compat import string_type
from bookish.parser.bootstrap import bootstrap_context
from bookish.parser import Miss


class AvenueParserError(Exception):
    pass


# Parents

def make_parents(data):
    parents = {}

    def walk(parent, obj):
        parents[id(obj)] = parent
        if isinstance(obj, dict):
            for v in obj.values():
                walk(obj, v)
        elif isinstance(obj, list):
            for v in obj:
                walk(obj, v)

    walk(None, data)
    return parents


def get_parent(parents, obj):
    return parents[id(obj)]


# Context

class AvenueContext(dict):
    def __init__(self, root, **kwargs):
        from bookish.functions import functions_dict

        super(AvenueContext, self).__init__()
        self.update(functions_dict)
        self.update(kwargs)
        self.root = root
        self._parents = make_parents(root)

    def parent(self, obj):
        return get_parent(self._parents, obj)


# Entry points

def parse(avestring):
    from bookish.grammars.avenue import grammar

    ctx = bootstrap_context()
    out, i = grammar(avestring, 0, ctx)
    if out is Miss:
        raise AvenueParserError(i)
    return out


def find(parsed, root, **vars):
    avectx = AvenueContext(root, **vars)
    return parsed.pull(avectx, root)


class AvenueManager(object):
    """
    Simple class that provides caching of compiled Avenue strings.
    """

    def __init__(self):
        self._cache = {}

    def compile(self, avestring):
        if avestring in self._cache:
            ave = self._cache[avestring]
        else:
            ave = parse(avestring)
            self._cache[avestring] = ave
        return ave

    def find(self, ave, root, start, **vars):
        if isinstance(ave, string_type):
            ave = self.compile(ave)
        avectx = AvenueContext(root, **vars)
        return ave.pull(avectx, start)
