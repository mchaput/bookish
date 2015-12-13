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

import operator
import re


class Pattern(object):
    def matches(self, ctx, obj):
        raise NotImplementedError

    def pull(self, ctx, obj):
        raise NotImplementedError


class Root(Pattern):
    def matches(self, ctx, obj):
        return obj is ctx.root

    def pull(self, ctx, obj):
        yield ctx.root


class Lookup(Pattern):
    def __init__(self, key):
        self.key = key

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.key)

    def matches(self, ctx, obj):
        if obj is not ctx.root:
            par = ctx.parent(obj)
            if isinstance(par, (dict, list)):
                try:
                    return par[self.key] is obj
                except KeyError:
                    return False
                except IndexError:
                    return False

    def pull(self, ctx, obj):
        if isinstance(obj, (dict, list)):
            try:
                yield obj[self.key]
            except KeyError:
                pass
            except IndexError:
                pass


class Slice(Pattern):
    def __init__(self, start, stop=None):
        self.start = start
        self.stop = stop

    def __repr__(self):
        return "%s(%r, %r)" % (type(self).__name__, self.start, self.stop)

    def matches(self, ctx, obj):
        start = self.start
        stop = self.stop
        if obj is not ctx.root:
            par = ctx.parent(obj)
            if isinstance(par, list):
                x = par.index(obj)
                if stop is not None:
                    return start <= x < stop
                else:
                    return start == x

    def pull(self, ctx, obj):
        start = self.start
        stop = self.stop
        if isinstance(obj, list) and start < len(obj):
            if stop is not None:
                for sub in obj[start:stop]:
                    yield sub
            else:
                yield obj[start]


class Star(Pattern):
    def matches(self, ctx, obj):
        return True

    def pull(self, ctx, obj):
        if isinstance(obj, dict):
            return iter(obj.values())
        elif isinstance(obj, list):
            return iter(obj)
        else:
            return iter((obj,))


class TestPattern(Pattern):
    def _test(self, ctx, obj):
        raise NotImplementedError

    def matches(self, ctx, obj):
        return self._test(ctx, obj)

    def pull(self, ctx, obj):
        if isinstance(obj, list):
            for o in obj:
                for oo in self.pull(ctx, o):
                    yield oo
        else:
            if self._test(ctx, obj):
                yield obj


class Comparison(TestPattern):
    ops = {"=": operator.eq, "==": operator.eq, "<=": operator.le,
           ">=": operator.ge, "<": operator.lt, ">": operator.gt,
           "!=": operator.ne}

    def __init__(self, name, opname, value):
        self.name = name
        self.opname = opname
        self.value = value

        if opname == "=~":
            expr = re.compile(value)
            self.fn = lambda v: bool(expr.match(v))
        else:
            op = self.ops[opname]
            self.fn = lambda v: op(v, self.value)

    def __repr__(self):
        return "%s(%r, %r, %r)" % (type(self).__name__, self.name, self.opname,
                                   self.value)

    def _test(self, ctx, obj):
        if isinstance(obj, dict):
            try:
                v = obj[self.name]
            except KeyError:
                return False
            if self.fn(v):
                return True


def run_code(ctx, obj, code):
    c = ctx.copy()
    if isinstance(obj, dict):
        c.update(obj)
    c["this"] = obj

    return eval(code, {}, c)


class Predicate(TestPattern):
    def __init__(self, source):
        self.source = source
        self.code = compile(self.source, "<string>", "eval", dont_inherit=True)

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.source)

    def _test(self, ctx, obj):
        try:
            return run_code(ctx, obj, self.code)
        except NameError:
            return False


class Union(Pattern):
    def __init__(self, patterns):
        self.patterns = patterns

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.patterns)

    def matches(self, ctx, obj):
        return any(pattern.matches(ctx, obj) for pattern in self.patterns)

    def pull(self, ctx, obj):
        seen = set()
        for pattern in self.patterns:
            for x in pattern.pull(ctx, obj):
                if id(x) not in seen:
                    yield x
                    seen.add(id(x))


