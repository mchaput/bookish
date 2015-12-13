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

import re
import sys
from collections import defaultdict

from bookish.parser.parser import ParserContext, ArgError, ParserError
from bookish.parser.parser import Empty, Miss, Failure
from bookish.parser.parser import rules_from_locals
from bookish.compat import string_type


__all__ = ("ensure Rule Wrapper MultiRule Any alphanum streamstart linestart "
           "lineend streamend Match String In Or Seq Not Repeat Opt Star Plus "
           "Peek LookBehind Bind Take Do If Regex Mixed FailIf PythonExpr "
           "appargs Parms Call Call2 valexpr actionexpr"
           ).split()


# Utility functions
def ensure(rule):
    if isinstance(rule, string_type):
        rule = String(rule)
    elif isinstance(rule, Rule):
        pass
    else:
        raise TypeError("%r (%s) is not a rule" % (rule, type(rule)))

    return rule


def is_equal(o1, o2, attrs):
    if not type(o1) is type(o2):
        return False
    return all(getattr(o1, attr) == getattr(o2, attr) for attr in attrs)


def compile_expr(expr):
    return compile(expr, '<string>', 'eval', dont_inherit=True)


def make_rule(name, expr, args, add=False):
    if args:
        expr = Parms(args, expr)
    expr.rulename = name
    return expr


# Base rule classes

class Rule(object):
    def __init__(self, rulename=None, grammarpos=-1):
        self.rulename = rulename
        self.grammarpos = grammarpos
        self.snapped = False

    def __hash__(self):
        raise NotImplementedError(self.__class__)

    def __repr__(self):
        return ("$%s" % self.rulename) if self.rulename else self.repr()

    def __add__(self, other):
        if isinstance(self, Seq) and isinstance(other, Seq):
            return Seq(self.targets + other.targets)
        elif isinstance(self, Seq):
            return Seq(self.targets + [ensure(other)])
        elif isinstance(other, Seq):
            return Seq([self] + other.targets)
        else:
            return Seq([self, ensure(other)])

    def __radd__(self, other):
        if isinstance(self, Seq):
            return Seq([ensure(other)] + self.targets)
        else:
            return Seq([ensure(other), self])

    def __or__(self, other):
        if isinstance(self, Or) and isinstance(other, Or):
            return Or(self.targets + other.targets)
        elif isinstance(self, Or):
            return Or(self.targets + [ensure(other)])
        elif isinstance(other, Or):
            return Or([self] + other.targets)
        else:
            return Or([self, ensure(other)])

    def __ror__(self, other):
        if isinstance(self, Seq):
            return Seq([ensure(other)] + self.targets)
        else:
            return Seq([ensure(other), self])

    def __mul__(self, times):
        return Repeat(self, times, times)

    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        return not self.__eq__(other)

    def __call__(self, stream, i, context):
        return self.accept(stream, i, context)

    def is_atomic(self):
        return True

    def children(self):
        return iter([])

    def repr(self):
        return "%s" % self.__class__.__name__

    def _writeline(self, tab, msg, *args, **kwargs):
        sys.stdout.write("  " * tab)
        sys.stdout.write(msg)
        if args:
            for arg in args:
                sys.stdout.write(" " + str(arg))
        if kwargs:
            for key, value in kwargs.items():
                sys.stdout.write(" " + key + "=" + str(value))
        sys.stdout.write("\n")

    def _writetag(self, tab, targets=None, **kwargs):
        if self.rulename:
            kwargs["name"] = self.rulename
        self._writeline(tab, self.__class__.__name__, **kwargs)
        if targets:
            for target in targets:
                if target.rulename:
                    self._writeline(tab + 1, "::" + target.rulename)
                else:
                    target.dump(tab + 1)

    def dump(self, tab=0):
        self._writetag(tab)

    def getname(self):
        if self.rulename:
            return self.rulename
        else:
            return "_r_%s_%s" % (type(self).__name__.lower(), id(self))

    def accept(self, stream, i, context, level=0):
        raise NotImplementedError

    def build(self, builder):
        raise NotImplementedError

    #

    def test(self, stream, i=0, context=None):
        return self.test2(stream, i, context)[0]

    def test2(self, stream, i=0, context=None):
        context = context if context is not None else ParserContext()
        return self.accept(stream, i, context)

    def fixed_length(self, context):
        return -1

    def is_optional(self):
        return False

    def optional_firsts(self):
        return self.firsts()

    def has_binding(self, builder):
        return False

    def arguments(self):
        return []

    def arity(self):
        return 0

    def firsts(self):
        return None

    def snap(self, context):
        return self


class Wrapper(Rule):
    def __init__(self, target, **kwargs):
        Rule.__init__(self, **kwargs)
        self.target = ensure(target)

    def __hash__(self):
        return hash((self.__class__, self.target))

    def __eq__(self, other):
        return type(self) is type(other) and self.target == other.target

    def is_atomic(self):
        return False

    def children(self):
        yield self.target

    def repr(self):
        return "%s(%r)" % (self.__class__.__name__, self.target)

    def dump(self, tab=0):
        self._writetag(tab, [self.target])

    def is_optional(self):
        return self.target.is_optional()

    def optional_firsts(self):
        return self.target.optional_firsts()

    def has_binding(self, builder):
        return self.target and self.target.has_binding(builder)

    def fixed_length(self, context):
        return self.target.fixed_length(context)

    def firsts(self):
        return self.target.firsts()

    def build(self, builder):
        builder.build_rule(self.target)

    def snap(self, context):
        if self.snapped:
            return self

        self.target = self.target.snap(context)
        assert self.target is not None
        self.snapped = True
        return self


