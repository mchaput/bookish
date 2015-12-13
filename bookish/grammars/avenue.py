#encoding: utf8

import re
from bookish import compat
from bookish.parser.builder import _fill_args
from bookish.parser.parser import make_grammar
from bookish.parser.parser import Empty, Failure, Miss
from bookish.parser.parser import ParserError
from bookish.parser import rules as r

import bookish.avenue.patterns as pt


# Any
def Any(stream, i, context):
    if i >= len(stream) or stream.startswith(u"\uffff", i):
        return Miss, i
    else:
        return stream[i], i + 1


# (<((~Su'"') Any)+>):s
def _r_bind_4475773328(stream, i, context):
    out, i = _r_take_4475775504(stream, i, context)
    if out is not Miss:
        context[u's'] = out
    return out, i


# (<$digit+>):ds
def _r_bind_4475773520(stream, i, context):
    out, i = _r_take_4475773968(stream, i, context)
    if out is not Miss:
        context[u'ds'] = out
    return out, i


# ($barenum):x
def _r_bind_4475775376(stream, i, context):
    out, i = barenum(stream, i, context)
    if out is not Miss:
        context[u'x'] = out
    return out, i


# ($barenum):x
def _r_bind_4475776080(stream, i, context):
    out, i = barenum(stream, i, context)
    if out is not Miss:
        context[u'x'] = out
    return out, i


# (($ws Su':' $ws $number)?):j
def _r_bind_4475776144(stream, i, context):
    out, i = _r_opt_4475775824(stream, i, context)
    if out is not Miss:
        context[u'j'] = out
    return out, i


# (<((~Su"'") Any)+>):s
def _r_bind_4475776272(stream, i, context):
    out, i = _r_take_4475776528(stream, i, context)
    if out is not Miss:
        context[u's'] = out
    return out, i


# ($number):i
def _r_bind_4475776720(stream, i, context):
    out, i = number(stream, i, context)
    if out is not Miss:
        context[u'i'] = out
    return out, i


# (($string | $name)):s
def _r_bind_4481032272(stream, i, context):
    out, i = _r_or_4481033808(stream, i, context)
    if out is not Miss:
        context[u's'] = out
    return out, i


# (<((~Su'/') Any)+>):r
def _r_bind_4481032912(stream, i, context):
    out, i = _r_take_4481033936(stream, i, context)
    if out is not Miss:
        context[u'r'] = out
    return out, i


# ((Su'==' | Su'=' | Su'<=' | Su'>=' | Su'<' | Su'>' | Su'!=' | Su'=~')):op
def _r_bind_4481033168(stream, i, context):
    out, i = _r_or_4481035472(stream, i, context)
    if out is not Miss:
        context[u'op'] = out
    return out, i


# ($name):n
def _r_bind_4481033296(stream, i, context):
    out, i = name(stream, i, context)
    if out is not Miss:
        context[u'n'] = out
    return out, i


# ($literal):v
def _r_bind_4481035088(stream, i, context):
    out, i = literal(stream, i, context)
    if out is not Miss:
        context[u'v'] = out
    return out, i


# ($actionexpr):src
def _r_bind_4481035216(stream, i, context):
    out, i = actionexpr(stream, i, context)
    if out is not Miss:
        context[u'src'] = out
    return out, i


# ($actionexpr):src
def _r_bind_4481036240(stream, i, context):
    out, i = actionexpr(stream, i, context)
    if out is not Miss:
        context[u'src'] = out
    return out, i


# (($ws Su',' $expr)*):es
def _r_bind_4481040656(stream, i, context):
    out, i = _r_star_4481042256(stream, i, context)
    if out is not Miss:
        context[u'es'] = out
    return out, i


# ($expr):e
def _r_bind_4481041936(stream, i, context):
    out, i = expr(stream, i, context)
    if out is not Miss:
        context[u'e'] = out
    return out, i


# ($name):n
def _r_bind_4481042192(stream, i, context):
    out, i = name(stream, i, context)
    if out is not Miss:
        context[u'n'] = out
    return out, i


# ($expr):e
def _r_bind_4481042320(stream, i, context):
    out, i = expr(stream, i, context)
    if out is not Miss:
        context[u'e'] = out
    return out, i


# ($expr):e
def _r_bind_4481042704(stream, i, context):
    out, i = expr(stream, i, context)
    if out is not Miss:
        context[u'e'] = out
    return out, i


# ($args):args
def _r_bind_4481042832(stream, i, context):
    out, i = args(stream, i, context)
    if out is not Miss:
        context[u'args'] = out
    return out, i


# ($expr):e
def _r_bind_4481044240(stream, i, context):
    out, i = expr(stream, i, context)
    if out is not Miss:
        context[u'e'] = out
    return out, i


