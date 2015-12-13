#encoding: utf8

import re
from bookish import compat
from bookish.parser.builder import _fill_args
from bookish.parser.parser import make_grammar
from bookish.parser.parser import Empty, Failure, Miss
from bookish.parser.parser import ParserError
from bookish.parser import rules as r


# (((Su'"' ((u'escchar'() | ((~Su'"') u'r'.u'Any'()))+):s Su'"' ->(s)) | (Su"'" ((u'escchar'() | ((~Su"'") u'r'.u'Any'()))+):s Su"'" ->(s)))):s
def _r_bind_4481291344(stream, i, context):
    out, i = _r_or_4481358096(stream, i, context)
    if out is not Miss:
        context[u's'] = out
    return out, i


# (u'barenum'()):x
def _r_bind_4481292240(stream, i, context):
    out, i = barenum(stream, i, context)
    if out is not Miss:
        context[u'x'] = out
    return out, i


# (<u'hexdigit'()+>):hs
def _r_bind_4481292304(stream, i, context):
    out, i = _r_take_4481293328(stream, i, context)
    if out is not Miss:
        context[u'hs'] = out
    return out, i


# (<u'digit'()+>):ds
def _r_bind_4481293584(stream, i, context):
    out, i = _r_take_4481292048(stream, i, context)
    if out is not Miss:
        context[u'ds'] = out
    return out, i


# (u'barenum'()):x
def _r_bind_4481293648(stream, i, context):
    out, i = barenum(stream, i, context)
    if out is not Miss:
        context[u'x'] = out
    return out, i


# (u'name'()):rule
def _r_bind_4481356048(stream, i, context):
    out, i = name(stream, i, context)
    if out is not Miss:
        context[u'rule'] = out
    return out, i


# ((u'escchar'() | ((~Su']') u'r'.u'Any'()))*):xs
def _r_bind_4481357776(stream, i, context):
    out, i = _r_star_4481358608(stream, i, context)
    if out is not Miss:
        context[u'xs'] = out
    return out, i


# (<(u'hexdigit'() u'hexdigit'())>):d
def _r_bind_4481357840(stream, i, context):
    out, i = _r_take_4481358352(stream, i, context)
    if out is not Miss:
        context[u'd'] = out
    return out, i


# (u'r'.u'Any'()):a
def _r_bind_4481358160(stream, i, context):
    out, i = r.Any(stream, i, context)
    if out is not Miss:
        context[u'a'] = out
    return out, i


# ((u'escchar'() | ((~Su'"') u'r'.u'Any'()))+):s
def _r_bind_4481359184(stream, i, context):
    out, i = _r_plus_4481359312(stream, i, context)
    if out is not Miss:
        context[u's'] = out
    return out, i


# ((u'escchar'() | ((~Su"'") u'r'.u'Any'()))+):s
def _r_bind_4481359440(stream, i, context):
    out, i = _r_plus_4481384656(stream, i, context)
    if out is not Miss:
        context[u's'] = out
    return out, i


# (u'args'()):args
def _r_bind_4481385296(stream, i, context):
    out, i = args(stream, i, context)
    if out is not Miss:
        context[u'args'] = out
    return out, i


# (u'name'()):rule
def _r_bind_4481386192(stream, i, context):
    out, i = name(stream, i, context)
    if out is not Miss:
        context[u'rule'] = out
    return out, i


# (u'r'.u'appargs'()):aa
def _r_bind_4481386576(stream, i, context):
    out, i = r.appargs(stream, i, context)
    if out is not Miss:
        context[u'aa'] = out
    return out, i


# (u'name'()):mod
def _r_bind_4481386640(stream, i, context):
    out, i = name(stream, i, context)
    if out is not Miss:
        context[u'mod'] = out
    return out, i


# (u'args'()):args
def _r_bind_4481387792(stream, i, context):
    out, i = args(stream, i, context)
    if out is not Miss:
        context[u'args'] = out
    return out, i


# (u'r'.u'valexpr'()):code
def _r_bind_4481388240(stream, i, context):
    out, i = r.valexpr(stream, i, context)
    if out is not Miss:
        context[u'code'] = out
    return out, i


# (u'r'.u'actionexpr'()):code
def _r_bind_4481409232(stream, i, context):
    out, i = r.actionexpr(stream, i, context)
    if out is not Miss:
        context[u'code'] = out
    return out, i


# (u'r'.u'actionexpr'()):code
def _r_bind_4481409616(stream, i, context):
    out, i = r.actionexpr(stream, i, context)
    if out is not Miss:
        context[u'code'] = out
    return out, i


# (u'expr1'()):until
def _r_bind_4481409872(stream, i, context):
    out, i = expr1(stream, i, context)
    if out is not Miss:
        context[u'until'] = out
    return out, i


# (((u'ws'() Su',' (u'expr1'()):e ->(e)) | ->(None))):aim
def _r_bind_4481410128(stream, i, context):
    out, i = _r_or_4481410704(stream, i, context)
    if out is not Miss:
        context[u'aim'] = out
    return out, i


# (u'expr1'()):f
def _r_bind_4481410576(stream, i, context):
    out, i = expr1(stream, i, context)
    if out is not Miss:
        context[u'f'] = out
    return out, i


# (u'expr1'()):e
def _r_bind_4481411216(stream, i, context):
    out, i = expr1(stream, i, context)
    if out is not Miss:
        context[u'e'] = out
    return out, i


# (u'expr'()):e
def _r_bind_4481411536(stream, i, context):
    out, i = expr(stream, i, context)
    if out is not Miss:
        context[u'e'] = out
    return out, i


# (u'expr'()):e
def _r_bind_4481411984(stream, i, context):
    out, i = expr(stream, i, context)
    if out is not Miss:
        context[u'e'] = out
    return out, i


# (((~Su'/') ((Su'\\/' ->("/")) | u'r'.u'Any'()))*):pattern
def _r_bind_4481412816(stream, i, context):
    out, i = _r_star_4481429584(stream, i, context)
    if out is not Miss:
        context[u'pattern'] = out
    return out, i


# (u'barenum'()):mn
def _r_bind_4481429712(stream, i, context):
    out, i = barenum(stream, i, context)
    if out is not Miss:
        context[u'mn'] = out
    return out, i