class MultiRule(Rule):
    def __init__(self, targets):
        self.targets = targets

    def __hash__(self):
        return hash((self.__class__, self.targets))

    def _reset(self):
        return

    def __eq__(self, other):
        return type(self) is type(other) and self.targets == other.targets

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, item):
        return self.targets.__getitem__(item)

    def is_atomic(self):
        return False

    def children(self):
        return iter(self.targets)

    def dump(self, tab=0):
        self._writetag(tab, self.targets)

    def has_binding(self, builder):
        return any(target.has_binding(builder) for target in self.targets)

    def is_optional(self):
        return all(t.is_optional() for t in self.targets)

    def fixed_length(self, context):
        length = 0
        for target in self.targets:
            tlen = target.fixed_length(context)
            if tlen < 0:
                return -1
            length += tlen
        return length

    def snap(self, context):
        if self.snapped:
            return self

        self.targets = [t.snap(context) for t in self.targets]
        self._reset()
        self.snapped = True
        return self


# Singleton rules

class SingletonRule(Rule):
    def __hash__(self):
        return hash(self.__class__)

    def __eq__(self, other):
        return type(other) is type(self)


class AnyItem(SingletonRule):
    def accept(self, stream, i, context, level=0):
        if i >= len(stream) or stream.startswith(u"\uffff", i):
            return Miss, lambda: [{"cause": repr(self), "pos": i}]
        else:
            return stream[i], i + 1

    def __repr__(self):
        return "Any"

    def fixed_length(self, context):
        return 1

    def build(self, builder):
        return """
        if i >= len(stream) or stream.startswith(u"\\uffff", i):
            return Miss, i
        else:
            return stream[i], i + 1
        """

    def firsts(self):
        return None


Any = AnyItem()


class AlphaNum(SingletonRule):
    @staticmethod
    def _accept(stream, i):
        if i < len(stream) and stream[i].isalnum():
            return stream[i], i + 1
        else:
            return Miss, i

    def accept(self, stream, i, context, level=0):
        return self._accept(stream, i)

    def fixed_length(self, context):
        return 1

    def build(self, builder):
        return "return r.AlphaNum._accept(stream, i)"


alphanum = AlphaNum()


class StreamStart(SingletonRule):
    def accept(self, stream, i, context, level=0):
        if i == 0:
            return Empty, i
        else:
            return Miss, lambda: [{"cause": repr(self), "pos": i}]

    def fixed_length(self, context):
        return 0

    def build(self, builder):
        return "return (Empty if i == 0 else Miss), i"


streamstart = StreamStart()


class LineStart(SingletonRule):
    def __eq__(self, other):
        return type(other) is type(self)

    def accept(self, stream, i, context, level=0):
        # tracing = False
        # if tracing:
        #     context.trace(level, i, self)

        if i < len(stream) and not stream.startswith(u"\uffff", i):
            if i == 0 or stream.startswith("\n", i - 1):
                # if tracing:
                #     context.trace_hit(level, i, self, None)
                return Empty, i
        return Miss, lambda: [{"cause": repr(self), "pos": i}]

    def fixed_length(self, context):
        return 0

    def build(self, builder):
        return """
        if i < len(stream) and not stream.startswith(u'\\uffff', i):
            if i == 0 or stream.startswith('\\n', i - 1):
                return Empty, i
        return Miss, i
        """


linestart = LineStart()


class LineEnd(SingletonRule):
    def __eq__(self, other):
        return type(other) is type(self)

    def accept(self, stream, i, context, level=0):
        if i >= len(stream) or stream.startswith(u"\uffff", i):
            return Empty, i

        if stream.startswith("\n", i):
            return "\n", i + 1
        else:
            return Miss, lambda: [{"cause": repr(self), "pos": i}]

    def fixed_length(self, context):
        return 0

    def build(self, builder):
        return """
        if i >= len(stream):
            return Empty, i
        if stream.startswith("\\n", i):
            return "\\n", i + 1
        else:
            return Miss, i
        """

    def firsts(self):
        return "\n\uffff"


lineend = LineEnd()


class StreamEnd(SingletonRule):
    def __eq__(self, other):
        return type(other) is type(self)

    @staticmethod
    def _accept(stream, i):
        if i >= len(stream) or stream.startswith(u"\uffff", i):
            return Empty, i
        else:
            return Miss, i

    @staticmethod
    def at_end(stream, i):
        out, _ = StreamEnd._accept(stream, i)
        return out is not Miss

    def accept(self, stream, i, context, level=0):
        return self._accept(stream, i)

    def fixed_length(self, context):
        return 0

    def build(self,
              builder):
        return """
        return r.StreamEnd._accept(stream, i)
        """

    def firsts(self):
        return u"\uffff"


streamend = StreamEnd()