# ($expr1):e1
def _r_bind_4481044368(stream, i, context):
    out, i = expr1(stream, i, context)
    if out is not Miss:
        context[u'e1'] = out
    return out, i


# (($ws Su'|' $expr2)*):e2s
def _r_bind_4481291216(stream, i, context):
    out, i = _r_star_4481291984(stream, i, context)
    if out is not Miss:
        context[u'e2s'] = out
    return out, i


# ($expr):e
def _r_bind_4481291472(stream, i, context):
    out, i = expr(stream, i, context)
    if out is not Miss:
        context[u'e'] = out
    return out, i


# ($expr1):e1
def _r_bind_4481291536(stream, i, context):
    out, i = expr1(stream, i, context)
    if out is not Miss:
        context[u'e1'] = out
    return out, i


# ($expr2):e2
def _r_bind_4481291664(stream, i, context):
    out, i = expr2(stream, i, context)
    if out is not Miss:
        context[u'e2'] = out
    return out, i


# ($expr):e
def _r_bind_4481291728(stream, i, context):
    out, i = expr(stream, i, context)
    if out is not Miss:
        context[u'e'] = out
    return out, i


# ->(int(ds))
def _r_do_4475773648(stream, i, context):
    # int(ds)
    return eval(_r_do_4475773648_code, globals(), context), i


# ->(s)
def _r_do_4475775440(stream, i, context):
    # s
    return eval(_r_do_4475775440_code, globals(), context), i


# ->(s)
def _r_do_4475775760(stream, i, context):
    # s
    return eval(_r_do_4475775760_code, globals(), context), i


# ->(-x)
def _r_do_4475776016(stream, i, context):
    # -x
    return eval(_r_do_4475776016_code, globals(), context), i


# ->(x)
def _r_do_4475776400(stream, i, context):
    # x
    return eval(_r_do_4475776400_code, globals(), context), i


# ->(pt.Lookup(s))
def _r_do_4481033424(stream, i, context):
    # pt.Lookup(s)
    return eval(_r_do_4481033424_code, globals(), context), i


# ->(pt.Slice(i, j[0] if j else None))
def _r_do_4481033488(stream, i, context):
    # pt.Slice(i, j[0] if j else None)
    return eval(_r_do_4481033488_code, globals(), context), i


# ->(Star())
def _r_do_4481034640(stream, i, context):
    # Star()
    return eval(_r_do_4481034640_code, globals(), context), i


# ->(pt.Regex(r))
def _r_do_4481034704(stream, i, context):
    # pt.Regex(r)
    return eval(_r_do_4481034704_code, globals(), context), i


# ->(pt.Comparison(n, op, v))
def _r_do_4481036048(stream, i, context):
    # pt.Comparison(n, op, v)
    return eval(_r_do_4481036048_code, globals(), context), i


# ->(pt.Action(src))
def _r_do_4481040592(stream, i, context):
    # pt.Action(src)
    return eval(_r_do_4481040592_code, globals(), context), i


# ->(pt.Predicate(src))
def _r_do_4481040912(stream, i, context):
    # pt.Predicate(src)
    return eval(_r_do_4481040912_code, globals(), context), i


# ->([])
def _r_do_4481040976(stream, i, context):
    # []
    return eval(_r_do_4481040976_code, globals(), context), i


# ->(Root())
def _r_do_4481042064(stream, i, context):
    # Root()
    return eval(_r_do_4481042064_code, globals(), context), i


# ->([e] + es)
def _r_do_4481042512(stream, i, context):
    # [e] + es
    return eval(_r_do_4481042512_code, globals(), context), i


# ->(pt.App(n, args))
def _r_do_4481043088(stream, i, context):
    # pt.App(n, args)
    return eval(_r_do_4481043088_code, globals(), context), i


# ->(e)
def _r_do_4481043536(stream, i, context):
    # e
    return eval(_r_do_4481043536_code, globals(), context), i


# ->(pt.Filter(e))
def _r_do_4481044048(stream, i, context):
    # pt.Filter(e)
    return eval(_r_do_4481044048_code, globals(), context), i


# ->(pt.Ancestor(e1, e))
def _r_do_4481291280(stream, i, context):
    # pt.Ancestor(e1, e)
    return eval(_r_do_4481291280_code, globals(), context), i


# ->(pt.Child(e1, e))
def _r_do_4481292112(stream, i, context):
    # pt.Child(e1, e)
    return eval(_r_do_4481292112_code, globals(), context), i


# ->(pt.Union([e2] + e2s) if e2s else e2)
def _r_do_4481292432(stream, i, context):
    # pt.Union([e2] + e2s) if e2s else e2
    return eval(_r_do_4481292432_code, globals(), context), i