# (((Su',' (u'barenum'() | ->(None))) | ->(mn))):mx
def _r_bind_4481430032(stream, i, context):
    out, i = _r_or_4481432528(stream, i, context)
    if out is not Miss:
        context[u'mx'] = out
    return out, i


# (u'expr2'()):e2
def _r_bind_4481431760(stream, i, context):
    out, i = expr2(stream, i, context)
    if out is not Miss:
        context[u'e2'] = out
    return out, i


# (u'expr1'()):e
def _r_bind_4481432016(stream, i, context):
    out, i = expr1(stream, i, context)
    if out is not Miss:
        context[u'e'] = out
    return out, i


# (u'expr3a'()):r
def _r_bind_4481432976(stream, i, context):
    out, i = expr3a(stream, i, context)
    if out is not Miss:
        context[u'r'] = out
    return out, i


# (u'expr2'()):e
def _r_bind_4481433104(stream, i, context):
    out, i = expr2(stream, i, context)
    if out is not Miss:
        context[u'e'] = out
    return out, i


# (u'expr2'()):e
def _r_bind_4481433360(stream, i, context):
    out, i = expr2(stream, i, context)
    if out is not Miss:
        context[u'e'] = out
    return out, i


# ((u'ws'() Su'|' u'expr4'())*):e4s
def _r_bind_4481454224(stream, i, context):
    out, i = _r_star_4481456464(stream, i, context)
    if out is not Miss:
        context[u'e4s'] = out
    return out, i


# (u'expr3'()+):e3s
def _r_bind_4481454544(stream, i, context):
    out, i = _r_plus_4481456016(stream, i, context)
    if out is not Miss:
        context[u'e3s'] = out
    return out, i


# (u'repeattimes'()):ts
def _r_bind_4481455760(stream, i, context):
    out, i = repeattimes(stream, i, context)
    if out is not Miss:
        context[u'ts'] = out
    return out, i


# (u'name'()):n
def _r_bind_4481455952(stream, i, context):
    out, i = name(stream, i, context)
    if out is not Miss:
        context[u'n'] = out
    return out, i


# (u'name'()):n
def _r_bind_4481456528(stream, i, context):
    out, i = name(stream, i, context)
    if out is not Miss:
        context[u'n'] = out
    return out, i


# (u'expr4'()):e4
def _r_bind_4481456592(stream, i, context):
    out, i = expr4(stream, i, context)
    if out is not Miss:
        context[u'e4'] = out
    return out, i


# (((Su'|=' ->(True)) | (Su'=' ->(False)))):add
def _r_bind_4481456976(stream, i, context):
    out, i = _r_or_4481495504(stream, i, context)
    if out is not Miss:
        context[u'add'] = out
    return out, i


# (u'args'()):arglist
def _r_bind_4481457296(stream, i, context):
    out, i = args(stream, i, context)
    if out is not Miss:
        context[u'arglist'] = out
    return out, i


# (u'expr'()):e
def _r_bind_4481458064(stream, i, context):
    out, i = expr(stream, i, context)
    if out is not Miss:
        context[u'e'] = out
    return out, i


# (<(u'name'() (Su'.' u'name'())*)>):mod
def _r_bind_4481495120(stream, i, context):
    out, i = _r_take_4481496656(stream, i, context)
    if out is not Miss:
        context[u'mod'] = out
    return out, i


# (u'name'()):n
def _r_bind_4481495184(stream, i, context):
    out, i = name(stream, i, context)
    if out is not Miss:
        context[u'n'] = out
    return out, i


# (u'rule'()+):rs
def _r_bind_4481497040(stream, i, context):
    out, i = _r_plus_4481497616(stream, i, context)
    if out is not Miss:
        context[u'rs'] = out
    return out, i


# ->(x)
def _r_do_4481290320(stream, i, context):
    # x
    return eval(_r_do_4481290320_code, globals(), context), i


# ->(int(ds))
def _r_do_4481291728(stream, i, context):
    # int(ds)
    return eval(_r_do_4481291728_code, globals(), context), i


# ->(int(hs, 16))
def _r_do_4481293520(stream, i, context):
    # int(hs, 16)
    return eval(_r_do_4481293520_code, globals(), context), i


# ->(-x)
def _r_do_4481293904(stream, i, context):
    # -x
    return eval(_r_do_4481293904_code, globals(), context), i


# ->(String("".join(s)))
def _r_do_4481356112(stream, i, context):
    # String("".join(s))
    return eval(_r_do_4481356112_code, globals(), context), i


# ->("\n")
def _r_do_4481356880(stream, i, context):
    # "\n"
    return eval(_r_do_4481356880_code, globals(), context), i


# ->("\r")
def _r_do_4481357008(stream, i, context):
    # "\r"
    return eval(_r_do_4481357008_code, globals(), context), i


# ->("\t")
def _r_do_4481357392(stream, i, context):
    # "\t"
    return eval(_r_do_4481357392_code, globals(), context), i


# ->("\b")
def _r_do_4481357648(stream, i, context):
    # "\b"
    return eval(_r_do_4481357648_code, globals(), context), i


# ->("\f")
def _r_do_4481357904(stream, i, context):
    # "\f"
    return eval(_r_do_4481357904_code, globals(), context), i


# ->(compat.unichr(int(d, 16)))
def _r_do_4481358288(stream, i, context):
    # compat.unichr(int(d, 16))
    return eval(_r_do_4481358288_code, globals(), context), i


# ->(a)
def _r_do_4481358800(stream, i, context):
    # a
    return eval(_r_do_4481358800_code, globals(), context), i


# ->(s)
def _r_do_4481359568(stream, i, context):
    # s
    return eval(_r_do_4481359568_code, globals(), context), i


# ->(s)
def _r_do_4481384528(stream, i, context):
    # s
    return eval(_r_do_4481384528_code, globals(), context), i


# ->(In(set(xs)))
def _r_do_4481384592(stream, i, context):
    # In(set(xs))
    return eval(_r_do_4481384592_code, globals(), context), i