class BlockBreak(SingletonRule):
    emptylines_expr = re.compile("\n([ \t]*\n)+", re.MULTILINE)
    ws_expr = re.compile("\n( *)")

    @staticmethod
    def _accept(stream, i, context):
        # If we're at the end of the stream, signal a break
        if i >= len(stream) or stream.startswith(u"\uffff", i):
            return Empty, i

        # Only start checking if we're at a newline
        if stream.startswith("\n", i):
            # If this is the last newline in the file, it's a break
            if i + 1 == len(stream) or stream.startswith(u"\uffff", i + 1):
                return "\n", i + 1

            # If there are multiple newlines (possibly separated by whitespace),
            # it's a break
            m = BlockBreak.emptylines_expr.match(stream, i)
            if m:
                return m.group(0), m.end()

            # If the newline is followed by spaces, we'll check if indentation
            # changed
            m = BlockBreak.ws_expr.match(stream, i)
            if m:
                if m.end() == len(stream):
                    return m.group(0), m.end()

                # Get the current indent from the context (the block rule should
                # have stored it)
                current_indent = context.get("indent")
                # "bwidth" contains the width of the bullet/number if we're in a
                # bullet/ord block; add it to the indent
                current_indent += context.get("bwidth", 0)

                next_indent = len(m.group(1))
                # If the indentation after the newline does not equal the
                # current indentation, it's a break
                if next_indent != current_indent:
                    return m.group(0), i + 1

        return Miss, i

    def accept(self, stream, i, context, level=0):
        return self._accept(stream, i, context)

    def build(self, builder):
        return """
        return r.BlockBreak._accept(stream, i, context)
        """

    def firsts(self):
        return u"\n\uffff"


blockbreak = BlockBreak()


# Item based rules

class Match(Rule):
    def __init__(self, item, **kwargs):
        Rule.__init__(self, **kwargs)
        self.match = item

    def __hash__(self):
        return hash((self.__class__, self.match))

    def __eq__(self, other):
        return type(other) is type(self) and self.match == other.match

    def repr(self):
        return "C%r" % self.match

    def dump(self, tab=0):
        self._writetag(tab, match=repr(self.match))

    def accept(self, stream, i, context, level=0):
        tracing = False
        if tracing:
            context.trace(level, i, self)

        item = self.match
        if i < len(stream):
            this = stream[i]
            if this == item:
                if tracing:
                    context.trace_hit(level, i + 1, self, this)
                return this, i + 1

        if tracing:
            context.trace_miss(level, i, self)
        return Miss, lambda: [{"cause": repr(self), "pos": i}]

    def fixed_length(self, context):
        return 1

    def firsts(self):
        return [self.match]

    def build(self, builder):
        return """
        if i < len(stream):
            if stream[i] == %r:
                return stream[i], i + 1
        return Miss
        """ % (self.match,)


class String(Match):
    def __init__(self, string, **kwargs):
        Rule.__init__(self, **kwargs)
        if (isinstance(string, list)
            and all(isinstance(c, str) for c in string)
            and all(len(c) == 1 for c in string)):
            string = "".join(string)
        self.match = string

    def repr(self):
        return "S%r" % self.match

    def accept(self, stream, i, context, level=0):
        string = self.match
        tracing = False
        if tracing:
            context.trace(level, i, self)

        end = i + len(string)
        if stream.startswith(string, i, i + len(string)):
            if tracing:
                context.trace_hit(level, end, self, string)
            return string, end

        if tracing:
            context.trace_miss(level, i, self)
        return Miss, lambda: [{"cause": repr(self), "pos": i}]

    def fixed_length(self, context):
        return len(self.match)

    def firsts(self):
        return [self.match[0]]

    def build(self, builder):
        return """
        string = %r
        if stream.startswith(string, i, i + len(string)):
            return string, i + len(string)
        return Miss, i
        """ % (self.match,)


class In(Match):
    def __init__(self, xs, **kwargs):
        Rule.__init__(self, **kwargs)

        if not isinstance(xs, str):
            allstrs = all(isinstance(x, str) for x in xs)
            if len(xs) < 256 and allstrs and all(len(x) == 1 for x in xs):
                xs = "".join(sorted(xs))
            else:
                xs = frozenset(xs)
        self.match = xs

    def repr(self):
        return "I%r" % self.match

    def accept(self, stream, i, context, level=0):
        xs = self.match
        tracing = False
        if tracing:
            context.trace(level, i, self)

        if i < len(stream):
            item = stream[i]
            if item in xs:
                if tracing:
                    context.trace_hit(level, i + 1, self, item)
                return item, i + 1

        if tracing:
            context.trace_miss(level, i, self)
        return Miss, lambda: [{"cause": repr(self), "pos": i}]

    def fixed_length(self, context):
        return 1

    def firsts(self):
        return self.match

    def build(self, builder):
        xs = self.match
        if all(isinstance(x, string_type) and len(x) == 1 for x in xs):
            xs = "".join(xs)

        return """
        __xs = %r
        if i < len(stream) and stream[i] in __xs:
            return stream[i], i + 1
        else:
            return Miss, i
        """ % (xs,)


class Regex(Match):
    def __init__(self, pattern, **kwargs):
        Rule.__init__(self, **kwargs)
        self.match = pattern
        self.expr = re.compile(pattern, re.UNICODE | re.MULTILINE)

    def __hash__(self):
        return hash((self.__class__, self.match))

    def repr(self):
        return "R(" + self.match + ")"

    def accept(self, stream, i, context, level=0):
        m = self.expr.match(stream, i)
        tracing = False
        if tracing:
            context.trace(level, i, self)

        if m:
            context.update(m.groupdict())
            if tracing:
                context.trace_hit(level, m.end(), self, m.group(0))
            return m.group(0), m.end()

        if tracing:
            context.trace_miss(level, i, self)
        return Miss, lambda: [{"cause": repr(self), "pos": i}]

    def firsts(self):
        return None

    def fixed_length(self, context):
        return -1

    def build(self, builder):
        cv = builder.add_assignment(self, "re",
                                    "re.compile(%r, re.UNICODE | re.MULTILINE)"
                                    % self.match)
        return """
        __m = %s.match(stream, i)
        if __m:
            context.update(__m.groupdict())
            return __m.group(0), __m.end()
        return Miss, i
        """ % (cv,)