# ->(e)
def _r_do_4481292880(stream, i, context):
    # e
    return eval(_r_do_4481292880_code, globals(), context), i


# (~Su'"')
def _r_not_4481033616(stream, i, context):
    return (Empty if _r_string_4481034000(stream, i, context)[0] is Miss else Miss), i


# (~Su"'")
def _r_not_4481034448(stream, i, context):
    return (Empty if _r_string_4481034896(stream, i, context)[0] is Miss else Miss), i


# (~Su'/')
def _r_not_4481040848(stream, i, context):
    return (Empty if _r_string_4481041232(stream, i, context)[0] is Miss else Miss), i


# ($ws Su':' $ws $number)?
def _r_opt_4475775824(stream, i, context):
    out, newi = _r_seq_4481032592(stream, i, context)
    if out is Miss:
        return [], i
    else:
        return [out], newi


# (Su' ' | S'\t')
def _r_or_4475773776(stream, i, context):
    fm = _r_or_4475773776_fm
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


# ((Su'-' ($barenum):x ->(-x)) | (($barenum):x ->(x)))
def _r_or_4475774416(stream, i, context):
    fm = _r_or_4475774416_fm
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


# (Su'_' | $ascii_letter)
def _r_or_4475776592(stream, i, context):
    fm = _r_or_4475776592_fm
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


# (Su'_' | $ascii_letter | $digit)
def _r_or_4475776656(stream, i, context):
    fm = _r_or_4475776656_fm
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


# ($string | $name)
def _r_or_4481033808(stream, i, context):
    fm = _r_or_4481033808_fm
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


# (Su'==' | Su'=' | Su'<=' | Su'>=' | Su'<' | Su'>' | Su'!=' | Su'=~')
def _r_or_4481035472(stream, i, context):
    fm = _r_or_4481035472_fm
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


# $digit+
def _r_plus_4475775056(stream, i, context):
    target = digit
    _i = i
    times = 0
    output = []
    length = len(stream)
    maxtimes = None
    mintimes = 1
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


# ((~Su'"') Any)+
def _r_plus_4475776464(stream, i, context):
    target = _r_seq_4481032400
    _i = i
    times = 0
    output = []
    length = len(stream)
    maxtimes = None
    mintimes = 1
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


# ((~Su"'") Any)+
def _r_plus_4481032336(stream, i, context):
    target = _r_seq_4481033680
    _i = i
    times = 0
    output = []
    length = len(stream)
    maxtimes = None
    mintimes = 1
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


# ((~Su'/') Any)+
def _r_plus_4481035536(stream, i, context):
    target = _r_seq_4481035920
    _i = i
    times = 0
    output = []
    length = len(stream)
    maxtimes = None
    mintimes = 1
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


# (Su"'" (<((~Su"'") Any)+>):s Su"'" ->(s))
def _r_seq_4475773008(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4475774224, _r_bind_4475776272, _r_string_4475775888, _r_do_4475775760):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'"' (<((~Su'"') Any)+>):s Su'"' ->(s))
def _r_seq_4475773072(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4475775312, _r_bind_4475773328, _r_string_4475776336, _r_do_4475775440):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((Su'_' | $ascii_letter) (Su'_' | $ascii_letter | $digit)*)
def _r_seq_4475773712(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_or_4475776592, _r_star_4475775952):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'-' ($barenum):x ->(-x))
def _r_seq_4475774672(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4475775696, _r_bind_4475775376, _r_do_4475776016):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (($barenum):x ->(x))
def _r_seq_4475775248(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4475776080, _r_do_4475776400):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((~Su'"') Any)
def _r_seq_4481032400(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_not_4481033616, Any):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ($ws Su':' $ws $number)
def _r_seq_4481032592(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481034128, ws, number):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (($expr):e (($ws Su',' $expr)*):es ->([e] + es))
def _r_seq_4481032784(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481041936, _r_bind_4481040656, _r_do_4481042512):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((~Su"'") Any)
def _r_seq_4481033680(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_not_4481034448, Any):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((~Su'/') Any)
def _r_seq_4481035920(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_not_4481040848, Any):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (($expr1):e1 $ws Su'..' ($expr):e ->(pt.Ancestor(e1, e)))
def _r_seq_4481042384(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481044368, ws, _r_string_4481290384, _r_bind_4481044240, _r_do_4481291280):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ($ws Su',' $expr)
def _r_seq_4481042640(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481043280, expr):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (($expr1):e1 $ws Su'.' ($expr):e ->(pt.Child(e1, e)))
def _r_seq_4481043024(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481291536, ws, _r_string_4481291792, _r_bind_4481291472, _r_do_4481292112):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ($ws Su'|' $expr2)
def _r_seq_4481292496(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481293136, expr2):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'_' | $ascii_letter | $digit)*
def _r_star_4475775952(stream, i, context):
    target = _r_or_4475776656
    _i = i
    times = 0
    output = []
    length = len(stream)
    maxtimes = None
    mintimes = 0
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