# ->(Call(rule, args))
def _r_do_4481386384(stream, i, context):
    # Call(rule, args)
    return eval(_r_do_4481386384_code, globals(), context), i


# ->(aa)
def _r_do_4481387280(stream, i, context):
    # aa
    return eval(_r_do_4481387280_code, globals(), context), i


# ->([])
def _r_do_4481387536(stream, i, context):
    # []
    return eval(_r_do_4481387536_code, globals(), context), i


# ->(Call2(mod, rule, args))
def _r_do_4481388304(stream, i, context):
    # Call2(mod, rule, args)
    return eval(_r_do_4481388304_code, globals(), context), i


# ->(Do("".join(code)))
def _r_do_4481409360(stream, i, context):
    # Do("".join(code))
    return eval(_r_do_4481409360_code, globals(), context), i


# ->(Do(code))
def _r_do_4481409744(stream, i, context):
    # Do(code)
    return eval(_r_do_4481409744_code, globals(), context), i


# ->(If(code))
def _r_do_4481410192(stream, i, context):
    # If(code)
    return eval(_r_do_4481410192_code, globals(), context), i


# ->(Mixed(until, aim))
def _r_do_4481410640(stream, i, context):
    # Mixed(until, aim)
    return eval(_r_do_4481410640_code, globals(), context), i


# ->(e)
def _r_do_4481411600(stream, i, context):
    # e
    return eval(_r_do_4481411600_code, globals(), context), i


# ->(None)
def _r_do_4481411728(stream, i, context):
    # None
    return eval(_r_do_4481411728_code, globals(), context), i


# ->(FailIf(f))
def _r_do_4481411856(stream, i, context):
    # FailIf(f)
    return eval(_r_do_4481411856_code, globals(), context), i


# ->(e)
def _r_do_4481412368(stream, i, context):
    # e
    return eval(_r_do_4481412368_code, globals(), context), i


# ->(Take(e))
def _r_do_4481412880(stream, i, context):
    # Take(e)
    return eval(_r_do_4481412880_code, globals(), context), i


# ->(Regex("".join(pattern)))
def _r_do_4481429776(stream, i, context):
    # Regex("".join(pattern))
    return eval(_r_do_4481429776_code, globals(), context), i


# ->((mn, mx))
def _r_do_4481431824(stream, i, context):
    # (mn, mx)
    return eval(_r_do_4481431824_code, globals(), context), i


# ->("/")
def _r_do_4481432080(stream, i, context):
    # "/"
    return eval(_r_do_4481432080_code, globals(), context), i


# ->(LookBehind(e))
def _r_do_4481433168(stream, i, context):
    # LookBehind(e)
    return eval(_r_do_4481433168_code, globals(), context), i


# ->(Peek(e))
def _r_do_4481433424(stream, i, context):
    # Peek(e)
    return eval(_r_do_4481433424_code, globals(), context), i


# ->(Not(e))
def _r_do_4481454160(stream, i, context):
    # Not(e)
    return eval(_r_do_4481454160_code, globals(), context), i


# ->(mn)
def _r_do_4481454416(stream, i, context):
    # mn
    return eval(_r_do_4481454416_code, globals(), context), i


# ->(None)
def _r_do_4481455376(stream, i, context):
    # None
    return eval(_r_do_4481455376_code, globals(), context), i


# ->(Star(e2))
def _r_do_4481455440(stream, i, context):
    # Star(e2)
    return eval(_r_do_4481455440_code, globals(), context), i


# ->(e3s[0] if len(e3s) == 1 else Seq(e3s))
def _r_do_4481455568(stream, i, context):
    # e3s[0] if len(e3s) == 1 else Seq(e3s)
    return eval(_r_do_4481455568_code, globals(), context), i


# ->(Plus(e2))
def _r_do_4481455632(stream, i, context):
    # Plus(e2)
    return eval(_r_do_4481455632_code, globals(), context), i


# ->(Opt(e2))
def _r_do_4481455888(stream, i, context):
    # Opt(e2)
    return eval(_r_do_4481455888_code, globals(), context), i


# ->(Repeat(e2, *ts))
def _r_do_4481456144(stream, i, context):
    # Repeat(e2, *ts)
    return eval(_r_do_4481456144_code, globals(), context), i


# ->(e2)
def _r_do_4481456208(stream, i, context):
    # e2
    return eval(_r_do_4481456208_code, globals(), context), i


# ->(Bind(n, r))
def _r_do_4481456848(stream, i, context):
    # Bind(n, r)
    return eval(_r_do_4481456848_code, globals(), context), i


# ->(r)
def _r_do_4481456912(stream, i, context):
    # r
    return eval(_r_do_4481456912_code, globals(), context), i


# ->(Or([e4] + e4s) if e4s else e4)
def _r_do_4481457104(stream, i, context):
    # Or([e4] + e4s) if e4s else e4
    return eval(_r_do_4481457104_code, globals(), context), i


# ->(r.make_rule(n, e, arglist, add))
def _r_do_4481495888(stream, i, context):
    # r.make_rule(n, e, arglist, add)
    return eval(_r_do_4481495888_code, globals(), context), i


# ->(True)
def _r_do_4481496144(stream, i, context):
    # True
    return eval(_r_do_4481496144_code, globals(), context), i


# ->(False)
def _r_do_4481496272(stream, i, context):
    # False
    return eval(_r_do_4481496272_code, globals(), context), i


# ->(add_import(mod, n))
def _r_do_4481496976(stream, i, context):
    # add_import(mod, n)
    return eval(_r_do_4481496976_code, globals(), context), i


# ->(make_grammar(rs))
def _r_do_4481497936(stream, i, context):
    # make_grammar(rs)
    return eval(_r_do_4481497936_code, globals(), context), i


# Ifrozenset([u'_'])
def _r_in_4481387024(stream, i, context):
    __xs = u'_'
    if i < len(stream) and stream[i] in __xs:
        return stream[i], i + 1
    else:
        return Miss, i


# (~S'\n')
def _r_not_4481043792(stream, i, context):
    return (Empty if _r_string_4475682512(stream, i, context)[0] is Miss else Miss), i


# (~Su'"')
def _r_not_4481385168(stream, i, context):
    return (Empty if _r_string_4481385424(stream, i, context)[0] is Miss else Miss), i