# Higher order rules

def make_firstmap(rules):
    # Make a map from first chars to possible matching rules

    # if all(r.firsts() is None for r in rules):
    #     return {None: rules}

    fm = defaultdict(list)
    for r in rules:
        firsts = r.firsts()
        if firsts is None:
            fm[None].append(r)
        else:
            for char in firsts:
                fm[char].append(r)

    always = fm.get(None)
    if always:
        for key in fm:
            if key is not None:
                fm[key].extend(always)
    else:
        fm[None] = ()

    return fm


class Or(MultiRule):
    def __init__(self, targets, **kwargs):
        Rule.__init__(self, **kwargs)
        self.targets = self._normalize(targets)
        self._firstmap = make_firstmap(self.targets)

    def __getstate__(self):
        return {"targets": self.targets}

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._firstmap = make_firstmap(self.targets)

    @staticmethod
    def _normalize(targets):
        # Remove duplicates, merge any Ins and Matches into a single In
        inset = set()
        output = []
        for target in targets:
            target = ensure(target)
            if isinstance(target, Or):
                ts = target.targets
            else:
                ts = [target]
            for t in ts:
                if t in output:
                    continue
                if type(t) is In:
                    inset.update(t.match)
                elif type(t) is Match:
                    inset.add(t.match)
                else:
                    output.append(t)
        if inset:
            output.append(In(inset))

        return output

    def repr(self):
        return "(%s)" % " | ".join(repr(t) for t in self.targets)

    def accept(self, stream, i, context, level=0):
        out = Miss
        causes = []
        tracing = False
        fm = self._firstmap

        if tracing:
            context.trace(level, i, self)

        if i < len(stream):
            targets = fm.get(stream[i], fm[None])
        else:
            targets = self.targets

        if not targets:
            if tracing:
                context.trace_miss(level, i, self, "targets=%r" % targets)
            return out, i
        # targets = self.targets

        for rule in targets:
            c = context.push()
            out, newi = rule.accept(stream, i, c, level + 1)

            if out is not Miss:
                context.update(c.first())
                i = newi
                break
            else:
                causes.append(newi)

        if out is Miss:
            if tracing:
                context.trace_miss(level, i, self)
            return out, lambda: [{"cause": repr(self), "pos": i}]
        else:
            if tracing:
                context.trace_hit(level, i, self, out)
            return out, i

    def build(self, builder):
        firstmap = make_firstmap(self.targets)

        for t in self.targets:
            builder.build_rule(t)

        if firstmap:
            fmcode = "{\n"
            fmitems = sorted(firstmap.items(), key=lambda x: x[0] or '')
            for char, rlist in fmitems:
                pairs = ["(%s, %r)" % (builder.qname(r), r.has_binding(builder))
                         for r in rlist]
                nlist = ", ".join(pairs)
                fmcode += "    %r: [%s],\n" % (char, nlist)
            fmcode += "}"
            fm = builder.add_assignment(self, "fm", fmcode)
        else:
            fm = builder.add_assignment(self, "fm", "None")

        return """
        fm = %s
        targets = fm[None]
        if i < len(stream):
            try:
                targets = fm[stream[i]]
            except KeyError:
                pass
        if targets:
            for rule, hasbinding in targets:
                if hasbinding:
                    c = context.push()
                else:
                    c = context
                out, newi = rule(stream, i, c)
                if out is not Miss:
                    if hasbinding:
                        context.update(c.first())
                    return out, newi
        return Miss, i
        """ % (fm,)

    def firsts(self):
        s = set()
        for target in self.targets:
            firsts = target.firsts()
            if firsts is None:
                return None
            s.update(target.firsts())
        return s

    def optional_firsts(self):
        s = set()
        for target in self.targets:
            firsts = target.firsts()
            if firsts:
                s.update(firsts)
        return s if s else None

    def fixed_length(self, context):
        if any(target.fixed_length(context) < 0 for target in self.targets):
            return -1

        length = self.targets[0].fixed_length(context)
        for target in self.targets[1:]:
            if target.fixed_length(context) != length:
                return -1
        return length


class Seq(MultiRule):
    def __init__(self, targets, **kwargs):
        Rule.__init__(self, **kwargs)
        targets = [ensure(target) for target in targets]
        self.targets = []
        for target in targets:
            if isinstance(target, Seq):
                self.targets.extend(target.targets)
            else:
                self.targets.append(target)

    def repr(self):
        return "(%s)" % " ".join(repr(t) for t in self.targets)

    def accept(self, stream, i, context, level=0):
        c = context.push()
        out = Miss
        newi = lambda: []
        tracing = False

        if tracing:
            context.trace(level, i, self)

        for rule in self.targets:
            out, newi = rule.accept(stream, i, c, level + 1)
            if out is Miss:
                break
            i = newi

        if tracing:
            context.trace_hit(level, i, self, out)
        return out, i

    def build(self, builder):
        for t in self.targets:
            builder.build_rule(t)

        names = ", ".join(builder.qname(t) for t in self.targets)
        out = ""
        if self.has_binding(builder):
            out += """
        context = context.push()
        """
        out += """
        out = Miss
        _i = i
        for rule in (%s):
            out, newi = rule(stream, i, context)
            if out is Miss:
                break
            i = newi
        return out, (_i if out is Miss else i)
        """ % (names,)
        return out

    def firsts(self):
        extras = set()
        for target in self.targets:
            if isinstance(target, LookBehind):
                continue

            fs = target.firsts()
            if fs is None and target.fixed_length(None) == 0:
                continue

            if target.is_optional():
                ofs = target.optional_firsts()
                if ofs:
                    extras.update(ofs)
                    continue

            if fs:
                return extras | set(fs)
            else:
                return None

    def fixed_length(self, context):
        length = 0
        for target in self.targets:
            tlen = target.fixed_length(context)
            if tlen < 0:
                return -1
            length += tlen
        return length