class Filter(Pattern):
    def __init__(self, pattern, test):
        self.pattern = pattern
        self.test = test

    def matches(self, ctx, obj):
        if self.pattern.matches(ctx, obj):
            for _ in self.test.pull(ctx, obj):
                return True

    def pull(self, ctx, obj):
        for o in self.pattern.pull(ctx, obj):
            for _ in self.test.pull(ctx, o):
                yield o
                break


class Action(Pattern):
    def __init__(self, source):
        self.source = source
        self.code = compile(self.source, "<string>", "eval", dont_inherit=True)

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.source)

    def pull(self, ctx, obj):
        try:
            result = run_code(ctx, obj, self.code)
        except NameError:
            pass
        else:
            yield result

    def matches(self, ctx, obj):
        return False


class Child(Pattern):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "%s(%r, %r)" % (type(self).__name__, self.left, self.right)

    def matches(self, ctx, obj):
        return (
            obj is not ctx.root
            and self.left.matches(ctx, ctx.parent(obj))
            and self.right.matches(ctx, obj)
        )

    def pull(self, ctx, obj):
        seen = set()
        for o in self.left.pull(ctx, obj):
            for oo in self.right.pull(ctx, o):
                if id(oo) not in seen:
                    yield oo
                    seen.add(id(oo))


class Sequence(Pattern):
    def __init__(self, patterns):
        self.patterns = patterns

    def matches(self, ctx, obj):
        # Match the sequence backwards as we "parent" upwards
        pattno = len(self.patterns) - 1
        while pattno >= 0:
            pattern = self.patterns[pattno]
            if not pattern.matches(ctx, obj):
                return False

            try:
                obj = ctx.parent(obj)
            except KeyError:
                return False
            if obj is None:
                return False

            pattno -= 1
        return True

    def pull(self, ctx, obj):
        pool = {id(obj): obj}
        for pattern in self.patterns:
            if not pool:
                return
            newpool = {}
            for o in pool.values():
                for oo in pattern.pull(ctx, o):
                    newpool[id(oo)] = oo
            pool = newpool

        return iter(pool.values())


class Ancestor(Pattern):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def matches(self, ctx, obj):
        if obj is not ctx.root and self.right.matches(ctx, obj):
            par = ctx.parent(obj)
            while par is not None:
                if self.left.matches(ctx, par):
                    return True
                par = ctx.parent(par)

    def pull(self, ctx, obj):
        left = self.left
        right = self.right

        def recurse(this):
            if this is None:
                return

            # Find matches from here
            for match in right.pull(ctx, this):
                yield match

            # Recurse on list/dict children
            it = None
            if isinstance(this, list):
                it = this
            elif isinstance(this, dict):
                it = this.values()
            if it:
                for item in it:
                    for submatch in recurse(item):
                        yield submatch

        for o in left.pull(ctx, obj):
            for oo in recurse(o):
                yield oo


class App(Pattern):
    def __init__(self, name, patterns):
        self.name = name
        self.patterns = patterns

    def __repr__(self):
        return "%s(%r, %r)" % (type(self).__name__, self.name, self.patterns)

    def matches(self, ctx, obj):
        # It doesn't make sense to put an application in a match
        return False

    def pull(self, ctx, obj):
        fn = ctx.get(self.name)
        if fn:
            args = [list(pattern.pull(ctx, obj)) for pattern in self.patterns]
            # Avenue functions should always return a generator, so yield from
            # that
            for o in fn(*args):
                yield o


pattern_dict = {
    "Root": Root,
    "Lookup": Lookup,
    "Star": Star,
    "Comparison": Comparison,
    "Predicate": Predicate,
    "Union": Union,
    "Filter": Filter,
    "Action": Action,
    "Child": Child,
    "Sequence": Sequence,
    "Ancestor": Ancestor,
    "App": App,
}