# (~Su"'")
def _r_not_4481386000(stream, i, context):
    return (Empty if _r_string_4481386256(stream, i, context)[0] is Miss else Miss), i


# (~Su']')
def _r_not_4481386448(stream, i, context):
    return (Empty if _r_string_4481386704(stream, i, context)[0] is Miss else Miss), i


# (~Su'/')
def _r_not_4481430736(stream, i, context):
    return (Empty if _r_string_4481430992(stream, i, context)[0] is Miss else Miss), i


# u'indent'()?
def _r_opt_4481385872(stream, i, context):
    out, newi = indent(stream, i, context)
    if out is Miss:
        return [], i
    else:
        return [out], newi


# u'indent'()?
def _r_opt_4481387408(stream, i, context):
    out, newi = indent(stream, i, context)
    if out is Miss:
        return [], i
    else:
        return [out], newi


# (u'hspace'() | u'vspace'() | u'comment'())
def _r_or_4475682576(stream, i, context):
    fm = _r_or_4475682576_fm
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


# ((Su'-' (u'barenum'()):x ->(-x)) | ((u'barenum'()):x ->(x)))
def _r_or_4481293712(stream, i, context):
    fm = _r_or_4481293712_fm
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


# (Su'x' | Su'X')
def _r_or_4481293968(stream, i, context):
    fm = _r_or_4481293968_fm
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


# ((Su'n' ->("\n")) | (Su'r' ->("\r")) | (Su't' ->("\t")) | (Su'b' ->("\b")) | (Su'f' ->("\f")) | (Su'x' (<(u'hexdigit'() u'hexdigit'())>):d ->(compat.unichr(int(d, 16)))) | ((u'r'.u'Any'()):a ->(a)))
def _r_or_4481356176(stream, i, context):
    fm = _r_or_4481356176_fm
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


# ((Su'"' ((u'escchar'() | ((~Su'"') u'r'.u'Any'()))+):s Su'"' ->(s)) | (Su"'" ((u'escchar'() | ((~Su"'") u'r'.u'Any'()))+):s Su"'" ->(s)))
def _r_or_4481358096(stream, i, context):
    fm = _r_or_4481358096_fm
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


# (u'escchar'() | ((~Su']') u'r'.u'Any'()))
def _r_or_4481358864(stream, i, context):
    fm = _r_or_4481358864_fm
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


# (u'escchar'() | ((~Su'"') u'r'.u'Any'()))
def _r_or_4481359504(stream, i, context):
    fm = _r_or_4481359504_fm
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


# (u'escchar'() | ((~Su"'") u'r'.u'Any'()))
def _r_or_4481384720(stream, i, context):
    fm = _r_or_4481384720_fm
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


# (Su'_' | u'ascii_letters'())
def _r_or_4481386896(stream, i, context):
    fm = _r_or_4481386896_fm
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


# (u'ascii_letters'() | u'digits'() | Ifrozenset([u'_']))
def _r_or_4481386960(stream, i, context):
    fm = _r_or_4481386960_fm
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


# ((u'ws'() Su',' (u'expr1'()):e ->(e)) | ->(None))
def _r_or_4481410704(stream, i, context):
    fm = _r_or_4481410704_fm
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


# ((Su'\\/' ->("/")) | u'r'.u'Any'())
def _r_or_4481430544(stream, i, context):
    fm = _r_or_4481430544_fm
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


# ((Su',' (u'barenum'() | ->(None))) | ->(mn))
def _r_or_4481432528(stream, i, context):
    fm = _r_or_4481432528_fm
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


# ((Su'~' (u'expr2'()):e ->(Peek(e))) | ((u'expr2'()):e ->(Not(e))))
def _r_or_4481432592(stream, i, context):
    fm = _r_or_4481432592_fm
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


# ((Su'*' ->(Star(e2))) | (Su'+' ->(Plus(e2))) | (Su'?' ->(Opt(e2))) | ((u'repeattimes'()):ts ->(Repeat(e2, *ts))) | ->(e2))
def _r_or_4481454288(stream, i, context):
    fm = _r_or_4481454288_fm
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


# (u'barenum'() | ->(None))
def _r_or_4481454608(stream, i, context):
    fm = _r_or_4481454608_fm
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


# ((Su':' (u'name'()):n ->(Bind(n, r))) | ->(r))
def _r_or_4481455248(stream, i, context):
    fm = _r_or_4481455248_fm
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


# ((Su'|=' ->(True)) | (Su'=' ->(False)))
def _r_or_4481495504(stream, i, context):
    fm = _r_or_4481495504_fm
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


# u'hspace'()+
def _r_plus_4481293200(stream, i, context):
    target = hspace
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


# u'hexdigit'()+
def _r_plus_4481355920(stream, i, context):
    target = hexdigit
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


# u'digit'()+
def _r_plus_4481356304(stream, i, context):
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


# (u'escchar'() | ((~Su'"') u'r'.u'Any'()))+
def _r_plus_4481359312(stream, i, context):
    target = _r_or_4481359504
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


# (u'escchar'() | ((~Su"'") u'r'.u'Any'()))+
def _r_plus_4481384656(stream, i, context):
    target = _r_or_4481384720
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


# u'expr3'()+
def _r_plus_4481456016(stream, i, context):
    target = expr3
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


# u'emptyline'()+
def _r_plus_4481495440(stream, i, context):
    target = emptyline
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


# u'rule'()+
def _r_plus_4481497616(stream, i, context):
    target = rule
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