class Not(Wrapper):
    def accept(self, stream, i, context, level=0):
        out, newi = self.target.accept(stream, i, context, level + 1)
        if out is Miss:
            return Empty, i
        else:
            return Miss, lambda: [{"cause": repr(self), "pos": i}] + newi()

    def build(self, builder):
        builder.build_rule(self.target)
        return """
        return (Empty if %s(stream, i, context)[0] is Miss else Miss), i
        """ % (builder.qname(self.target))

    def firsts(self):
        return None

    def repr(self):
        return "(~%r)" % self.target

    def fixed_length(self, context):
        return 0


class FailIf(Wrapper):
    def __eq__(self, other):
        return type(other) is type(self) and self.child == other.child

    def accept(self, stream, i, context, level=0):
        out, newi = self.target.accept(stream, i, context, level + 1)
        lm = lambda: [{"cause": repr(self), "pos": i}] + newi()
        if out is not Miss:
            return Failure, lm
        else:
            return Miss, lm

    def build(self, builder):
        builder.build_rule(self.target)
        return """
        return (Failure if %s(stream, i, context)[0] is not Miss else Miss), i
        """ % builder.qname(self.target)

    def firsts(self):
        return self.target.firsts()

    def repr(self):
        return "(fail %r)" % self.target

    def fixed_length(self, context):
        return 0


class Repeat(Wrapper):
    def __init__(self, target, mintimes=1, maxtimes=None, **kwargs):
        Rule.__init__(self, **kwargs)
        self.target = ensure(target)
        self.mintimes = mintimes
        self.maxtimes = maxtimes

    def __eq__(self, other):
        return is_equal(self, other, ("target", "mintimes", "maxtimes"))

    def repr(self):
        if self.mintimes == 0 and self.maxtimes == 1:
            return "%r?" % self.target
        elif self.mintimes == 0 and self.maxtimes is None:
            return "%r*" % self.target
        elif self.mintimes == 1 and self.maxtimes is None:
            return "%r+" % self.target
        elif self.mintimes == self.maxtimes:
            return "%r{%s}" % (self.target, self.mintimes)
        else:
            return "%r{%s, %s}" % (self.target, self.mintimes, self.maxtimes)

    def dump(self, tab=0):
        self._writetag(tab, [self.target], min=self.mintimes, max=self.maxtimes)

    def accept(self, stream, i, context, level=0):
        rule = self.target
        accept = rule.accept
        mintimes = self.mintimes
        maxtimes = self.maxtimes
        tracing = False

        times = 0
        output = []
        length = len(stream)
        newi = lambda: []

        if tracing:
            context.trace(level, i, self)

        while i <= length:
            out, newi = accept(stream, i, context, level + 1)
            if out is Miss:
                break

            if newi <= i:
                if i == length:
                    break
                raise ParserError("%r did not move forward in %r"
                                  % (rule, self))
            i = newi

            if out is not Empty:
                output.append(out)
            times += 1
            if maxtimes and times == maxtimes:
                break

        if times >= mintimes:
            if tracing:
                context.trace_hit(level, i, self, output)
            return output, i
        else:
            if tracing:
                context.trace_miss(level, i, self)
            return Miss, lambda: [{"cause": repr(self), "pos": i}] + newi()

    def build(self, builder):
        builder.build_rule(self.target)
        return """
        target = %s
        _i = i
        times = 0
        output = []
        length = len(stream)
        maxtimes = %s
        mintimes = %s
        while i <= length:
            out, newi = target(stream, i, context)
            if out is Miss:
                break
            if newi <= i:
                if i == length:
                    break
                raise ParserError
            i = newi
            if out is not Empty:
                output.append(out)
            times += 1
            if maxtimes and times == maxtimes:
                break
        if times >= mintimes:
            return output, i
        else:
            return Miss, _i
        """ % (builder.qname(self.target), self.maxtimes, self.mintimes)

    def is_optional(self):
        return self.mintimes == 0

    def fixed_length(self, context):
        tlen = self.target.fixed_length(context)
        if self.mintimes == self.maxtimes and tlen >= 0:
            return tlen * self.mintimes
        return -1

    def firsts(self):
        if self.mintimes < 1:
            return None
        else:
            return self.target.firsts()

    def optional_firsts(self):
        return self.target.firsts()


class Opt(Repeat):
    def __init__(self, target, **kwargs):
        Repeat.__init__(self, target, mintimes=0, maxtimes=1, **kwargs)

    def accept(self, stream, i, context, level=0):
        out, j = self.target.accept(stream, i, context, level + 1)
        if out is Miss:
            return [], i
        else:
            return [out], j

    def build(self, builder):
        builder.build_rule(self.target)
        return """
        out, newi = %s(stream, i, context)
        if out is Miss:
            return [], i
        else:
            return [out], newi
        """ % (builder.qname(self.target),)