# ($ws Su',' $expr)*
def _r_star_4481042256(stream, i, context):
    target = _r_seq_4481042640
    _i = i
    times = 0
    output = []
    length = len(stream)
    maxtimes = None
    mintimes = 0
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


# ($ws Su'|' $expr2)*
def _r_star_4481291984(stream, i, context):
    target = _r_seq_4481292496
    _i = i
    times = 0
    output = []
    length = len(stream)
    maxtimes = None
    mintimes = 0
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


# Su"'"
def _r_string_4475774224(stream, i, context):
    string = u"'"
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su' '
def _r_string_4475774736(stream, i, context):
    string = u' '
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\t'
def _r_string_4475774992(stream, i, context):
    string = '\t'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'"'
def _r_string_4475775312(stream, i, context):
    string = u'"'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'-'
def _r_string_4475775696(stream, i, context):
    string = u'-'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su"'"
def _r_string_4475775888(stream, i, context):
    string = u"'"
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'"'
def _r_string_4475776336(stream, i, context):
    string = u'"'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'/'
def _r_string_4481032464(stream, i, context):
    string = u'/'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'_'
def _r_string_4481032656(stream, i, context):
    string = u'_'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'_'
def _r_string_4481033104(stream, i, context):
    string = u'_'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'/'
def _r_string_4481033872(stream, i, context):
    string = u'/'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'"'
def _r_string_4481034000(stream, i, context):
    string = u'"'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su':'
def _r_string_4481034128(stream, i, context):
    string = u':'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su"'"
def _r_string_4481034896(stream, i, context):
    string = u"'"
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'*'
def _r_string_4481035344(stream, i, context):
    string = u'*'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'@'
def _r_string_4481035600(stream, i, context):
    string = u'@'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'?('
def _r_string_4481035728(stream, i, context):
    string = u'?('
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su')'
def _r_string_4481040528(stream, i, context):
    string = u')'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'{'
def _r_string_4481040784(stream, i, context):
    string = u'{'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'=='
def _r_string_4481041040(stream, i, context):
    string = u'=='
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'<='
def _r_string_4481041168(stream, i, context):
    string = u'<='
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'/'
def _r_string_4481041232(stream, i, context):
    string = u'/'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'>='
def _r_string_4481041296(stream, i, context):
    string = u'>='
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'='
def _r_string_4481041360(stream, i, context):
    string = u'='
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'<'
def _r_string_4481041424(stream, i, context):
    string = u'<'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'>'
def _r_string_4481041488(stream, i, context):
    string = u'>'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'!='
def _r_string_4481041552(stream, i, context):
    string = u'!='
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'=~'
def _r_string_4481041680(stream, i, context):
    string = u'=~'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'}'
def _r_string_4481041872(stream, i, context):
    string = u'}'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'$'
def _r_string_4481042000(stream, i, context):
    string = u'$'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'('
def _r_string_4481042896(stream, i, context):
    string = u'('
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'('
def _r_string_4481043152(stream, i, context):
    string = u'('
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su','
def _r_string_4481043280(stream, i, context):
    string = u','
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su')'
def _r_string_4481043664(stream, i, context):
    string = u')'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su')'
def _r_string_4481043920(stream, i, context):
    string = u')'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'['
def _r_string_4481044112(stream, i, context):
    string = u'['
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su']'
def _r_string_4481044304(stream, i, context):
    string = u']'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'..'
def _r_string_4481290384(stream, i, context):
    string = u'..'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'.'
def _r_string_4481291792(stream, i, context):
    string = u'.'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'|'
def _r_string_4481293136(stream, i, context):
    string = u'|'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# <$digit+>