# (Su'0' (Su'x' | Su'X') (<u'hexdigit'()+>):hs ->(int(hs, 16)))
def _r_seq_4475775184(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481293264, _r_or_4481293968, _r_bind_4481292304, _r_do_4481293520):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((<u'digit'()+>):ds ->(int(ds)))
def _r_seq_4475776976(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481293584, _r_do_4481291728):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((~S'\n') u'r'.u'Any'())
def _r_seq_4481043984(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_not_4481043792, r.Any):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((u'barenum'()):x ->(x))
def _r_seq_4481291600(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481292240, _r_do_4481290320):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'-' (u'barenum'()):x ->(-x))
def _r_seq_4481292368(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481293776, _r_bind_4481293648, _r_do_4481293904):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'n' ->("\n"))
def _r_seq_4481356240(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481356944, _r_do_4481356880):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'r' ->("\r"))
def _r_seq_4481356560(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481357136, _r_do_4481357008):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'b' ->("\b"))
def _r_seq_4481356624(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481357712, _r_do_4481357648):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su't' ->("\t"))
def _r_seq_4481356688(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481357520, _r_do_4481357392):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'x' (<(u'hexdigit'() u'hexdigit'())>):d ->(compat.unichr(int(d, 16))))
def _r_seq_4481357264(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481358224, _r_bind_4481357840, _r_do_4481358288):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'f' ->("\f"))
def _r_seq_4481357328(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481357968, _r_do_4481357904):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((u'r'.u'Any'()):a ->(a))
def _r_seq_4481357584(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481358160, _r_do_4481358800):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'"' ((u'escchar'() | ((~Su'"') u'r'.u'Any'()))+):s Su'"' ->(s))
def _r_seq_4481358032(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481359376, _r_bind_4481359184, _r_string_4481359632, _r_do_4481359568):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (u'hexdigit'() u'hexdigit'())
def _r_seq_4481358480(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (hexdigit, hexdigit):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su"'" ((u'escchar'() | ((~Su"'") u'r'.u'Any'()))+):s Su"'" ->(s))
def _r_seq_4481358736(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481359824, _r_bind_4481359440, _r_string_4481385360, _r_do_4481384528):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((~Su'"') u'r'.u'Any'())
def _r_seq_4481359760(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_not_4481385168, r.Any):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((~Su"'") u'r'.u'Any'())
def _r_seq_4481385040(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_not_4481386000, r.Any):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((~Su']') u'r'.u'Any'())
def _r_seq_4481385104(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_not_4481386448, r.Any):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((Su'_' | u'ascii_letters'()) (u'ascii_letters'() | u'digits'() | Ifrozenset([u'_']))*)
def _r_seq_4481385680(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_or_4481386896, _r_star_4481386768):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'(' (u'r'.u'appargs'()):aa Su')' ->(aa))
def _r_seq_4481386320(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481387152, _r_bind_4481386576, _r_string_4481387216, _r_do_4481387280):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (u'ws'() Su',' (u'expr1'()):e ->(e))
def _r_seq_4481410832(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481411472, _r_bind_4481411216, _r_do_4481411600):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((~Su'/') ((Su'\\/' ->("/")) | u'r'.u'Any'()))
def _r_seq_4481429904(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_not_4481430736, _r_or_4481430544):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'\\/' ->("/"))
def _r_seq_4481431568(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481432144, _r_do_4481432080):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (u'ws'() Su'~' ((Su'~' (u'expr2'()):e ->(Peek(e))) | ((u'expr2'()):e ->(Not(e)))))
def _r_seq_4481431632(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481432464, _r_or_4481432592):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (u'ws'() Su'^' (u'expr1'()):e ->(LookBehind(e)))
def _r_seq_4481431952(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481432912, _r_bind_4481432016, _r_do_4481433168):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su',' (u'barenum'() | ->(None)))
def _r_seq_4481432208(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481454480, _r_or_4481454608):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'~' (u'expr2'()):e ->(Peek(e)))
def _r_seq_4481432784(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481433296, _r_bind_4481433104, _r_do_4481433424):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((u'expr2'()):e ->(Not(e)))
def _r_seq_4481432848(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481433360, _r_do_4481454160):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'*' ->(Star(e2)))
def _r_seq_4481454672(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481455504, _r_do_4481455440):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'+' ->(Plus(e2)))
def _r_seq_4481454800(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481455696, _r_do_4481455632):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'?' ->(Opt(e2)))
def _r_seq_4481454928(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481455824, _r_do_4481455888):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su':' (u'name'()):n ->(Bind(n, r)))
def _r_seq_4481455056(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481456720, _r_bind_4481456528, _r_do_4481456848):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((u'repeattimes'()):ts ->(Repeat(e2, *ts)))
def _r_seq_4481455120(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481455760, _r_do_4481456144):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (u'ws'() Su'|' u'expr4'())
def _r_seq_4481457168(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481457808, expr4):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (u'hspace'()* u'emptyline'()+)
def _r_seq_4481457616(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_star_4481495248, _r_plus_4481495440):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'|=' ->(True))
def _r_seq_4481495632(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481496208, _r_do_4481496144):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'=' ->(False))
def _r_seq_4481495824(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481496400, _r_do_4481496272):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (u'name'() (Su'.' u'name'())*)
def _r_seq_4481496912(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (name, _r_star_4481497424):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'.' u'name'())
def _r_seq_4481497744(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481498320, name):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((~S'\n') u'r'.u'Any'())*
def _r_star_4481040464(stream, i, context):
    target = _r_seq_4481043984
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


# u'hspace'()*
def _r_star_4481042448(stream, i, context):
    target = hspace
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


# u'emptyline'()*
def _r_star_4481276496(stream, i, context):
    target = emptyline
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


# (u'escchar'() | ((~Su']') u'r'.u'Any'()))*
def _r_star_4481358608(stream, i, context):
    target = _r_or_4481358864
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


# (u'ascii_letters'() | u'digits'() | Ifrozenset([u'_']))*
def _r_star_4481386768(stream, i, context):
    target = _r_or_4481386960
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


# ((~Su'/') ((Su'\\/' ->("/")) | u'r'.u'Any'()))*
def _r_star_4481429584(stream, i, context):
    target = _r_seq_4481429904
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


# (u'ws'() Su'|' u'expr4'())*
def _r_star_4481456464(stream, i, context):
    target = _r_seq_4481457168
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


# u'hspace'()*
def _r_star_4481495248(stream, i, context):
    target = hspace
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


# u'imp'()*
def _r_star_4481497296(stream, i, context):
    target = imp
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


# (Su'.' u'name'())*
def _r_star_4481497424(stream, i, context):
    target = _r_seq_4481497744
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


# S'\n'
def _r_string_4475682512(stream, i, context):
    string = '\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'#'
def _r_string_4481040720(stream, i, context):
    string = u'#'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\t'