class Star(Repeat):
    def __init__(self, target, **kwargs):
        Repeat.__init__(self, target, mintimes=0, **kwargs)


class Plus(Repeat):
    def __init__(self, target, **kwargs):
        Repeat.__init__(self, target, mintimes=1, **kwargs)


class Peek(Wrapper):
    def repr(self):
        return "(~~%r)" % self.target

    def accept(self, stream, i, context, level=0):
        out, _ = self.target.accept(stream, i, context, level + 1)
        return (out if out is Miss else Empty), i

    def build(self, builder):
        builder.build_rule(self.target)
        return """
        return (Miss if %s(stream, i, context)[0] is Miss else Empty), i
        """ % (builder.qname(self.target))

    def fixed_length(self, context):
        return 0


class LookBehind(Wrapper):
    def repr(self):
        return "(^%r)" % self.target

    def dump(self, tab=0):
        self._writetag(tab, [self.target])

    def accept(self, stream, i, context, level=0):
        length = self.target.fixed_length(context)
        assert length >= 0
        start = i - length
        if start < 0:
            return Miss, lambda: [{"cause": repr(self), "pos": i}]

        out, newi = self.target.accept(stream, start, context, level + 1)
        if out is not Miss and i == newi:
            return Empty, i
        else:
            return Miss, newi

    def build(self, builder):
        builder.build_rule(self.target)

        length = self.target.fixed_length(builder.context)
        if length <= 0:
            raise Exception("Rule %r has non-fixed lookbehind" % self)
        lcv = str(length)

        return """
        start = i - %s
        if start >= 0:
            out, newi = %s(stream, start, context)
            if out is not Miss and newi == i:
                return Empty, i
        return Miss, i
        """ % (lcv, builder.qname(self.target))

    def fixed_length(self, context):
        return 0


class Take(Wrapper):
    def accept(self, stream, i, context, level=0):
        start = i
        out, i = self.target.accept(stream, i, context, level + 1)
        if out is Miss:
            return out, i
        return stream[start:i], i

    def build(self, builder):
        builder.build_rule(self.target)
        return """
        _i = i
        out, i = %s(stream, i, context)
        if out is Miss:
            return out, _i
        else:
            return stream[_i:i], i
        """ % (builder.qname(self.target),)

    def repr(self):
        return "<%r>" % self.target


# Data rules

class Bind(Wrapper):
    def __init__(self, name, target, **kwargs):
        Rule.__init__(self, **kwargs)
        self.name = name
        self.target = ensure(target)

    def __hash__(self):
        return hash((self.__class__, self.name, self.target))

    def __eq__(self, other):
        return is_equal(self, other, ("name", "target"))

    def repr(self):
        return "(%r):%s" % (self.target, self.name)

    def dump(self, tab=0):
        self._writetag(tab, [self.target], var=self.name)

    def accept(self, stream, i, context, level=0):
        out, i = self.target.accept(stream, i, context, level + 1)
        if out is not Miss:
            context[self.name] = out
        return out, i

    def build(self, builder):
        builder.build_rule(self.target)
        return """
        out, i = %s(stream, i, context)
        if out is not Miss:
            context[%r] = out
        return out, i
        """ % (builder.qname(self.target), self.name)

    def has_binding(self, builder):
        return True


class Do(Rule):
    def __init__(self, source, **kwargs):
        Rule.__init__(self, **kwargs)
        self.source = source
        self._compile()

    def __hash__(self):
        return hash((self.__class__, self.source))

    def _compile(self):
        self.code = compile_expr(self.source)

    def __getstate__(self):
        return {"source": self.source}

    def __setstate__(self, state):
        self.source = state["source"]
        self._compile()

    def __eq__(self, other):
        return type(self) is type(other) and self.source == other.source

    def repr(self):
        return "->(%s)" % self.source

    def dump(self, tab=0):
        self._writetag(tab, src=self.source)

    def accept(self, stream, i, context, level=0):
        try:
            item = eval(self.code, {}, context)
        except:
            e = sys.exc_info()[1]
            raise type(e)("%s in %r at %s" % (e, self.source, i))
        return item, i

    def build(self, builder):
        cv = builder.add_assignment(self, "code",
                                    "r.compile_expr(%r)" % self.source)
        return """
        # %s
        return eval(%s, globals(), context), i
        """ % (self.source, cv,)

    def fixed_length(self, context):
        return 0


class If(Do):
    def accept(self, stream, i, context, level=0):
        try:
            boolean = eval(self.code, {}, context)
        except:
            e = sys.exc_info()[1]
            raise type(e)("%s in %r at %s" % (e, self.source, i))
        if boolean:
            return Empty, i
        else:
            return Miss, lambda: [{"cause": repr(self), "pos": i}]

    def build(self, builder):
        cv = builder.add_assignment(self, "code",
                                    "r.compile_expr(%r)" % self.source)
        return """
        if eval(%s, globals(), context):
            return Empty, i
        else:
            return Miss, i
        """ % (cv,)

    def repr(self):
        return "?(%s)" % self.source


# Mixed rule