def _r_take_4475773968(stream, i, context):
    _i = i
    out, i = _r_plus_4475775056(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# <((~Su'"') Any)+>
def _r_take_4475775504(stream, i, context):
    _i = i
    out, i = _r_plus_4475776464(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# <((~Su"'") Any)+>
def _r_take_4475776528(stream, i, context):
    _i = i
    out, i = _r_plus_4481032336(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# <((~Su'/') Any)+>
def _r_take_4481033936(stream, i, context):
    _i = i
    out, i = _r_plus_4481035536(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# $action
def action(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481040784, _r_bind_4481036240, _r_string_4481041872, _r_do_4481040592):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $actionexpr
def actionexpr(stream, i, context):
    expression, newi = r.PythonExpr.take_python_expr(stream, i, ')')
    if expression:
        return expression, newi
    else:
        return Miss, i


# $application
def application(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481042192, _r_string_4481042896, _r_bind_4481042832, _r_string_4481043664, _r_do_4481043088):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $args
def args(stream, i, context):
    fm = args_fm
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


# $ascii_letter
def ascii_letter(stream, i, context):
    __xs = u'ACBEDGFIHKJMLONQPSRUTWVYXZacbedgfihkjmlonqpsrutwvyxz'
    if i < len(stream) and stream[i] in __xs:
        return stream[i], i + 1
    else:
        return Miss, i


# $barenum
def barenum(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4475773520, _r_do_4475773648):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $brackets
def brackets(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481043152, _r_bind_4481042320, _r_string_4481043920, _r_do_4481043536):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $digit
def digit(stream, i, context):
    __xs = u'1032547698'
    if i < len(stream) and stream[i] in __xs:
        return stream[i], i + 1
    else:
        return Miss, i


# $expr
def expr(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481291664, _r_bind_4481291216, _r_do_4481292432):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $expr1
def expr1(stream, i, context):
    fm = expr1_fm
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


# $expr2
def expr2(stream, i, context):
    fm = expr2_fm
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


# $filter
def filter(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481044112, _r_bind_4481042704, _r_string_4481044304, _r_do_4481044048):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $grammar
def grammar(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481291728, ws, streamend, _r_do_4481292880):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $index
def index(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4475776720, _r_bind_4475776144, _r_do_4481033488):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $literal
def literal(stream, i, context):
    fm = literal_fm
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


# $lookup
def lookup(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_bind_4481032272, _r_do_4481033424):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $name
def name(stream, i, context):
    _i = i
    out, i = _r_seq_4475773712(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# $number
def number(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_or_4475774416):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $predicate
def predicate(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481035728, _r_bind_4481035216, _r_string_4481040528, _r_do_4481040912):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $regex
def regex(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481033872, _r_bind_4481032912, _r_string_4481032464, _r_do_4481034704):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $root
def root(stream, i, context):
    out = Miss
    _i = i
    for rule in (ws, _r_string_4481042000, _r_do_4481042064):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $star
def star(stream, i, context):
    out = Miss
    _i = i
    for rule in (ws, _r_string_4481035344, _r_do_4481034640):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $streamend
def streamend(stream, i, context):
    return r.StreamEnd._accept(stream, i)


# $string
def string(stream, i, context):
    fm = string_fm
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


# $test
def test(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481035600, _r_bind_4481033296, ws, _r_bind_4481033168, ws, _r_bind_4481035088, _r_do_4481036048):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $ws
def ws(stream, i, context):
    target = _r_or_4475773776
    _i = i
    times = 0
    output = []
    length = len(stream)
    maxtimes = None
    mintimes = 0
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


# 151 functions


_r_do_4475773648_code = r.compile_expr(u'int(ds)')
_r_do_4475775440_code = r.compile_expr(u's')
_r_do_4475775760_code = r.compile_expr(u's')
_r_do_4475776016_code = r.compile_expr(u'-x')
_r_do_4475776400_code = r.compile_expr(u'x')
_r_do_4481033424_code = r.compile_expr(u'pt.Lookup(s)')
_r_do_4481033488_code = r.compile_expr(u'pt.Slice(i, j[0] if j else None)')
_r_do_4481034640_code = r.compile_expr(u'Star()')
_r_do_4481034704_code = r.compile_expr(u'pt.Regex(r)')
_r_do_4481036048_code = r.compile_expr(u'pt.Comparison(n, op, v)')
_r_do_4481040592_code = r.compile_expr(u'pt.Action(src)')
_r_do_4481040912_code = r.compile_expr(u'pt.Predicate(src)')
_r_do_4481040976_code = r.compile_expr(u'[]')
_r_do_4481042064_code = r.compile_expr(u'Root()')
_r_do_4481042512_code = r.compile_expr(u'[e] + es')
_r_do_4481043088_code = r.compile_expr(u'pt.App(n, args)')
_r_do_4481043536_code = r.compile_expr(u'e')
_r_do_4481044048_code = r.compile_expr(u'pt.Filter(e)')
_r_do_4481291280_code = r.compile_expr(u'pt.Ancestor(e1, e)')
_r_do_4481292112_code = r.compile_expr(u'pt.Child(e1, e)')
_r_do_4481292432_code = r.compile_expr(u'pt.Union([e2] + e2s) if e2s else e2')
_r_do_4481292880_code = r.compile_expr(u'e')
_r_or_4475773776_fm = {
    None: [],
    '\t': [(_r_string_4475774992, False)],
    u' ': [(_r_string_4475774736, False)],
}
_r_or_4475774416_fm = {
    None: [],
    u'-': [(_r_seq_4475774672, True)],
    u'0': [(_r_seq_4475775248, True)],
    u'1': [(_r_seq_4475775248, True)],
    u'2': [(_r_seq_4475775248, True)],
    u'3': [(_r_seq_4475775248, True)],
    u'4': [(_r_seq_4475775248, True)],
    u'5': [(_r_seq_4475775248, True)],
    u'6': [(_r_seq_4475775248, True)],
    u'7': [(_r_seq_4475775248, True)],
    u'8': [(_r_seq_4475775248, True)],
    u'9': [(_r_seq_4475775248, True)],
}
_r_or_4475776592_fm = {
    None: [],
    u'A': [(ascii_letter, False)],
    u'B': [(ascii_letter, False)],
    u'C': [(ascii_letter, False)],
    u'D': [(ascii_letter, False)],
    u'E': [(ascii_letter, False)],
    u'F': [(ascii_letter, False)],
    u'G': [(ascii_letter, False)],
    u'H': [(ascii_letter, False)],
    u'I': [(ascii_letter, False)],
    u'J': [(ascii_letter, False)],
    u'K': [(ascii_letter, False)],
    u'L': [(ascii_letter, False)],
    u'M': [(ascii_letter, False)],
    u'N': [(ascii_letter, False)],
    u'O': [(ascii_letter, False)],
    u'P': [(ascii_letter, False)],
    u'Q': [(ascii_letter, False)],
    u'R': [(ascii_letter, False)],
    u'S': [(ascii_letter, False)],
    u'T': [(ascii_letter, False)],
    u'U': [(ascii_letter, False)],
    u'V': [(ascii_letter, False)],
    u'W': [(ascii_letter, False)],
    u'X': [(ascii_letter, False)],
    u'Y': [(ascii_letter, False)],
    u'Z': [(ascii_letter, False)],
    u'_': [(_r_string_4481032656, False)],
    u'a': [(ascii_letter, False)],
    u'b': [(ascii_letter, False)],
    u'c': [(ascii_letter, False)],
    u'd': [(ascii_letter, False)],
    u'e': [(ascii_letter, False)],
    u'f': [(ascii_letter, False)],
    u'g': [(ascii_letter, False)],
    u'h': [(ascii_letter, False)],
    u'i': [(ascii_letter, False)],
    u'j': [(ascii_letter, False)],
    u'k': [(ascii_letter, False)],
    u'l': [(ascii_letter, False)],
    u'm': [(ascii_letter, False)],
    u'n': [(ascii_letter, False)],
    u'o': [(ascii_letter, False)],
    u'p': [(ascii_letter, False)],
    u'q': [(ascii_letter, False)],
    u'r': [(ascii_letter, False)],
    u's': [(ascii_letter, False)],
    u't': [(ascii_letter, False)],
    u'u': [(ascii_letter, False)],
    u'v': [(ascii_letter, False)],
    u'w': [(ascii_letter, False)],
    u'x': [(ascii_letter, False)],
    u'y': [(ascii_letter, False)],
    u'z': [(ascii_letter, False)],
}
_r_or_4475776656_fm = {
    None: [],
    u'0': [(digit, False)],
    u'1': [(digit, False)],
    u'2': [(digit, False)],
    u'3': [(digit, False)],
    u'4': [(digit, False)],
    u'5': [(digit, False)],
    u'6': [(digit, False)],
    u'7': [(digit, False)],
    u'8': [(digit, False)],
    u'9': [(digit, False)],
    u'A': [(ascii_letter, False)],
    u'B': [(ascii_letter, False)],
    u'C': [(ascii_letter, False)],
    u'D': [(ascii_letter, False)],
    u'E': [(ascii_letter, False)],
    u'F': [(ascii_letter, False)],
    u'G': [(ascii_letter, False)],
    u'H': [(ascii_letter, False)],
    u'I': [(ascii_letter, False)],
    u'J': [(ascii_letter, False)],
    u'K': [(ascii_letter, False)],
    u'L': [(ascii_letter, False)],
    u'M': [(ascii_letter, False)],
    u'N': [(ascii_letter, False)],
    u'O': [(ascii_letter, False)],
    u'P': [(ascii_letter, False)],
    u'Q': [(ascii_letter, False)],
    u'R': [(ascii_letter, False)],
    u'S': [(ascii_letter, False)],
    u'T': [(ascii_letter, False)],
    u'U': [(ascii_letter, False)],
    u'V': [(ascii_letter, False)],
    u'W': [(ascii_letter, False)],
    u'X': [(ascii_letter, False)],
    u'Y': [(ascii_letter, False)],
    u'Z': [(ascii_letter, False)],
    u'_': [(_r_string_4481033104, False)],
    u'a': [(ascii_letter, False)],
    u'b': [(ascii_letter, False)],
    u'c': [(ascii_letter, False)],
    u'd': [(ascii_letter, False)],
    u'e': [(ascii_letter, False)],
    u'f': [(ascii_letter, False)],
    u'g': [(ascii_letter, False)],
    u'h': [(ascii_letter, False)],
    u'i': [(ascii_letter, False)],
    u'j': [(ascii_letter, False)],
    u'k': [(ascii_letter, False)],
    u'l': [(ascii_letter, False)],
    u'm': [(ascii_letter, False)],
    u'n': [(ascii_letter, False)],
    u'o': [(ascii_letter, False)],
    u'p': [(ascii_letter, False)],
    u'q': [(ascii_letter, False)],
    u'r': [(ascii_letter, False)],
    u's': [(ascii_letter, False)],
    u't': [(ascii_letter, False)],
    u'u': [(ascii_letter, False)],
    u'v': [(ascii_letter, False)],
    u'w': [(ascii_letter, False)],
    u'x': [(ascii_letter, False)],
    u'y': [(ascii_letter, False)],
    u'z': [(ascii_letter, False)],
}
_r_or_4481033808_fm = {
    None: [],
    u'"': [(string, True)],
    u"'": [(string, True)],
    u'A': [(name, False)],
    u'B': [(name, False)],
    u'C': [(name, False)],
    u'D': [(name, False)],
    u'E': [(name, False)],
    u'F': [(name, False)],
    u'G': [(name, False)],
    u'H': [(name, False)],
    u'I': [(name, False)],
    u'J': [(name, False)],
    u'K': [(name, False)],
    u'L': [(name, False)],
    u'M': [(name, False)],
    u'N': [(name, False)],
    u'O': [(name, False)],
    u'P': [(name, False)],
    u'Q': [(name, False)],
    u'R': [(name, False)],
    u'S': [(name, False)],
    u'T': [(name, False)],
    u'U': [(name, False)],
    u'V': [(name, False)],
    u'W': [(name, False)],
    u'X': [(name, False)],
    u'Y': [(name, False)],
    u'Z': [(name, False)],
    u'_': [(name, False)],
    u'a': [(name, False)],
    u'b': [(name, False)],
    u'c': [(name, False)],
    u'd': [(name, False)],
    u'e': [(name, False)],
    u'f': [(name, False)],
    u'g': [(name, False)],
    u'h': [(name, False)],
    u'i': [(name, False)],
    u'j': [(name, False)],
    u'k': [(name, False)],
    u'l': [(name, False)],
    u'm': [(name, False)],
    u'n': [(name, False)],
    u'o': [(name, False)],
    u'p': [(name, False)],
    u'q': [(name, False)],
    u'r': [(name, False)],
    u's': [(name, False)],
    u't': [(name, False)],
    u'u': [(name, False)],
    u'v': [(name, False)],
    u'w': [(name, False)],
    u'x': [(name, False)],
    u'y': [(name, False)],
    u'z': [(name, False)],
}
_r_or_4481035472_fm = {
    None: [],
    u'!': [(_r_string_4481041552, False)],
    u'<': [(_r_string_4481041168, False), (_r_string_4481041424, False)],
    u'=': [(_r_string_4481041040, False), (_r_string_4481041360, False), (_r_string_4481041680, False)],
    u'>': [(_r_string_4481041296, False), (_r_string_4481041488, False)],
}
args_fm = {
    None: [(_r_do_4481040976, False)],
    '\t': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u' ': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'"': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'$': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u"'": [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'(': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'*': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'-': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'/': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'0': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'1': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'2': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'3': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'4': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'5': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'6': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'7': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'8': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'9': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'?': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'@': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'A': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'B': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'C': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'D': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'E': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'F': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'G': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'H': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'I': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'J': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'K': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'L': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'M': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'N': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'O': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'P': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'Q': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'R': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'S': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'T': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'U': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'V': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'W': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'X': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'Y': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'Z': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'[': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'_': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'a': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'b': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'c': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'd': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'e': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'f': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'g': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'h': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'i': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'j': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'k': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'l': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'm': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'n': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'o': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'p': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'q': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'r': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u's': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u't': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'u': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'v': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'w': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'x': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'y': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'z': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
    u'{': [(_r_seq_4481032784, True), (_r_do_4481040976, False)],
}
expr1_fm = {
    None: [],
    '\t': [(root, False), (index, True), (lookup, True), (regex, True), (star, False), (test, True), (predicate, True), (action, True), (brackets, True)],
    u' ': [(root, False), (index, True), (lookup, True), (regex, True), (star, False), (test, True), (predicate, True), (action, True), (brackets, True)],
    u'"': [(lookup, True)],
    u'$': [(root, False)],
    u"'": [(lookup, True)],
    u'(': [(brackets, True)],
    u'*': [(star, False)],
    u'-': [(index, True)],
    u'/': [(regex, True)],
    u'0': [(index, True)],
    u'1': [(index, True)],
    u'2': [(index, True)],
    u'3': [(index, True)],
    u'4': [(index, True)],
    u'5': [(index, True)],
    u'6': [(index, True)],
    u'7': [(index, True)],
    u'8': [(index, True)],
    u'9': [(index, True)],
    u'?': [(predicate, True)],
    u'@': [(test, True)],
    u'A': [(application, True), (lookup, True)],
    u'B': [(application, True), (lookup, True)],
    u'C': [(application, True), (lookup, True)],
    u'D': [(application, True), (lookup, True)],
    u'E': [(application, True), (lookup, True)],
    u'F': [(application, True), (lookup, True)],
    u'G': [(application, True), (lookup, True)],
    u'H': [(application, True), (lookup, True)],
    u'I': [(application, True), (lookup, True)],
    u'J': [(application, True), (lookup, True)],
    u'K': [(application, True), (lookup, True)],
    u'L': [(application, True), (lookup, True)],
    u'M': [(application, True), (lookup, True)],
    u'N': [(application, True), (lookup, True)],
    u'O': [(application, True), (lookup, True)],
    u'P': [(application, True), (lookup, True)],
    u'Q': [(application, True), (lookup, True)],
    u'R': [(application, True), (lookup, True)],
    u'S': [(application, True), (lookup, True)],
    u'T': [(application, True), (lookup, True)],
    u'U': [(application, True), (lookup, True)],
    u'V': [(application, True), (lookup, True)],
    u'W': [(application, True), (lookup, True)],
    u'X': [(application, True), (lookup, True)],
    u'Y': [(application, True), (lookup, True)],
    u'Z': [(application, True), (lookup, True)],
    u'[': [(filter, True)],
    u'_': [(application, True), (lookup, True)],
    u'a': [(application, True), (lookup, True)],
    u'b': [(application, True), (lookup, True)],
    u'c': [(application, True), (lookup, True)],
    u'd': [(application, True), (lookup, True)],
    u'e': [(application, True), (lookup, True)],
    u'f': [(application, True), (lookup, True)],
    u'g': [(application, True), (lookup, True)],
    u'h': [(application, True), (lookup, True)],
    u'i': [(application, True), (lookup, True)],
    u'j': [(application, True), (lookup, True)],
    u'k': [(application, True), (lookup, True)],
    u'l': [(application, True), (lookup, True)],
    u'm': [(application, True), (lookup, True)],
    u'n': [(application, True), (lookup, True)],
    u'o': [(application, True), (lookup, True)],
    u'p': [(application, True), (lookup, True)],
    u'q': [(application, True), (lookup, True)],
    u'r': [(application, True), (lookup, True)],
    u's': [(application, True), (lookup, True)],
    u't': [(application, True), (lookup, True)],
    u'u': [(application, True), (lookup, True)],
    u'v': [(application, True), (lookup, True)],
    u'w': [(application, True), (lookup, True)],
    u'x': [(application, True), (lookup, True)],
    u'y': [(application, True), (lookup, True)],
    u'z': [(application, True), (lookup, True)],
    u'{': [(action, True)],
}
expr2_fm = {
    None: [],
    '\t': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u' ': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'"': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'$': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u"'": [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'(': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'*': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'-': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'/': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'0': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'1': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'2': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'3': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'4': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'5': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'6': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'7': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'8': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'9': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'?': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'@': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'A': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'B': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'C': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'D': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'E': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'F': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'G': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'H': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'I': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'J': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'K': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'L': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'M': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'N': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'O': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'P': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'Q': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'R': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'S': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'T': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'U': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'V': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'W': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'X': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'Y': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'Z': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'[': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'_': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'a': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'b': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'c': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'd': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'e': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'f': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'g': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'h': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'i': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'j': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'k': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'l': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'm': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'n': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'o': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'p': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'q': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'r': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u's': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u't': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'u': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'v': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'w': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'x': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'y': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'z': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
    u'{': [(_r_seq_4481042384, True), (_r_seq_4481043024, True), (expr1, True)],
}
literal_fm = {
    None: [],
    '\t': [(number, True)],
    u' ': [(number, True)],
    u'"': [(string, True)],
    u"'": [(string, True)],
    u'-': [(number, True)],
    u'0': [(number, True)],
    u'1': [(number, True)],
    u'2': [(number, True)],
    u'3': [(number, True)],
    u'4': [(number, True)],
    u'5': [(number, True)],
    u'6': [(number, True)],
    u'7': [(number, True)],
    u'8': [(number, True)],
    u'9': [(number, True)],
}
string_fm = {
    None: [],
    u'"': [(_r_seq_4475773072, True)],
    u"'": [(_r_seq_4475773008, True)],
}