def _r_string_4481041104(stream, i, context):
    string = '\t'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\r'
def _r_string_4481042128(stream, i, context):
    string = '\r'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\n'
def _r_string_4481042768(stream, i, context):
    string = '\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\r\n'
def _r_string_4481043344(stream, i, context):
    string = '\r\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su' '
def _r_string_4481043472(stream, i, context):
    string = u' '
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'0'
def _r_string_4481293264(stream, i, context):
    string = u'0'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'-'
def _r_string_4481293776(stream, i, context):
    string = u'-'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'X'
def _r_string_4481294096(stream, i, context):
    string = u'X'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'x'
def _r_string_4481294224(stream, i, context):
    string = u'x'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\\'
def _r_string_4481294288(stream, i, context):
    string = '\\'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'n'
def _r_string_4481356944(stream, i, context):
    string = u'n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'r'
def _r_string_4481357136(stream, i, context):
    string = u'r'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su't'
def _r_string_4481357520(stream, i, context):
    string = u't'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'b'
def _r_string_4481357712(stream, i, context):
    string = u'b'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'f'
def _r_string_4481357968(stream, i, context):
    string = u'f'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'x'
def _r_string_4481358224(stream, i, context):
    string = u'x'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'['
def _r_string_4481358928(stream, i, context):
    string = u'['
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'"'
def _r_string_4481359376(stream, i, context):
    string = u'"'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'"'
def _r_string_4481359632(stream, i, context):
    string = u'"'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su']'
def _r_string_4481359696(stream, i, context):
    string = u']'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su"'"
def _r_string_4481359824(stream, i, context):
    string = u"'"
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su"'"
def _r_string_4481385360(stream, i, context):
    string = u"'"
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'"'
def _r_string_4481385424(stream, i, context):
    string = u'"'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su"'"
def _r_string_4481386256(stream, i, context):
    string = u"'"
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su']'
def _r_string_4481386704(stream, i, context):
    string = u']'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'('
def _r_string_4481387152(stream, i, context):
    string = u'('
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su')'
def _r_string_4481387216(stream, i, context):
    string = u')'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'_'
def _r_string_4481387600(stream, i, context):
    string = u'_'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'.'
def _r_string_4481387920(stream, i, context):
    string = u'.'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'->'
def _r_string_4481388496(stream, i, context):
    string = u'->'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'!('
def _r_string_4481409552(stream, i, context):
    string = u'!('
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su')'
def _r_string_4481409680(stream, i, context):
    string = u')'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'?('
def _r_string_4481410000(stream, i, context):
    string = u'?('
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su')'
def _r_string_4481410064(stream, i, context):
    string = u')'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'@('
def _r_string_4481410448(stream, i, context):
    string = u'@('
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su')'
def _r_string_4481410768(stream, i, context):
    string = u')'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su','
def _r_string_4481411472(stream, i, context):
    string = u','
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'.('
def _r_string_4481411664(stream, i, context):
    string = u'.('
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su')'
def _r_string_4481411920(stream, i, context):
    string = u')'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'('
def _r_string_4481412176(stream, i, context):
    string = u'('
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su')'
def _r_string_4481412432(stream, i, context):
    string = u')'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'<'
def _r_string_4481412688(stream, i, context):
    string = u'<'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'>'
def _r_string_4481412944(stream, i, context):
    string = u'>'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'/'
def _r_string_4481429648(stream, i, context):
    string = u'/'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'/'
def _r_string_4481429840(stream, i, context):
    string = u'/'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'/'
def _r_string_4481430992(stream, i, context):
    string = u'/'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'{'
def _r_string_4481431376(stream, i, context):
    string = u'{'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'\\/'
def _r_string_4481432144(stream, i, context):
    string = u'\\/'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'}'
def _r_string_4481432272(stream, i, context):
    string = u'}'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'~'
def _r_string_4481432464(stream, i, context):
    string = u'~'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'^'
def _r_string_4481432912(stream, i, context):
    string = u'^'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'~'
def _r_string_4481433296(stream, i, context):
    string = u'~'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su','
def _r_string_4481454480(stream, i, context):
    string = u','
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'*'
def _r_string_4481455504(stream, i, context):
    string = u'*'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'+'
def _r_string_4481455696(stream, i, context):
    string = u'+'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'?'
def _r_string_4481455824(stream, i, context):
    string = u'?'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su':'
def _r_string_4481456720(stream, i, context):
    string = u':'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'|'
def _r_string_4481457808(stream, i, context):
    string = u'|'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'|='
def _r_string_4481496208(stream, i, context):
    string = u'|='
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'='
def _r_string_4481496400(stream, i, context):
    string = u'='
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su' as '
def _r_string_4481496720(stream, i, context):
    string = u' as '
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'import '
def _r_string_4481496784(stream, i, context):
    string = u'import '
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\n'
def _r_string_4481497104(stream, i, context):
    string = '\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'.'
def _r_string_4481498320(stream, i, context):
    string = u'.'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# <u'digit'()+>