class Mixed(Wrapper):
    def __init__(self, until, target=None, **kwargs):
        Rule.__init__(self, **kwargs)
        self.until = ensure(until)
        self.target = ensure(target) if target else target

    def __hash__(self):
        return hash((self.__class__, self.until, self.target))

    def __eq__(self, other):
        return is_equal(self, other, ("until", "target"))

    def is_atomic(self):
        return False

    def children(self):
        yield self.until
        if self.target:
            yield self.target

    def accept(self, stream, i, context, level=0):
        until = self.until
        target = self.target
        tracing = False

        firsts = None
        output = []
        length = len(stream)
        if stream.endswith(u"\uffff"):
            length -= 1

        context = context.push()

        if target:
            firsts = target.firsts()
        lasti = i

        if tracing:
            context.trace(level, i, self)

        while i < length:
            out, _ = until.accept(stream, i, context, level + 1)
            if out is not Miss:
                break

            if target and (not firsts or stream[i] in firsts):
                out, newi = target.accept(stream, i, context, level + 1)
                if out is Failure:
                    return Miss, lambda: [{"cause": repr(self), "pos": i}] + newi()
                if out is Miss:
                    i += 1
                else:
                    if newi <= i:
                        raise ParserError("%r did not move forward in %r"
                                          % (target, self))
                    if i > lasti:
                        output.append(stream[lasti:i])
                    output.append(out)
                    lasti = i = newi
            else:
                i += 1

        if i > lasti:
            output.append(stream[lasti:i])

        if tracing:
            context.trace_hit(level, i, self, output)
        return output, i

    def build(self, builder):
        builder.build_rule(self.until)
        if self.target:
            builder.build_rule(self.target)

        lines = []
        if self.target:
            lines.append("target = %s" % builder.qname(self.target))
            firsts = self.target.firsts()
            assert firsts, "target=%r type=%s, firsts=%r" % (self.target, type(self.target), firsts)
            chars = ", ".join(repr(c) for c in firsts)
            lines.append("firsts = set((%s))" % chars)

        if self.has_binding(builder):
            lines.append("context = context.push()")

        lines.extend([
            "until = %s" % builder.qname(self.until),
            "lasti = _i = i",
            "length = len(stream)",
            "if stream.endswith(u'\\uffff'):",
            "    length -= 1",
            "output = []",
            "while i < length:",
            "    out, _ = until(stream, i, context)",
            "    if out is not Miss: break",
        ])

        if self.target:
            lines.extend([
                "    if not firsts or stream[i] in firsts:",
                "        out, newi = target(stream, i, context)",
                "        if out is Failure:",
                "            return Miss, _i",
                "        if out is not Miss:",
                "            if newi <= i: raise ParserError",
                "            if i > lasti:",
                "                output.append(stream[lasti:i])",
                "            output.append(out)",
                "            lasti = i = newi",
                "            continue",
            ])

        lines.extend([
            "    i += 1",
            "if i > lasti:",
            "    output.append(stream[lasti:i])",
            "return output, i",
        ])
        return "\n".join(lines)

    def repr(self):
        return "@(%r, %r)" % (self.until, self.target)

    def dump(self, tab=0):
        self._writetag(tab, [self.until, self.target])

    def snap(self, context):
        if self.snapped:
            return self

        self.until = self.until.snap(context)
        if self.target:
            self.target = self.target.snap(context)
        self.snapped = True
        return self


# Python expression taker

class PythonExpr(Rule):
    brackets = {"(": ")", "[": "]", "{": "}"}
    endbrackets = frozenset(brackets.values())

    def __init__(self, ends, **kwargs):
        Rule.__init__(self, **kwargs)
        self.ends = ends

    def __hash__(self):
        return hash((self.__class__, self.ends))

    def __eq__(self, other):
        return type(self) is type(other) and self.ends == other.ends

    @staticmethod
    def take_python_expr(stream, i, ends):
        start = i
        stack = []
        length = len(stream)
        while i < length:
            char = stream[i]

            # Check if we can end here
            if len(stack) == 0 and char in ends:
                break

            # If the char is an open bracket, add it to the stack
            if char in PythonExpr.brackets:
                stack.append((PythonExpr.brackets[char], i))
            # If it's the close bracket we're looking for, pop the stack
            elif stack and char == stack[-1][0]:
                stack.pop()
            # If it's a close bracket we're NOT looking for, no match
            elif char in PythonExpr.endbrackets:
                return None

            # If we're starting a string, loop through chars until we find
            # the end quote
            if char in "\"'":
                strstart = i

                while i < length - 1:
                    i += 1
                    inner = stream[i]
                    if inner == "\\":
                        i += 1
                    elif inner == char:
                        break

                if i >= length:
                    return None, start

            # Move to the next char
            i += 1

        string = stream[start:i]
        if stack:
            ochar, opos = stack[-1]
            raise ParserError("Unmatched %r at %s" % (ochar, opos))
        if not string:
            raise ParserError("Empty Python expression")
        return string, i

    def accept(self, stream, i, context, level=0):
        expression, newi = self.take_python_expr(stream, i, self.ends)
        if expression:
            return expression, newi
        else:
            return Miss, i

    def build(self, builder):
        return """
        expression, newi = r.PythonExpr.take_python_expr(stream, i, %r)
        if expression:
            return expression, newi
        else:
            return Miss, i
        """ % (self.ends,)


# Applications

class ApplicationArgs(SingletonRule):
    def __eq__(self, other):
        return type(self) is type(other)

    @staticmethod
    def take_app_args(stream, i):
        args = []
        length = len(stream)
        start = i

        while i < length:
            try:
                expr, i = PythonExpr.take_python_expr(stream, i, ") ")
            except ParserError:
                return None, start

            if expr:
                args.append(expr)
            else:
                return None, start

            if stream.startswith(")", i):
                break
            elif stream.startswith(" ", i):
                i += 1
            else:
                return Miss, start

        return args, i

    def accept(self, stream, i, context, level=0):
        args, newi = self.take_app_args(stream, i)
        if args is not None:
            return args, newi
        else:
            return Miss, i

    def build(self, builder):
        return """
        args, newi = ApplicationArgs.take_app_args(stream, i)
        if args is not None:
            return args, newi
        else:
            return Miss, i
        """


appargs = ApplicationArgs()


class Parms(Wrapper):
    def __init__(self, args, target, **kwargs):
        Rule.__init__(self, **kwargs)
        self.args = tuple(args)
        self.target = target

    def __eq__(self, other):
        return is_equal(self, other, ("args", "target"))

    def repr(self):
        return "%r(%s)" % (self.target, ", ".join(self.args))

    def accept(self, stream, i, context, level=0):
        return self.target.accept(stream, i, context, level + 1)

    def build(self, builder):
        return self.target.build(builder)

    def arguments(self):
        return self.args

    def arity(self):
        return len(self.args)


class Call(Rule):
    def __init__(self, target, args=None, **kwargs):
        Rule.__init__(self, **kwargs)
        assert isinstance(target, (string_type, Rule)), "Target is %r" % target
        self.target = target
        self.args = tuple(args) if args else ()
        self._snaptarget = None

    def __hash__(self):
        return hash((self.__class__, self.target, self.args))

    def __getstate__(self):
        return {"target": self.target, "args": self.args}

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.snaptarget = None

    def __eq__(self, other):
        return is_equal(self, other, ("args", "target"))

    def repr(self):
        return "%r(%s)" % (self.target, ", ".join(self.args))

    def dump(self, tab=0):
        self._writetag(tab, target=repr(self.target), args=repr(self.args))

    def get_target(self, context):
        _st = self._snaptarget
        if _st:
            return _st

        target = self.target
        if "." in target:
            modulename, rulename = target.split(".", 1)
            module = context[modulename]
            return getattr(module, rulename)

        if isinstance(target, string_type):
            # target = context.rule(target)
            target = context[target]
        if not isinstance(target, Rule):
            raise Exception("Call target %r is not a Rule" % target)

        self._snaptarget = target
        return target

    def has_binding(self, builder):
        if isinstance(self.target, string_type):
            return True
        else:
            return self.target.has_binding(builder)

    def is_optional(self):
        if isinstance(self.target, string_type):
            return False
        else:
            return self.target.is_optional()

    def fixed_length(self, context):
        if context is None:
            return -1
        return self.get_target(context).fixed_length(context)

    def accept(self, stream, i, context, level=0):
        tracing = False
        try:
            target = self.get_target(context)
        except KeyError:
            raise NameError("Unknown call target %r at %d" % (self.target, i))

        # If the call site has arguments, try to relate them to parameters on
        # the callee
        args = self.args
        if args:
            # Check that the number of arguments supplied and required match
            arity = target.arity()
            if len(args) < arity:
                raise ArgError("Not enough arguments to %r" % target)
            elif len(args) > arity:
                raise ArgError("Too many arguments to %r" % target)

            # Create a mapping from argument names to evaluated values
            values = dict((name, eval(arg, {}, context))
                          for name, arg in zip(target.arguments(), args))
            # Push the mapping onto the context
            context = context.push(values)

        if tracing:
            context.trace(level, i, self)
        out, i = target.accept(stream, i, context, level + 1)
        if tracing:
            if out is Miss:
                context.trace_miss(level, i, self)
            else:
                context.trace_hit(level, i, self, out)
        return out, i

    def build(self, builder):
        if isinstance(self.target, string_type):
            n = self.target
        else:
            builder.build_rule(self.target)
            n = builder.qname(self.target)

        if self.args:
            parmnames = builder.args[n]
            assert len(self.args) == len(parmnames)
            arglist = ", ".join(repr(a) for a in self.args)
            return """
            target = %s
            parmnames = %r
            values = [eval(a, globals(), context) for a in [%s]]
            c = _fill_args(context, parmnames, values)
            return target(stream, i, c)
            """ % (n, parmnames, arglist)

    def snap(self, context):
        if self.args:
            return self
        else:
            return self.get_target(context)


class Call2(Call):
    def __init__(self, modulename, rulename, args=None, **kwargs):
        Call.__init__(self, rulename, args, **kwargs)
        self.modulename = modulename

    def __hash__(self):
        return Call.__hash__(self) ^ hash(self.modulename)

    def repr(self):
        return "%r.%r(%s)" % (self.modulename, self.target, ", ".join(self.args))

    def dump(self, tab=0):
        self._writetag(tab, target=repr(self.qname()),
                       args=repr(self.args))

    def get_target(self, context):
        moduleobj = context[self.modulename]
        return getattr(moduleobj, self.target)

    def qname(self):
        return "%s.%s" % (self.modulename, self.target)

    def build(self, builder):
        n = self.qname()
        if self.args:
            arglist = ", ".join(repr(a) for a in self.args)
            return """
            target = %s
            values = [eval(a, globals(), context) for a in (%s)]
            c = self._fill_args(target, context, values)
            return target(stream, i, c)
            """ % (n, arglist)
        else:
            builder.add_alias(self.getname(), n)


valexpr = PythonExpr("\r\n)]")
actionexpr = PythonExpr(")")


basic_rules = rules_from_locals(locals(), __all__)