def _r_take_4481292048(stream, i, context):
    _i = i
    out, i = _r_plus_4481356304(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# <u'hexdigit'()+>
def _r_take_4481293328(stream, i, context):
    _i = i
    out, i = _r_plus_4481355920(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# <(u'hexdigit'() u'hexdigit'())>
def _r_take_4481358352(stream, i, context):
    _i = i
    out, i = _r_seq_4481358480(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# <(u'name'() (Su'.' u'name'())*)>
def _r_take_4481496656(stream, i, context):
    _i = i
    out, i = _r_seq_4481496912(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# $action
def action(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481409552, _r_bind_4481409232, _r_string_4481409680, _r_do_4481409744):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $application
def application(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_opt_4481385872, _r_bind_4481356048, _r_bind_4481385296, _r_do_4481386384):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $application2
def application2(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_opt_4481387408, _r_bind_4481386640, _r_string_4481387920, _r_bind_4481386192, _r_bind_4481387792, _r_do_4481388304):
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


# $ascii_letters
def ascii_letters(stream, i, context):
    __xs = u'ACBEDGFIHKJMLONQPSRUTWVYXZacbedgfihkjmlonqpsrutwvyxz'
    if i < len(stream) and stream[i] in __xs:
        return stream[i], i + 1
    else:
        return Miss, i


# $barenum
def barenum(stream, i, context):
    fm = barenum_fm
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


# $brackets
def brackets(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481412176, _r_bind_4481411536, ws, _r_string_4481412432, _r_do_4481412368):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $category
def category(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481358928, _r_bind_4481357776, _r_string_4481359696, _r_do_4481384592):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $comment
def comment(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481040720, _r_star_4481040464):
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


# $digits
def digits(stream, i, context):
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


# $emptyline
def emptyline(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_star_4481042448, vspace):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $escchar
def escchar(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481294288, _r_or_4481356176):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $expr
def expr(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481456592, _r_bind_4481454224, _r_do_4481457104):
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


# $expr3
def expr3(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481432976, _r_or_4481455248):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $expr3a
def expr3a(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481431760, _r_or_4481454288):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $expr4
def expr4(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481454544, _r_do_4481455568):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $failif
def failif(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481411664, _r_bind_4481410576, _r_string_4481411920, _r_do_4481411856):
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
    for rule in (_r_star_4481497296, _r_bind_4481497040, ws, r.streamend, _r_do_4481497936):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $hexdigit
def hexdigit(stream, i, context):
    __xs = u'ACBEDFacbedf1032547698'
    if i < len(stream) and stream[i] in __xs:
        return stream[i], i + 1
    else:
        return Miss, i


# $hspace
def hspace(stream, i, context):
    fm = hspace_fm
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


# $imp
def imp(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, r.linestart, _r_string_4481496784, _r_bind_4481495120, _r_string_4481496720, _r_bind_4481495184, _r_string_4481497104, _r_do_4481496976):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $indent
def indent(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_star_4481276496, _r_plus_4481293200):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $mixed
def mixed(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481410448, _r_bind_4481409872, _r_bind_4481410128, _r_string_4481410768, _r_do_4481410640):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $name
def name(stream, i, context):
    _i = i
    out, i = _r_seq_4481385680(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# $number
def number(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_or_4481293712):
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
    for rule in (ws, _r_string_4481410000, _r_bind_4481409616, _r_string_4481410064, _r_do_4481410192):
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
    for rule in (ws, _r_string_4481429648, _r_bind_4481412816, _r_string_4481429840, _r_do_4481429776):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $repeattimes
def repeattimes(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481431376, _r_bind_4481429712, _r_bind_4481430032, _r_string_4481432272, _r_do_4481431824):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $rule
def rule(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, r.linestart, _r_bind_4481455952, _r_bind_4481457296, ws, _r_bind_4481456976, _r_bind_4481458064, ruleend, _r_do_4481495888):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $ruleend
def ruleend(stream, i, context):
    fm = ruleend_fm
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


# $rulevalue
def rulevalue(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481388496, ws, _r_bind_4481388240, _r_do_4481409360):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $string
def string(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_bind_4481291344, _r_do_4481356112):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $take
def take(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_string_4481412688, _r_bind_4481411984, ws, _r_string_4481412944, _r_do_4481412880):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $vspace
def vspace(stream, i, context):
    fm = vspace_fm
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


# $ws
def ws(stream, i, context):
    target = _r_or_4475682576
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


# 392 functions


_r_do_4481290320_code = r.compile_expr(u'x')
_r_do_4481291728_code = r.compile_expr(u'int(ds)')
_r_do_4481293520_code = r.compile_expr(u'int(hs, 16)')
_r_do_4481293904_code = r.compile_expr(u'-x')
_r_do_4481356112_code = r.compile_expr(u'String("".join(s))')
_r_do_4481356880_code = r.compile_expr(u'"\\n"')
_r_do_4481357008_code = r.compile_expr(u'"\\r"')
_r_do_4481357392_code = r.compile_expr(u'"\\t"')
_r_do_4481357648_code = r.compile_expr(u'"\\b"')
_r_do_4481357904_code = r.compile_expr(u'"\\f"')
_r_do_4481358288_code = r.compile_expr(u'compat.unichr(int(d, 16))')
_r_do_4481358800_code = r.compile_expr(u'a')
_r_do_4481359568_code = r.compile_expr(u's')
_r_do_4481384528_code = r.compile_expr(u's')
_r_do_4481384592_code = r.compile_expr(u'In(set(xs))')
_r_do_4481386384_code = r.compile_expr(u'Call(rule, args)')
_r_do_4481387280_code = r.compile_expr(u'aa')
_r_do_4481387536_code = r.compile_expr(u'[]')
_r_do_4481388304_code = r.compile_expr(u'Call2(mod, rule, args)')
_r_do_4481409360_code = r.compile_expr(u'Do("".join(code))')
_r_do_4481409744_code = r.compile_expr(u'Do(code)')
_r_do_4481410192_code = r.compile_expr(u'If(code)')
_r_do_4481410640_code = r.compile_expr(u'Mixed(until, aim)')
_r_do_4481411600_code = r.compile_expr(u'e')
_r_do_4481411728_code = r.compile_expr(u'None')
_r_do_4481411856_code = r.compile_expr(u'FailIf(f)')
_r_do_4481412368_code = r.compile_expr(u'e')
_r_do_4481412880_code = r.compile_expr(u'Take(e)')
_r_do_4481429776_code = r.compile_expr(u'Regex("".join(pattern))')
_r_do_4481431824_code = r.compile_expr(u'(mn, mx)')
_r_do_4481432080_code = r.compile_expr(u'"/"')
_r_do_4481433168_code = r.compile_expr(u'LookBehind(e)')
_r_do_4481433424_code = r.compile_expr(u'Peek(e)')
_r_do_4481454160_code = r.compile_expr(u'Not(e)')
_r_do_4481454416_code = r.compile_expr(u'mn')
_r_do_4481455376_code = r.compile_expr(u'None')
_r_do_4481455440_code = r.compile_expr(u'Star(e2)')
_r_do_4481455568_code = r.compile_expr(u'e3s[0] if len(e3s) == 1 else Seq(e3s)')
_r_do_4481455632_code = r.compile_expr(u'Plus(e2)')
_r_do_4481455888_code = r.compile_expr(u'Opt(e2)')
_r_do_4481456144_code = r.compile_expr(u'Repeat(e2, *ts)')
_r_do_4481456208_code = r.compile_expr(u'e2')
_r_do_4481456848_code = r.compile_expr(u'Bind(n, r)')
_r_do_4481456912_code = r.compile_expr(u'r')
_r_do_4481457104_code = r.compile_expr(u'Or([e4] + e4s) if e4s else e4')
_r_do_4481495888_code = r.compile_expr(u'r.make_rule(n, e, arglist, add)')
_r_do_4481496144_code = r.compile_expr(u'True')
_r_do_4481496272_code = r.compile_expr(u'False')
_r_do_4481496976_code = r.compile_expr(u'add_import(mod, n)')
_r_do_4481497936_code = r.compile_expr(u'make_grammar(rs)')
_r_or_4475682576_fm = {
    None: [(hspace, True), (vspace, True), (comment, True)],
}
_r_or_4481293712_fm = {
    None: [(_r_seq_4481291600, True)],
    u'-': [(_r_seq_4481292368, True), (_r_seq_4481291600, True)],
}
_r_or_4481293968_fm = {
    None: [],
    u'X': [(_r_string_4481294096, False)],
    u'x': [(_r_string_4481294224, False)],
}
_r_or_4481356176_fm = {
    None: [(_r_seq_4481357584, True)],
    u'b': [(_r_seq_4481356624, False), (_r_seq_4481357584, True)],
    u'f': [(_r_seq_4481357328, False), (_r_seq_4481357584, True)],
    u'n': [(_r_seq_4481356240, False), (_r_seq_4481357584, True)],
    u'r': [(_r_seq_4481356560, False), (_r_seq_4481357584, True)],
    u't': [(_r_seq_4481356688, False), (_r_seq_4481357584, True)],
    u'x': [(_r_seq_4481357264, True), (_r_seq_4481357584, True)],
}
_r_or_4481358096_fm = {
    None: [],
    u'"': [(_r_seq_4481358032, True)],
    u"'": [(_r_seq_4481358736, True)],
}
_r_or_4481358864_fm = {
    None: [(escchar, True), (_r_seq_4481385104, True)],
}
_r_or_4481359504_fm = {
    None: [(escchar, True), (_r_seq_4481359760, True)],
}
_r_or_4481384720_fm = {
    None: [(escchar, True), (_r_seq_4481385040, True)],
}
_r_or_4481386896_fm = {
    None: [(ascii_letters, True)],
    u'_': [(_r_string_4481387600, False), (ascii_letters, True)],
}
_r_or_4481386960_fm = {
    None: [(ascii_letters, True), (digits, True)],
    u'_': [(_r_in_4481387024, False), (ascii_letters, True), (digits, True)],
}
_r_or_4481410704_fm = {
    None: [(_r_seq_4481410832, True), (_r_do_4481411728, False)],
}
_r_or_4481430544_fm = {
    None: [(r.Any, True)],
    u'\\': [(_r_seq_4481431568, False), (r.Any, True)],
}
_r_or_4481432528_fm = {
    None: [(_r_do_4481454416, False)],
    u',': [(_r_seq_4481432208, True), (_r_do_4481454416, False)],
}
_r_or_4481432592_fm = {
    None: [(_r_seq_4481432848, True)],
    u'~': [(_r_seq_4481432784, True), (_r_seq_4481432848, True)],
}
_r_or_4481454288_fm = {
    None: [(_r_seq_4481455120, True), (_r_do_4481456208, False)],
    u'*': [(_r_seq_4481454672, False), (_r_seq_4481455120, True), (_r_do_4481456208, False)],
    u'+': [(_r_seq_4481454800, False), (_r_seq_4481455120, True), (_r_do_4481456208, False)],
    u'?': [(_r_seq_4481454928, False), (_r_seq_4481455120, True), (_r_do_4481456208, False)],
}
_r_or_4481454608_fm = {
    None: [(barenum, True), (_r_do_4481455376, False)],
}
_r_or_4481455248_fm = {
    None: [(_r_do_4481456912, False)],
    u':': [(_r_seq_4481455056, True), (_r_do_4481456912, False)],
}
_r_or_4481495504_fm = {
    None: [],
    u'=': [(_r_seq_4481495824, False)],
    u'|': [(_r_seq_4481495632, False)],
}
args_fm = {
    None: [(_r_do_4481387536, False)],
    u'(': [(_r_seq_4481386320, True), (_r_do_4481387536, False)],
}
barenum_fm = {
    None: [(_r_seq_4475776976, True)],
    u'0': [(_r_seq_4475775184, True), (_r_seq_4475776976, True)],
}
expr1_fm = {
    None: [(application2, True), (application, True), (rulevalue, True), (predicate, True), (action, True), (mixed, True), (failif, True), (number, True), (string, True), (category, True), (brackets, True), (take, True), (regex, True)],
}
expr2_fm = {
    None: [(_r_seq_4481431632, True), (_r_seq_4481431952, True), (expr1, True)],
}
hspace_fm = {
    None: [(comment, True)],
    '\t': [(_r_string_4481041104, False), (comment, True)],
    u' ': [(_r_string_4481043472, False), (comment, True)],
}
ruleend_fm = {
    None: [(_r_seq_4481457616, True), (r.streamend, True)],
}
vspace_fm = {
    None: [],
    '\n': [(_r_string_4481042768, False)],
    '\r': [(_r_string_4481043344, False), (_r_string_4481042128, False)],
}


_r_call2_4481044176 = r.Any
_r_call2_4481358672 = r.Any
_r_call2_4481384912 = r.Any
_r_call2_4481385552 = r.Any
_r_call2_4481386128 = r.Any
_r_call2_4481387088 = r.appargs
_r_call2_4481409168 = r.valexpr
_r_call2_4481409424 = r.actionexpr
_r_call2_4481409936 = r.actionexpr
_r_call2_4481431312 = r.Any
_r_call2_4481457424 = r.streamend
_r_call2_4481457488 = r.linestart
_r_call2_4481496464 = r.linestart
_r_call2_4481497808 = r.streamend
