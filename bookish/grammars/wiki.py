#encoding: utf8

import re
from bookish import compat
from bookish.parser.builder import _fill_args
from bookish.parser.parser import make_grammar
from bookish.parser.parser import Empty, Failure, Miss
from bookish.parser.parser import ParserError
from bookish.parser import rules as r

import bookish.parser.rules as r
import bookish.util as util
import bookish.wikipages as w


# Any
def Any(stream, i, context):
    if i >= len(stream) or stream.startswith(u"\uffff", i):
        return Miss, i
    else:
        return stream[i], i + 1


# (@($para_ending, $spans)):tx
def _r_bind_4479709456(stream, i, context):
    out, i = _r_mixed_4479710544(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# ($para_ending):nd
def _r_bind_4479709584(stream, i, context):
    out, i = para_ending(stream, i, context)
    if out is not Miss:
        context[u'nd'] = out
    return out, i


# (Ifrozenset([u'*', u'-'])+):bs
def _r_bind_4479709968(stream, i, context):
    out, i = _r_plus_4479709776(stream, i, context)
    if out is not Miss:
        context[u'bs'] = out
    return out, i


# (Su' '+):space
def _r_bind_4479710480(stream, i, context):
    out, i = _r_plus_4479710864(stream, i, context)
    if out is not Miss:
        context[u'space'] = out
    return out, i


# (Su' '+):space
def _r_bind_4479710736(stream, i, context):
    out, i = _r_plus_4479711568(stream, i, context)
    if out is not Miss:
        context[u'space'] = out
    return out, i


# (Su'#'+):ns
def _r_bind_4479710992(stream, i, context):
    out, i = _r_plus_4479710928(stream, i, context)
    if out is not Miss:
        context[u'ns'] = out
    return out, i


# ($lstart):indent
def _r_bind_4479712208(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'indent'] = out
    return out, i


# (@($bullet_ending, $spans)):tx
def _r_bind_4479712336(stream, i, context):
    out, i = _r_mixed_4479712912(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# ($bullet_start):bwidth
def _r_bind_4479712720(stream, i, context):
    out, i = bullet_start(stream, i, context)
    if out is not Miss:
        context[u'bwidth'] = out
    return out, i


# ($bullet_body):tx
def _r_bind_4479712976(stream, i, context):
    out, i = bullet_body(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# ($lstart):indent
def _r_bind_4479713104(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'indent'] = out
    return out, i


# ($ord_start):bwidth
def _r_bind_4479734160(stream, i, context):
    out, i = ord_start(stream, i, context)
    if out is not Miss:
        context[u'bwidth'] = out
    return out, i


# ($lstart):nextin
def _r_bind_4479734224(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'nextin'] = out
    return out, i


# ($bullet_body):tx
def _r_bind_4479734480(stream, i, context):
    out, i = bullet_body(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# ($lstart):indent
def _r_bind_4479734736(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'indent'] = out
    return out, i


# ($lstart):indent
def _r_bind_4479735824(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'indent'] = out
    return out, i


# ((($ws Su'#!' $identifier) | ->(None))):lang
def _r_bind_4479735952(stream, i, context):
    out, i = _r_or_4479737168(stream, i, context)
    if out is not Miss:
        context[u'lang'] = out
    return out, i


# (@($sepend, $stylespans)):tx
def _r_bind_4479736144(stream, i, context):
    out, i = _r_mixed_4479736400(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# (Su'~'{2, None}):line
def _r_bind_4479736272(stream, i, context):
    out, i = _r_repeat_4479735376(stream, i, context)
    if out is not Miss:
        context[u'line'] = out
    return out, i


# ($lstart):indent
def _r_bind_4479736336(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'indent'] = out
    return out, i


# (@(Su'}}}', None)):tx
def _r_bind_4479736592(stream, i, context):
    out, i = _r_mixed_4479737424(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# (@(($hspace* Su'='), $stylespans)):tx
def _r_bind_4479736912(stream, i, context):
    out, i = _r_mixed_4479783760(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# (@(($hspace* Su'|>'), $stylespans)):tx
def _r_bind_4479736976(stream, i, context):
    out, i = _r_mixed_4479737232(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# (@((($hspace* Su'=') | Su'<|'), $stylespans)):tx
def _r_bind_4479783632(stream, i, context):
    out, i = _r_mixed_4479784976(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# ($subtitle?):subt
def _r_bind_4479784016(stream, i, context):
    out, i = _r_opt_4479785104(stream, i, context)
    if out is not Miss:
        context[u'subt'] = out
    return out, i


# ($supertitle?):supt
def _r_bind_4479784208(stream, i, context):
    out, i = _r_opt_4479784528(stream, i, context)
    if out is not Miss:
        context[u'supt'] = out
    return out, i


# ($lstart):indent
def _r_bind_4479784272(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'indent'] = out
    return out, i


# ($lstart):indent
def _r_bind_4479785744(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'indent'] = out
    return out, i


# (Su'='{2, None}):eqs
def _r_bind_4479786384(stream, i, context):
    out, i = _r_repeat_4479811920(stream, i, context)
    if out is not Miss:
        context[u'eqs'] = out
    return out, i


# (<((~Su')') Any)+>):tag
def _r_bind_4479786576(stream, i, context):
    out, i = _r_take_4479786832(stream, i, context)
    if out is not Miss:
        context[u'tag'] = out
    return out, i


# (@(($hspace* Su'='), $stylespans)):tx
def _r_bind_4479811728(stream, i, context):
    out, i = _r_mixed_4479812624(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# (Su'='{2, None}):eqs2
def _r_bind_4479812688(stream, i, context):
    out, i = _r_repeat_4479812496(stream, i, context)
    if out is not Miss:
        context[u'eqs2'] = out
    return out, i


# (@($lineend, $stylespans)):tx
def _r_bind_4479812752(stream, i, context):
    out, i = _r_mixed_4479814736(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# ($heading_tag?):tag
def _r_bind_4479812816(stream, i, context):
    out, i = _r_opt_4479812368(stream, i, context)
    if out is not Miss:
        context[u'tag'] = out
    return out, i


# ($identifier):n
def _r_bind_4479814416(stream, i, context):
    out, i = identifier(stream, i, context)
    if out is not Miss:
        context[u'n'] = out
    return out, i


# (@(($break_ | Su'"""'), $spans)):tx
def _r_bind_4479814608(stream, i, context):
    out, i = _r_mixed_4479815568(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# ($lstart):indent
def _r_bind_4479814672(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'indent'] = out
    return out, i


# ($identifier?):n
def _r_bind_4479815120(stream, i, context):
    out, i = _r_opt_4479814864(stream, i, context)
    if out is not Miss:
        context[u'n'] = out
    return out, i


# ((Su'TIP' | Su'NOTE' | Su'WARNING')):it
def _r_bind_4479832720(stream, i, context):
    out, i = _r_or_4479834960(stream, i, context)
    if out is not Miss:
        context[u'it'] = out
    return out, i


# (<@(Ifrozenset([u':', u' ', '\n']), None)>):k
def _r_bind_4479833296(stream, i, context):
    out, i = _r_take_4479835536(stream, i, context)
    if out is not Miss:
        context[u'k'] = out
    return out, i


# ($lstart):indent
def _r_bind_4479833488(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'indent'] = out
    return out, i


# ($itemtype):it
def _r_bind_4479833936(stream, i, context):
    out, i = itemtype(stream, i, context)
    if out is not Miss:
        context[u'it'] = out
    return out, i


# (@($itemend, $spans)):tx
def _r_bind_4479834064(stream, i, context):
    out, i = _r_mixed_4479834256(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# ($lstart):indent
def _r_bind_4479834576(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'indent'] = out
    return out, i


# ($lstart):indent
def _r_bind_4479834640(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'indent'] = out
    return out, i


# (@(S'\n', $stylespans)):tx
def _r_bind_4479834896(stream, i, context):
    out, i = _r_mixed_4479835088(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# (<@($lineend, None)>):v
def _r_bind_4479836048(stream, i, context):
    out, i = _r_take_4479834704(stream, i, context)
    if out is not Miss:
        context[u'v'] = out
    return out, i


# (((~~(($lstart):nextin ?(nextin > indent))) (R(.*$)):line ?(line.strip()) $lineend ->(line))*):extras
def _r_bind_4479836112(stream, i, context):
    out, i = _r_star_4479834832(stream, i, context)
    if out is not Miss:
        context[u'extras'] = out
    return out, i


# (@($lineend, $spans)):tx
def _r_bind_4479856848(stream, i, context):
    out, i = _r_mixed_4479858768(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# ($lstart):indent
def _r_bind_4479857040(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'indent'] = out
    return out, i


# (R(.*$)):line
def _r_bind_4479857552(stream, i, context):
    out, i = _r_regex_4479857936(stream, i, context)
    if out is not Miss:
        context[u'line'] = out
    return out, i


# ($xname):n
def _r_bind_4479857680(stream, i, context):
    out, i = xname(stream, i, context)
    if out is not Miss:
        context[u'n'] = out
    return out, i


# ($attrlist):alist
def _r_bind_4479858320(stream, i, context):
    out, i = attrlist(stream, i, context)
    if out is not Miss:
        context[u'alist'] = out
    return out, i


# ($lstart):nextin
def _r_bind_4479859344(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'nextin'] = out
    return out, i


# ($blocks*):b
def _r_bind_4479860560(stream, i, context):
    out, i = _r_star_4479894160(stream, i, context)
    if out is not Miss:
        context[u'b'] = out
    return out, i


# ($xname):n
def _r_bind_4481034192(stream, i, context):
    out, i = xname(stream, i, context)
    if out is not Miss:
        context[u'n'] = out
    return out, i


# ($attrlist):alist
def _r_bind_4481034512(stream, i, context):
    out, i = attrlist(stream, i, context)
    if out is not Miss:
        context[u'alist'] = out
    return out, i


# (@(Su'</', $spans)):tx
def _r_bind_4481035984(stream, i, context):
    out, i = _r_mixed_4481458064(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# ($xname):n
def _r_bind_4481043600(stream, i, context):
    out, i = xname(stream, i, context)
    if out is not Miss:
        context[u'n'] = out
    return out, i


# ($attrlist):alist
def _r_bind_4481043728(stream, i, context):
    out, i = attrlist(stream, i, context)
    if out is not Miss:
        context[u'alist'] = out
    return out, i


# ($lstart):indent
def _r_bind_4481334288(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'indent'] = out
    return out, i


# ($attr*):attrs
def _r_bind_4481356560(stream, i, context):
    out, i = _r_star_4481358864(stream, i, context)
    if out is not Miss:
        context[u'attrs'] = out
    return out, i


# ($xname):name
def _r_bind_4481358032(stream, i, context):
    out, i = xname(stream, i, context)
    if out is not Miss:
        context[u'name'] = out
    return out, i


# ($xname):k
def _r_bind_4481359120(stream, i, context):
    out, i = xname(stream, i, context)
    if out is not Miss:
        context[u'k'] = out
    return out, i


# (<((~Su'"') Any)*>):v
def _r_bind_4481359184(stream, i, context):
    out, i = _r_take_4481357712(stream, i, context)
    if out is not Miss:
        context[u'v'] = out
    return out, i


# (<@((Su')' | (fail $break_)), None)>):v
def _r_bind_4481359824(stream, i, context):
    out, i = _r_take_4481355856(stream, i, context)
    if out is not Miss:
        context[u'v'] = out
    return out, i


# (@((Su'>>' | (fail $break_)), $inline)):tx
def _r_bind_4481384720(stream, i, context):
    out, i = _r_mixed_4481411472(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# (@((Su'__' | (fail $break_)), ($uisep | $inline))):tx
def _r_bind_4481387792(stream, i, context):
    out, i = _r_mixed_4481411792(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# (@((Su'_' | (fail $break_)), $inline)):tx
def _r_bind_4481409808(stream, i, context):
    out, i = _r_mixed_4481412944(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# (@((Su'`' | (fail $break_)), $var)):tx
def _r_bind_4481409872(stream, i, context):
    out, i = _r_mixed_4481359760(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# ($identifier):n
def _r_bind_4481410704(stream, i, context):
    out, i = identifier(stream, i, context)
    if out is not Miss:
        context[u'n'] = out
    return out, i


# (@((Su'*' | (fail $break_)), $inline)):tx
def _r_bind_4481410768(stream, i, context):
    out, i = _r_mixed_4481411344(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# ((Su'---' | Su'--')):d
def _r_bind_4481429712(stream, i, context):
    out, i = _r_or_4481429776(stream, i, context)
    if out is not Miss:
        context[u'd'] = out
    return out, i


# (($num_entity | $named_entity)):char
def _r_bind_4481431248(stream, i, context):
    out, i = _r_or_4481432848(stream, i, context)
    if out is not Miss:
        context[u'char'] = out
    return out, i


# (R([A-Za-z]+)):n
def _r_bind_4481431312(stream, i, context):
    out, i = _r_regex_4481431184(stream, i, context)
    if out is not Miss:
        context[u'n'] = out
    return out, i


# (((Su'(c)' ->(compat.unichr(169))) | (Su'(tm)' ->(compat.unichr(8482))) | (Su'(r)' ->(compat.unichr(174))))):c
def _r_bind_4481431504(stream, i, context):
    out, i = _r_or_4481292240(stream, i, context)
    if out is not Miss:
        context[u'c'] = out
    return out, i


# (((Su'<-' ->(compat.unichr(8592))) | (Su'->' ->(compat.unichr(8594))) | (Su'<=' ->(compat.unichr(8804))) | (Su'=>' ->(compat.unichr(8805))) | (Su'<=>' ->(compat.unichr(8660))))):c
def _r_bind_4481432272(stream, i, context):
    out, i = _r_or_4481429584(stream, i, context)
    if out is not Miss:
        context[u'c'] = out
    return out, i


# (@(Su'|', $stylespans)):tx
def _r_bind_4481456016(stream, i, context):
    out, i = _r_mixed_4481456144(stream, i, context)
    if out is not Miss:
        context[u'tx'] = out
    return out, i


# (($hspace* Su'+' $hspace* $keyname)*):kk
def _r_bind_4481456656(stream, i, context):
    out, i = _r_star_4481454160(stream, i, context)
    if out is not Miss:
        context[u'kk'] = out
    return out, i


# ((($hspace+ $keyname) | ((~Su'(') $keyname))):k
def _r_bind_4481457488(stream, i, context):
    out, i = _r_or_4481454800(stream, i, context)
    if out is not Miss:
        context[u'k'] = out
    return out, i


# ($hspace*):indent
def _r_bind_4481495440(stream, i, context):
    out, i = _r_star_4481497680(stream, i, context)
    if out is not Miss:
        context[u'indent'] = out
    return out, i


# ($lstart):nextin
def _r_bind_4481495824(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'nextin'] = out
    return out, i


# ($charnum):num
def _r_bind_4481496720(stream, i, context):
    out, i = charnum(stream, i, context)
    if out is not Miss:
        context[u'num'] = out
    return out, i


# (Any):c
def _r_bind_4481496784(stream, i, context):
    out, i = Any(stream, i, context)
    if out is not Miss:
        context[u'c'] = out
    return out, i


# (<$digit+>):d
def _r_bind_4481496976(stream, i, context):
    out, i = _r_take_4481431120(stream, i, context)
    if out is not Miss:
        context[u'd'] = out
    return out, i


# (<Ifrozenset([u'A', u'C', u'B', u'E', u'D', u'F', u'a', u'c', u'b', u'e', u'd', u'f', u'1', u'0', u'3', u'2', u'5', u'4', u'7', u'6', u'9', u'8'])+>):h
def _r_bind_4481497232(stream, i, context):
    out, i = _r_take_4481497040(stream, i, context)
    if out is not Miss:
        context[u'h'] = out
    return out, i


# ($lstart):nextin
def _r_bind_4481498320(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'nextin'] = out
    return out, i


# ($lstart):nextin
def _r_bind_4481498832(stream, i, context):
    out, i = lstart(stream, i, context)
    if out is not Miss:
        context[u'nextin'] = out
    return out, i


# BlockBreak
def _r_blockbreak_4470302032(stream, i, context):
    return r.BlockBreak._accept(stream, i, context)


# u'ctag'(n)
def _r_call_4481456528(stream, i, context):
    target = ctag
    parmnames = (u'n',)
    values = [eval(a, globals(), context) for a in [u'n']]
    c = _fill_args(context, parmnames, values)
    return target(stream, i, c)


# ->(("cell", "td"))
def _r_do_4479709264(stream, i, context):
    # ("cell", "td")
    return eval(_r_do_4479709264_code, globals(), context), i


# ->(("cell", "th"))
def _r_do_4479709392(stream, i, context):
    # ("cell", "th")
    return eval(_r_do_4479709392_code, globals(), context), i


# ->(("para", None))
def _r_do_4479710096(stream, i, context):
    # ("para", None)
    return eval(_r_do_4479710096_code, globals(), context), i


# ->(w.block(nd[0], indent, tx, role=nd[1]))
def _r_do_4479710416(stream, i, context):
    # w.block(nd[0], indent, tx, role=nd[1])
    return eval(_r_do_4479710416_code, globals(), context), i


# ->(len(bs) + len(space))
def _r_do_4479711056(stream, i, context):
    # len(bs) + len(space)
    return eval(_r_do_4479711056_code, globals(), context), i


# ->(len(ns) + len(space))
def _r_do_4479711696(stream, i, context):
    # len(ns) + len(space)
    return eval(_r_do_4479711696_code, globals(), context), i


# ->(tx)
def _r_do_4479711952(stream, i, context):
    # tx
    return eval(_r_do_4479711952_code, globals(), context), i


# ->(w.block('bullet', indent, tx, blevel=indent+bwidth))
def _r_do_4479733840(stream, i, context):
    # w.block('bullet', indent, tx, blevel=indent+bwidth)
    return eval(_r_do_4479733840_code, globals(), context), i


# ->(w.block('ord', indent, tx, blevel=indent+bwidth))
def _r_do_4479735312(stream, i, context):
    # w.block('ord', indent, tx, blevel=indent+bwidth)
    return eval(_r_do_4479735312_code, globals(), context), i


# ->(w.block("divider", indent, None))
def _r_do_4479735760(stream, i, context):
    # w.block("divider", indent, None)
    return eval(_r_do_4479735760_code, globals(), context), i


# ->(w.block("sep", indent, tx, level=len(line)))
def _r_do_4479736528(stream, i, context):
    # w.block("sep", indent, tx, level=len(line))
    return eval(_r_do_4479736528_code, globals(), context), i


# ->(w.block("pre", indent, tx, lang=lang))
def _r_do_4479737104(stream, i, context):
    # w.block("pre", indent, tx, lang=lang)
    return eval(_r_do_4479737104_code, globals(), context), i


# ->(w.span("supertitle", tx))
def _r_do_4479783184(stream, i, context):
    # w.span("supertitle", tx)
    return eval(_r_do_4479783184_code, globals(), context), i


# ->(None)
def _r_do_4479783440(stream, i, context):
    # None
    return eval(_r_do_4479783440_code, globals(), context), i


# ->(w.span("subtitle", tx))
def _r_do_4479784144(stream, i, context):
    # w.span("subtitle", tx)
    return eval(_r_do_4479784144_code, globals(), context), i


# ->(w.block("title", indent, supt + tx + subt, level=0))
def _r_do_4479786192(stream, i, context):
    # w.block("title", indent, supt + tx + subt, level=0)
    return eval(_r_do_4479786192_code, globals(), context), i


# ->(tag)
def _r_do_4479811664(stream, i, context):
    # tag
    return eval(_r_do_4479811664_code, globals(), context), i


# ->(w.block("h", indent, tx, level=len(eqs), id=tag[0] if tag else None, container=True))
def _r_do_4479813840(stream, i, context):
    # w.block("h", indent, tx, level=len(eqs), id=tag[0] if tag else None, container=True)
    return eval(_r_do_4479813840_code, globals(), context), i


# ->(w.block(n + "_section", 0, tx, level=1, role="section", id=n, container=True))
def _r_do_4479815440(stream, i, context):
    # w.block(n + "_section", 0, tx, level=1, role="section", id=n, container=True)
    return eval(_r_do_4479815440_code, globals(), context), i


# ->(n[0] if n else None)
def _r_do_4479832912(stream, i, context):
    # n[0] if n else None
    return eval(_r_do_4479832912_code, globals(), context), i


# ->(w.block("summary", indent, tx))
def _r_do_4479833040(stream, i, context):
    # w.block("summary", indent, tx)
    return eval(_r_do_4479833040_code, globals(), context), i


# ->(w.block(it or "item", indent, tx, role="item"))
def _r_do_4479834448(stream, i, context):
    # w.block(it or "item", indent, tx, role="item")
    return eval(_r_do_4479834448_code, globals(), context), i


# ->(w.block(it.lower(), indent, tx, role="item"))
def _r_do_4479835664(stream, i, context):
    # w.block(it.lower(), indent, tx, role="item")
    return eval(_r_do_4479835664_code, globals(), context), i


# ->(w.block("prop", indent, None, name=k, value=v + "".join(extras)))
def _r_do_4479857296(stream, i, context):
    # w.block("prop", indent, None, name=k, value=v + "".join(extras))
    return eval(_r_do_4479857296_code, globals(), context), i


# ->(line)
def _r_do_4479858576(stream, i, context):
    # line
    return eval(_r_do_4479858576_code, globals(), context), i


# ->(w.block("pxml", indent, tx, tag=n, attrs=alist))
def _r_do_4479859024(stream, i, context):
    # w.block("pxml", indent, tx, tag=n, attrs=alist)
    return eval(_r_do_4479859024_code, globals(), context), i


# ->(b)
def _r_do_4479860688(stream, i, context):
    # b
    return eval(_r_do_4479860688_code, globals(), context), i


# ->(w.span("xml", '', tag=n, attrs=alist))
def _r_do_4481034256(stream, i, context):
    # w.span("xml", '', tag=n, attrs=alist)
    return eval(_r_do_4481034256_code, globals(), context), i


# ->(dict(attrs))
def _r_do_4481040720(stream, i, context):
    # dict(attrs)
    return eval(_r_do_4481040720_code, globals(), context), i


# ->(compat.unichr(8804))
def _r_do_4481290320(stream, i, context):
    # compat.unichr(8804)
    return eval(_r_do_4481290320_code, globals(), context), i


# ->(compat.unichr(8805))
def _r_do_4481290512(stream, i, context):
    # compat.unichr(8805)
    return eval(_r_do_4481290512_code, globals(), context), i


# ->(compat.unichr(8230))
def _r_do_4481291344(stream, i, context):
    # compat.unichr(8230)
    return eval(_r_do_4481291344_code, globals(), context), i


# ->(compat.unichr(8594))
def _r_do_4481291600(stream, i, context):
    # compat.unichr(8594)
    return eval(_r_do_4481291600_code, globals(), context), i


# ->(c)
def _r_do_4481291728(stream, i, context):
    # c
    return eval(_r_do_4481291728_code, globals(), context), i


# ->(compat.unichr(8660))
def _r_do_4481293200(stream, i, context):
    # compat.unichr(8660)
    return eval(_r_do_4481293200_code, globals(), context), i


# ->(compat.unichr(8592))
def _r_do_4481293520(stream, i, context):
    # compat.unichr(8592)
    return eval(_r_do_4481293520_code, globals(), context), i


# ->(w.span("link", tx, scheme=name, value=value))
def _r_do_4481331408(stream, i, context):
    # w.span("link", tx, scheme=name, value=value)
    return eval(_r_do_4481331408_code, globals(), context), i


# ->(("dt", None))
def _r_do_4481334800(stream, i, context):
    # ("dt", None)
    return eval(_r_do_4481334800_code, globals(), context), i


# ->(w.span("em", tx))
def _r_do_4481355920(stream, i, context):
    # w.span("em", tx)
    return eval(_r_do_4481355920_code, globals(), context), i


# ->((k, v))
def _r_do_4481358096(stream, i, context):
    # (k, v)
    return eval(_r_do_4481358096_code, globals(), context), i


# ->(w.span("env", [], name=n))
def _r_do_4481358160(stream, i, context):
    # w.span("env", [], name=n)
    return eval(_r_do_4481358160_code, globals(), context), i


# ->(w.span("link", None, scheme="Glyph", value=v))
def _r_do_4481358352(stream, i, context):
    # w.span("link", None, scheme="Glyph", value=v)
    return eval(_r_do_4481358352_code, globals(), context), i


# ->(w.span("code", tx))
def _r_do_4481358608(stream, i, context):
    # w.span("code", tx)
    return eval(_r_do_4481358608_code, globals(), context), i


# ->('')
def _r_do_4481385552(stream, i, context):
    # ''
    return eval(_r_do_4481385552_code, globals(), context), i


# ->(compat.unichr(174))
def _r_do_4481386832(stream, i, context):
    # compat.unichr(174)
    return eval(_r_do_4481386832_code, globals(), context), i


# ->(compat.unichr(215))
def _r_do_4481387280(stream, i, context):
    # compat.unichr(215)
    return eval(_r_do_4481387280_code, globals(), context), i


# ->(compat.unichr(8482))
def _r_do_4481387344(stream, i, context):
    # compat.unichr(8482)
    return eval(_r_do_4481387344_code, globals(), context), i


# ->(compat.unichr(169))
def _r_do_4481387600(stream, i, context):
    # compat.unichr(169)
    return eval(_r_do_4481387600_code, globals(), context), i


# ->('')
def _r_do_4481387664(stream, i, context):
    # ''
    return eval(_r_do_4481387664_code, globals(), context), i


# ->(" " + compat.unichr(9656) + " ")
def _r_do_4481388048(stream, i, context):
    # " " + compat.unichr(9656) + " "
    return eval(_r_do_4481388048_code, globals(), context), i


# ->(w.span("var", tx))
def _r_do_4481410832(stream, i, context):
    # w.span("var", tx)
    return eval(_r_do_4481410832_code, globals(), context), i


# ->(w.span("ui", tx))
def _r_do_4481411664(stream, i, context):
    # w.span("ui", tx)
    return eval(_r_do_4481411664_code, globals(), context), i


# ->(w.span("strong", tx))
def _r_do_4481412048(stream, i, context):
    # w.span("strong", tx)
    return eval(_r_do_4481412048_code, globals(), context), i


# ->(int(d))
def _r_do_4481429968(stream, i, context):
    # int(d)
    return eval(_r_do_4481429968_code, globals(), context), i


# ->(compat.unichr(8217))
def _r_do_4481430736(stream, i, context):
    # compat.unichr(8217)
    return eval(_r_do_4481430736_code, globals(), context), i


# ->(compat.unichr(num))
def _r_do_4481430864(stream, i, context):
    # compat.unichr(num)
    return eval(_r_do_4481430864_code, globals(), context), i


# ->(util.decode_named_entity(n))
def _r_do_4481430928(stream, i, context):
    # util.decode_named_entity(n)
    return eval(_r_do_4481430928_code, globals(), context), i


# ->(compat.unichr(8212) if len(d) == 3 else compat.unichr(8211))
def _r_do_4481430992(stream, i, context):
    # compat.unichr(8212) if len(d) == 3 else compat.unichr(8211)
    return eval(_r_do_4481430992_code, globals(), context), i


# ->(' ' + c)
def _r_do_4481433040(stream, i, context):
    # ' ' + c
    return eval(_r_do_4481433040_code, globals(), context), i


# ->(char)
def _r_do_4481433360(stream, i, context):
    # char
    return eval(_r_do_4481433360_code, globals(), context), i


# ->(w.span("keys", None, keys=[k] + kk))
def _r_do_4481455248(stream, i, context):
    # w.span("keys", None, keys=[k] + kk)
    return eval(_r_do_4481455248_code, globals(), context), i


# ->(w.span("xml", tx, tag=n, attrs=alist))
def _r_do_4481456400(stream, i, context):
    # w.span("xml", tx, tag=n, attrs=alist)
    return eval(_r_do_4481456400_code, globals(), context), i


# ->(w.span("link", '', scheme=name, value=value))
def _r_do_4481457232(stream, i, context):
    # w.span("link", '', scheme=name, value=value)
    return eval(_r_do_4481457232_code, globals(), context), i


# ->(int(h, 16))
def _r_do_4481495184(stream, i, context):
    # int(h, 16)
    return eval(_r_do_4481495184_code, globals(), context), i


# ->(c)
def _r_do_4481496656(stream, i, context):
    # c
    return eval(_r_do_4481496656_code, globals(), context), i


# ->(len(indent))
def _r_do_4481497296(stream, i, context):
    # len(indent)
    return eval(_r_do_4481497296_code, globals(), context), i


# (fail $break_)
def _r_failif_4481043472(stream, i, context):
    return (Failure if break_(stream, i, context)[0] is not Miss else Miss), i


# (fail $break_)
def _r_failif_4481332304(stream, i, context):
    return (Failure if break_(stream, i, context)[0] is not Miss else Miss), i


# (fail $break_)
def _r_failif_4481333264(stream, i, context):
    return (Failure if break_(stream, i, context)[0] is not Miss else Miss), i


# (fail $break_)
def _r_failif_4481356688(stream, i, context):
    return (Failure if break_(stream, i, context)[0] is not Miss else Miss), i


# (fail $break_)
def _r_failif_4481356880(stream, i, context):
    return (Failure if break_(stream, i, context)[0] is not Miss else Miss), i


# (fail $break_)
def _r_failif_4481357136(stream, i, context):
    return (Failure if break_(stream, i, context)[0] is not Miss else Miss), i


# (fail $break_)
def _r_failif_4481409296(stream, i, context):
    return (Failure if break_(stream, i, context)[0] is not Miss else Miss), i


# (fail $break_)
def _r_failif_4481410640(stream, i, context):
    return (Failure if break_(stream, i, context)[0] is not Miss else Miss), i


# ?(nextin < indent or nextin > indent + bwidth)
def _r_if_4479734864(stream, i, context):
    if eval(_r_if_4479734864_code, globals(), context):
        return Empty, i
    else:
        return Miss, i


# ?(len(eqs) > 1)
def _r_if_4479812560(stream, i, context):
    if eval(_r_if_4479812560_code, globals(), context):
        return Empty, i
    else:
        return Miss, i


# ?(eqs == eqs2)
def _r_if_4479813136(stream, i, context):
    if eval(_r_if_4479813136_code, globals(), context):
        return Empty, i
    else:
        return Miss, i


# ?(line.strip())
def _r_if_4479857872(stream, i, context):
    if eval(_r_if_4479857872_code, globals(), context):
        return Empty, i
    else:
        return Miss, i


# ?(nextin > indent)
def _r_if_4479859728(stream, i, context):
    if eval(_r_if_4479859728_code, globals(), context):
        return Empty, i
    else:
        return Miss, i


# ?(n == name)
def _r_if_4481042128(stream, i, context):
    if eval(_r_if_4481042128_code, globals(), context):
        return Empty, i
    else:
        return Miss, i


# ?(c.isalpha())
def _r_if_4481495312(stream, i, context):
    if eval(_r_if_4481495312_code, globals(), context):
        return Empty, i
    else:
        return Miss, i


# ?(nextin != indent)
def _r_if_4481495632(stream, i, context):
    if eval(_r_if_4481495632_code, globals(), context):
        return Empty, i
    else:
        return Miss, i


# ?(nextin < indent)
def _r_if_4481497360(stream, i, context):
    if eval(_r_if_4481497360_code, globals(), context):
        return Empty, i
    else:
        return Miss, i


# ?(nextin > indent)
def _r_if_4481497424(stream, i, context):
    if eval(_r_if_4481497424_code, globals(), context):
        return Empty, i
    else:
        return Miss, i


# I'\n\r'
def _r_in_4475775184(stream, i, context):
    __xs = '\n\r'
    if i < len(stream) and stream[i] in __xs:
        return stream[i], i + 1
    else:
        return Miss, i


# Ifrozenset([u'*', u'-'])
def _r_in_4479710800(stream, i, context):
    __xs = u'*-'
    if i < len(stream) and stream[i] in __xs:
        return stream[i], i + 1
    else:
        return Miss, i


# Ifrozenset([u':', u' ', '\n'])
def _r_in_4479857488(stream, i, context):
    __xs = u': \n'
    if i < len(stream) and stream[i] in __xs:
        return stream[i], i + 1
    else:
        return Miss, i


# Ifrozenset([u'A', u'C', u'B', u'E', u'D', u'F', u'a', u'c', u'b', u'e', u'd', u'f', u'1', u'0', u'3', u'2', u'5', u'4', u'7', u'6', u'9', u'8'])
def _r_in_4481430608(stream, i, context):
    __xs = u'ACBEDFacbedf1032547698'
    if i < len(stream) and stream[i] in __xs:
        return stream[i], i + 1
    else:
        return Miss, i


# Ifrozenset([u's', u'S', u't', u'T'])
def _r_in_4481431760(stream, i, context):
    __xs = u'sStT'
    if i < len(stream) and stream[i] in __xs:
        return stream[i], i + 1
    else:
        return Miss, i


# (^$digit)
def _r_lookbehind_4481293392(stream, i, context):
    start = i - 1
    if start >= 0:
        out, newi = digit(stream, start, context)
        if out is not Miss and newi == i:
            return Empty, i
    return Miss, i


# (^Su'_')
def _r_lookbehind_4481356304(stream, i, context):
    start = i - 1
    if start >= 0:
        out, newi = _r_string_4481357392(stream, start, context)
        if out is not Miss and newi == i:
            return Empty, i
    return Miss, i


# (^$alphanum)
def _r_lookbehind_4481384592(stream, i, context):
    start = i - 1
    if start >= 0:
        out, newi = alphanum(stream, start, context)
        if out is not Miss and newi == i:
            return Empty, i
    return Miss, i


# (^Su'*')
def _r_lookbehind_4481409360(stream, i, context):
    start = i - 1
    if start >= 0:
        out, newi = _r_string_4481409744(stream, start, context)
        if out is not Miss and newi == i:
            return Empty, i
    return Miss, i


# (^Su'_')
def _r_lookbehind_4481410576(stream, i, context):
    start = i - 1
    if start >= 0:
        out, newi = _r_string_4481411920(stream, start, context)
        if out is not Miss and newi == i:
            return Empty, i
    return Miss, i


# (^Su'<')
def _r_lookbehind_4481411408(stream, i, context):
    start = i - 1
    if start >= 0:
        out, newi = _r_string_4481409616(stream, start, context)
        if out is not Miss and newi == i:
            return Empty, i
    return Miss, i


# (^Su'-')
def _r_lookbehind_4481430288(stream, i, context):
    start = i - 1
    if start >= 0:
        out, newi = _r_string_4481430224(stream, start, context)
        if out is not Miss and newi == i:
            return Empty, i
    return Miss, i


# (^$alphachar)
def _r_lookbehind_4481432656(stream, i, context):
    start = i - 1
    if start >= 0:
        out, newi = alphachar(stream, start, context)
        if out is not Miss and newi == i:
            return Empty, i
    return Miss, i


# @($para_ending, $spans)
def _r_mixed_4479710544(stream, i, context):
    target = spans
    firsts = set((u'`', '\t', u'[', u'_', u' ', u'%', u"'", u'&', u'(', u'+', u'*', u'-', u'/', u'.', u'x', u'=', u'<'))
    context = context.push()
    until = para_ending
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @($bullet_ending, $spans)
def _r_mixed_4479712912(stream, i, context):
    target = spans
    firsts = set((u'`', '\t', u'[', u'_', u' ', u'%', u"'", u'&', u'(', u'+', u'*', u'-', u'/', u'.', u'x', u'=', u'<'))
    context = context.push()
    until = bullet_ending
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @($sepend, $stylespans)
def _r_mixed_4479736400(stream, i, context):
    target = stylespans
    firsts = set((u' ', u'`', u'%', u"'", u'&', '\t', u'(', u'+', u'\n', u'-', u'/', u'.', u'\uffff', u'x', u'=', u'<', u'_'))
    context = context.push()
    until = sepend
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @(($hspace* Su'|>'), $stylespans)
def _r_mixed_4479737232(stream, i, context):
    target = stylespans
    firsts = set((u' ', u'`', u'%', u"'", u'&', '\t', u'(', u'+', u'\n', u'-', u'/', u'.', u'\uffff', u'x', u'=', u'<', u'_'))
    context = context.push()
    until = _r_seq_4479783248
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @(Su'}}}', None)
def _r_mixed_4479737424(stream, i, context):
    until = _r_string_4479737552
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @(($hspace* Su'='), $stylespans)
def _r_mixed_4479783760(stream, i, context):
    target = stylespans
    firsts = set((u' ', u'`', u'%', u"'", u'&', '\t', u'(', u'+', u'\n', u'-', u'/', u'.', u'\uffff', u'x', u'=', u'<', u'_'))
    context = context.push()
    until = _r_seq_4479784720
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @((($hspace* Su'=') | Su'<|'), $stylespans)
def _r_mixed_4479784976(stream, i, context):
    target = stylespans
    firsts = set((u' ', u'`', u'%', u"'", u'&', '\t', u'(', u'+', u'\n', u'-', u'/', u'.', u'\uffff', u'x', u'=', u'<', u'_'))
    context = context.push()
    until = _r_or_4479785680
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @(($hspace* Su'='), $stylespans)
def _r_mixed_4479812624(stream, i, context):
    target = stylespans
    firsts = set((u' ', u'`', u'%', u"'", u'&', '\t', u'(', u'+', u'\n', u'-', u'/', u'.', u'\uffff', u'x', u'=', u'<', u'_'))
    context = context.push()
    until = _r_seq_4479813200
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @($lineend, $stylespans)
def _r_mixed_4479814736(stream, i, context):
    target = stylespans
    firsts = set((u' ', u'`', u'%', u"'", u'&', '\t', u'(', u'+', u'\n', u'-', u'/', u'.', u'\uffff', u'x', u'=', u'<', u'_'))
    context = context.push()
    until = lineend
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @(($break_ | Su'"""'), $spans)
def _r_mixed_4479815568(stream, i, context):
    target = spans
    firsts = set((u'`', '\t', u'[', u'_', u' ', u'%', u"'", u'&', u'(', u'+', u'*', u'-', u'/', u'.', u'x', u'=', u'<'))
    context = context.push()
    until = _r_or_4479832400
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @($itemend, $spans)
def _r_mixed_4479834256(stream, i, context):
    target = spans
    firsts = set((u'`', '\t', u'[', u'_', u' ', u'%', u"'", u'&', u'(', u'+', u'*', u'-', u'/', u'.', u'x', u'=', u'<'))
    context = context.push()
    until = itemend
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @(S'\n', $stylespans)
def _r_mixed_4479835088(stream, i, context):
    target = stylespans
    firsts = set((u' ', u'`', u'%', u"'", u'&', '\t', u'(', u'+', u'\n', u'-', u'/', u'.', u'\uffff', u'x', u'=', u'<', u'_'))
    context = context.push()
    until = _r_string_4479835024
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @(Ifrozenset([u':', u' ', '\n']), None)
def _r_mixed_4479857360(stream, i, context):
    until = _r_in_4479857488
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @($lineend, None)
def _r_mixed_4479857808(stream, i, context):
    until = lineend
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @($lineend, $spans)
def _r_mixed_4479858768(stream, i, context):
    target = spans
    firsts = set((u'`', '\t', u'[', u'_', u' ', u'%', u"'", u'&', u'(', u'+', u'*', u'-', u'/', u'.', u'x', u'=', u'<'))
    context = context.push()
    until = lineend
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @((Su')' | (fail $break_)), None)
def _r_mixed_4481359568(stream, i, context):
    until = _r_or_4481043344
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @((Su'`' | (fail $break_)), $var)
def _r_mixed_4481359760(stream, i, context):
    target = var
    firsts = set((u'<'))
    context = context.push()
    until = _r_or_4481357264
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @(Su'-->', None)
def _r_mixed_4481386064(stream, i, context):
    until = _r_string_4481386000
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @($lineend, None)
def _r_mixed_4481387088(stream, i, context):
    until = lineend
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @((Su'*' | (fail $break_)), $inline)
def _r_mixed_4481411344(stream, i, context):
    target = inline
    firsts = set((u' ', '\t', u'\n', u'[', u'_', u'`', u'%', u"'", u'&', u'(', u'+', u'*', u'-', u'/', u'.', u'x', u'=', u'<', u'\uffff'))
    context = context.push()
    until = _r_or_4481413008
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @((Su'>>' | (fail $break_)), $inline)
def _r_mixed_4481411472(stream, i, context):
    target = inline
    firsts = set((u' ', '\t', u'\n', u'[', u'_', u'`', u'%', u"'", u'&', u'(', u'+', u'*', u'-', u'/', u'.', u'x', u'=', u'<', u'\uffff'))
    context = context.push()
    until = _r_or_4481411728
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @((Su'__' | (fail $break_)), ($uisep | $inline))
def _r_mixed_4481411792(stream, i, context):
    target = _r_or_4481410448
    firsts = set((u'`', '\t', '\n', '\r', u'[', u'_', u' ', u'%', u"'", u'&', u'(', u'+', u'*', u'-', u'/', u'.', u'x', u'=', u'<', u'\uffff'))
    context = context.push()
    until = _r_or_4481411152
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @((Su'_' | (fail $break_)), $inline)
def _r_mixed_4481412944(stream, i, context):
    target = inline
    firsts = set((u' ', '\t', u'\n', u'[', u'_', u'`', u'%', u"'", u'&', u'(', u'+', u'*', u'-', u'/', u'.', u'x', u'=', u'<', u'\uffff'))
    context = context.push()
    until = _r_or_4481359312
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @(Su'|', $stylespans)
def _r_mixed_4481456144(stream, i, context):
    target = stylespans
    firsts = set((u' ', u'`', u'%', u"'", u'&', '\t', u'(', u'+', u'\n', u'-', u'/', u'.', u'\uffff', u'x', u'=', u'<', u'_'))
    context = context.push()
    until = _r_string_4481454224
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# @(Su'</', $spans)
def _r_mixed_4481458064(stream, i, context):
    target = spans
    firsts = set((u'`', '\t', u'[', u'_', u' ', u'%', u"'", u'&', u'(', u'+', u'*', u'-', u'/', u'.', u'x', u'=', u'<'))
    context = context.push()
    until = _r_string_4481456592
    lasti = _i = i
    length = len(stream)
    if stream.endswith(u'\uffff'):
        length -= 1
    output = []
    while i < length:
        out, _ = until(stream, i, context)
        if out is not Miss: break
        if not firsts or stream[i] in firsts:
            out, newi = target(stream, i, context)
            if out is Failure:
                return Miss, _i
            if out is not Miss:
                if newi <= i: raise ParserError
                if i > lasti:
                    output.append(stream[lasti:i])
                output.append(out)
                lasti = i = newi
                continue
        i += 1
    if i > lasti:
        output.append(stream[lasti:i])
    return output, i


# (~Su')')
def _r_not_4479813648(stream, i, context):
    return (Empty if _r_string_4479813968(stream, i, context)[0] is Miss else Miss), i


# (~Su'"')
def _r_not_4481034064(stream, i, context):
    return (Empty if _r_string_4481457296(stream, i, context)[0] is Miss else Miss), i


# (~Su'_')
def _r_not_4481358992(stream, i, context):
    return (Empty if _r_string_4481359440(stream, i, context)[0] is Miss else Miss), i


# (~Su'*')
def _r_not_4481359696(stream, i, context):
    return (Empty if _r_string_4481359248(stream, i, context)[0] is Miss else Miss), i


# (~(^$alphanum))
def _r_not_4481386192(stream, i, context):
    return (Empty if _r_lookbehind_4481384592(stream, i, context)[0] is Miss else Miss), i


# (~Su'>')
def _r_not_4481410000(stream, i, context):
    return (Empty if _r_string_4481410320(stream, i, context)[0] is Miss else Miss), i


# (~(^Su'_'))
def _r_not_4481410064(stream, i, context):
    return (Empty if _r_lookbehind_4481356304(stream, i, context)[0] is Miss else Miss), i


# (~(^Su'<'))
def _r_not_4481410128(stream, i, context):
    return (Empty if _r_lookbehind_4481411408(stream, i, context)[0] is Miss else Miss), i


# (~$alphanum)
def _r_not_4481410384(stream, i, context):
    return (Empty if alphanum(stream, i, context)[0] is Miss else Miss), i


# (~Su'_')
def _r_not_4481411216(stream, i, context):
    return (Empty if _r_string_4481410512(stream, i, context)[0] is Miss else Miss), i


# (~(^Su'*'))
def _r_not_4481412496(stream, i, context):
    return (Empty if _r_lookbehind_4481409360(stream, i, context)[0] is Miss else Miss), i


# (~(^Su'_'))
def _r_not_4481413072(stream, i, context):
    return (Empty if _r_lookbehind_4481410576(stream, i, context)[0] is Miss else Miss), i


# (~(^Su'-'))
def _r_not_4481431568(stream, i, context):
    return (Empty if _r_lookbehind_4481430288(stream, i, context)[0] is Miss else Miss), i


# (~Su'-')
def _r_not_4481431824(stream, i, context):
    return (Empty if _r_string_4481291856(stream, i, context)[0] is Miss else Miss), i


# (~Su'(')
def _r_not_4481454288(stream, i, context):
    return (Empty if _r_string_4481455504(stream, i, context)[0] is Miss else Miss), i


# (~(Su' ' | Su'))'))
def _r_not_4481454672(stream, i, context):
    return (Empty if _r_or_4481457104(stream, i, context)[0] is Miss else Miss), i


# $ws?
def _r_opt_4479734544(stream, i, context):
    out, newi = ws(stream, i, context)
    if out is Miss:
        return [], i
    else:
        return [out], newi


# $supertitle?
def _r_opt_4479784528(stream, i, context):
    out, newi = supertitle(stream, i, context)
    if out is Miss:
        return [], i
    else:
        return [out], newi


# $subtitle?
def _r_opt_4479785104(stream, i, context):
    out, newi = subtitle(stream, i, context)
    if out is Miss:
        return [], i
    else:
        return [out], newi


# $heading_tag?
def _r_opt_4479812368(stream, i, context):
    out, newi = heading_tag(stream, i, context)
    if out is Miss:
        return [], i
    else:
        return [out], newi


# $emptylines?
def _r_opt_4479813776(stream, i, context):
    out, newi = emptylines(stream, i, context)
    if out is Miss:
        return [], i
    else:
        return [out], newi


# $identifier?
def _r_opt_4479814864(stream, i, context):
    out, newi = identifier(stream, i, context)
    if out is Miss:
        return [], i
    else:
        return [out], newi


# Su':'?
def _r_opt_4479833104(stream, i, context):
    out, newi = _r_string_4479833616(stream, i, context)
    if out is Miss:
        return [], i
    else:
        return [out], newi


# $emptylines?
def _r_opt_4479835280(stream, i, context):
    out, newi = emptylines(stream, i, context)
    if out is Miss:
        return [], i
    else:
        return [out], newi


# $emptylines?
def _r_opt_4481334608(stream, i, context):
    out, newi = emptylines(stream, i, context)
    if out is Miss:
        return [], i
    else:
        return [out], newi


# $emptylines?
def _r_opt_4481495952(stream, i, context):
    out, newi = emptylines(stream, i, context)
    if out is Miss:
        return [], i
    else:
        return [out], newi


# $emptylines?
def _r_opt_4481496528(stream, i, context):
    out, newi = emptylines(stream, i, context)
    if out is Miss:
        return [], i
    else:
        return [out], newi


# $emptylines?
def _r_opt_4481498000(stream, i, context):
    out, newi = emptylines(stream, i, context)
    if out is Miss:
        return [], i
    else:
        return [out], newi


# $emptylines?
def _r_opt_4481498448(stream, i, context):
    out, newi = emptylines(stream, i, context)
    if out is Miss:
        return [], i
    else:
        return [out], newi


# ($emptylines | ($ws? $streamend))
def _r_or_4479712464(stream, i, context):
    fm = _r_or_4479712464_fm
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


# (($ws Su'#!' $identifier) | ->(None))
def _r_or_4479737168(stream, i, context):
    fm = _r_or_4479737168_fm
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


# ($lineend | $streamend)
def _r_or_4479737744(stream, i, context):
    fm = _r_or_4479737744_fm
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


# (($hspace* Su'=') | Su'<|')
def _r_or_4479785680(stream, i, context):
    fm = _r_or_4479785680_fm
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


# (S'\n' | $streamend)
def _r_or_4479786128(stream, i, context):
    fm = _r_or_4479786128_fm
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


# (S'\n' | $streamend)
def _r_or_4479814224(stream, i, context):
    fm = _r_or_4479814224_fm
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


# (S'\n' | $streamend)
def _r_or_4479815504(stream, i, context):
    fm = _r_or_4479815504_fm
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


# ($break_ | Su'"""')
def _r_or_4479832400(stream, i, context):
    fm = _r_or_4479832400_fm
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


# (Su'TIP' | Su'NOTE' | Su'WARNING')
def _r_or_4479834960(stream, i, context):
    fm = _r_or_4479834960_fm
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


# ($bullet_start | $ord_start | Su'==' | $itemtype | Su'{{{' | Su'~~')
def _r_or_4479859920(stream, i, context):
    fm = _r_or_4479859920_fm
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


# (Su')' | (fail $break_))
def _r_or_4481043344(stream, i, context):
    fm = _r_or_4481043344_fm
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


# ((Su'(c)' ->(compat.unichr(169))) | (Su'(tm)' ->(compat.unichr(8482))) | (Su'(r)' ->(compat.unichr(174))))
def _r_or_4481292240(stream, i, context):
    fm = _r_or_4481292240_fm
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


# ($lineend | (~~$space))
def _r_or_4481293904(stream, i, context):
    fm = _r_or_4481293904_fm
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


# (Su'`' | (fail $break_))
def _r_or_4481357264(stream, i, context):
    fm = _r_or_4481357264_fm
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


# (Su'_' | (fail $break_))
def _r_or_4481359312(stream, i, context):
    fm = _r_or_4481359312_fm
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


# ($digit | $hspace | $streamend)
def _r_or_4481386768(stream, i, context):
    fm = _r_or_4481386768_fm
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


# ($uisep | $inline)
def _r_or_4481410448(stream, i, context):
    fm = _r_or_4481410448_fm
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


# (Su'__' | (fail $break_))
def _r_or_4481411152(stream, i, context):
    fm = _r_or_4481411152_fm
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


# (Su'>>' | (fail $break_))
def _r_or_4481411728(stream, i, context):
    fm = _r_or_4481411728_fm
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


# (Su'*' | (fail $break_))
def _r_or_4481413008(stream, i, context):
    fm = _r_or_4481413008_fm
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


# ((Su'<-' ->(compat.unichr(8592))) | (Su'->' ->(compat.unichr(8594))) | (Su'<=' ->(compat.unichr(8804))) | (Su'=>' ->(compat.unichr(8805))) | (Su'<=>' ->(compat.unichr(8660))))
def _r_or_4481429584(stream, i, context):
    fm = _r_or_4481429584_fm
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


# (Su'---' | Su'--')
def _r_or_4481429776(stream, i, context):
    fm = _r_or_4481429776_fm
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


# (Su'll' | Su'LL' | Su'nt' | Su'NT' | Ifrozenset([u's', u'S', u't', u'T']))
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


# ($num_entity | $named_entity)
def _r_or_4481432848(stream, i, context):
    fm = _r_or_4481432848_fm
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


# (($hspace+ $keyname) | ((~Su'(') $keyname))
def _r_or_4481454800(stream, i, context):
    fm = _r_or_4481454800_fm
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


# (Su' ' | Su'))')
def _r_or_4481457104(stream, i, context):
    fm = _r_or_4481457104_fm
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


# ($hspace | $vspace)
def _r_or_4481498064(stream, i, context):
    fm = _r_or_4481498064_fm
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


# (~~$indentinc)
def _r_peek_4479710032(stream, i, context):
    return (Miss if indentinc(stream, i, context)[0] is Miss else Empty), i


# (~~(($lstart):nextin ?(nextin < indent or nextin > indent + bwidth)))
def _r_peek_4479712656(stream, i, context):
    return (Miss if _r_seq_4479713232(stream, i, context)[0] is Miss else Empty), i


# (~~$starters)
def _r_peek_4479712848(stream, i, context):
    return (Miss if starters(stream, i, context)[0] is Miss else Empty), i


# (~~$indentinc)
def _r_peek_4479835408(stream, i, context):
    return (Miss if indentinc(stream, i, context)[0] is Miss else Empty), i


# (~~(($lstart):nextin ?(nextin > indent)))
def _r_peek_4479858128(stream, i, context):
    return (Miss if _r_seq_4479858896(stream, i, context)[0] is Miss else Empty), i


# (~~$spaceorpunct)
def _r_peek_4481293072(stream, i, context):
    return (Miss if spaceorpunct(stream, i, context)[0] is Miss else Empty), i


# (~~$starters)
def _r_peek_4481334544(stream, i, context):
    return (Miss if starters(stream, i, context)[0] is Miss else Empty), i


# (~~$indentinc)
def _r_peek_4481334928(stream, i, context):
    return (Miss if indentinc(stream, i, context)[0] is Miss else Empty), i


# (~~(~Su'_'))
def _r_peek_4481356048(stream, i, context):
    return (Miss if _r_not_4481358992(stream, i, context)[0] is Miss else Empty), i


# (~~$space)
def _r_peek_4481386384(stream, i, context):
    return (Miss if space(stream, i, context)[0] is Miss else Empty), i


# (~~($digit | $hspace | $streamend))
def _r_peek_4481387728(stream, i, context):
    return (Miss if _r_or_4481386768(stream, i, context)[0] is Miss else Empty), i


# (~~(~$alphanum))
def _r_peek_4481388368(stream, i, context):
    return (Miss if _r_not_4481410384(stream, i, context)[0] is Miss else Empty), i


# (~~(~Su'_'))
def _r_peek_4481409104(stream, i, context):
    return (Miss if _r_not_4481411216(stream, i, context)[0] is Miss else Empty), i


# (~~(~Su'*'))
def _r_peek_4481412112(stream, i, context):
    return (Miss if _r_not_4481359696(stream, i, context)[0] is Miss else Empty), i


# (~~(~Su'>'))
def _r_peek_4481412752(stream, i, context):
    return (Miss if _r_not_4481410000(stream, i, context)[0] is Miss else Empty), i


# (~~$xchar)
def _r_peek_4481431952(stream, i, context):
    return (Miss if xchar(stream, i, context)[0] is Miss else Empty), i


# (~~(Su'll' | Su'LL' | Su'nt' | Su'NT' | Ifrozenset([u's', u'S', u't', u'T'])))
def _r_peek_4481432080(stream, i, context):
    return (Miss if _r_or_4481430544(stream, i, context)[0] is Miss else Empty), i


# (~~$xchar)
def _r_peek_4481432976(stream, i, context):
    return (Miss if xchar(stream, i, context)[0] is Miss else Empty), i


# Ifrozenset([u'*', u'-'])+
def _r_plus_4479709776(stream, i, context):
    target = _r_in_4479710800
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


# Su' '+
def _r_plus_4479710864(stream, i, context):
    target = _r_string_4479711120
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


# Su'#'+
def _r_plus_4479710928(stream, i, context):
    target = _r_string_4479711440
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


# Su' '+
def _r_plus_4479711568(stream, i, context):
    target = _r_string_4479711184
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


# ((~Su')') Any)+
def _r_plus_4479812304(stream, i, context):
    target = _r_seq_4479812880
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


# $space+
def _r_plus_4481387472(stream, i, context):
    target = space
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


# $space+
def _r_plus_4481387920(stream, i, context):
    target = space
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


# Ifrozenset([u'A', u'C', u'B', u'E', u'D', u'F', u'a', u'c', u'b', u'e', u'd', u'f', u'1', u'0', u'3', u'2', u'5', u'4', u'7', u'6', u'9', u'8'])+
def _r_plus_4481430480(stream, i, context):
    target = _r_in_4481430608
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


# $digit+
def _r_plus_4481431056(stream, i, context):
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


# $hspace+
def _r_plus_4481455760(stream, i, context):
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


# ((~(Su' ' | Su'))')) Any)+
def _r_plus_4481457744(stream, i, context):
    target = _r_seq_4481454608
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


# R(.*$)
def _r_regex_4479857936(stream, i, context):
    __m = _r_regex_4479857936_re.match(stream, i)
    if __m:
        context.update(__m.groupdict())
        return __m.group(0), __m.end()
    return Miss, i


# R([A-Za-z_0-9]+)
def _r_regex_4481429840(stream, i, context):
    __m = _r_regex_4481429840_re.match(stream, i)
    if __m:
        context.update(__m.groupdict())
        return __m.group(0), __m.end()
    return Miss, i


# R([A-Za-z]+)
def _r_regex_4481431184(stream, i, context):
    __m = _r_regex_4481431184_re.match(stream, i)
    if __m:
        context.update(__m.groupdict())
        return __m.group(0), __m.end()
    return Miss, i


# R([-A-Za-z_0-9]+)
def _r_regex_4481432208(stream, i, context):
    __m = _r_regex_4481432208_re.match(stream, i)
    if __m:
        context.update(__m.groupdict())
        return __m.group(0), __m.end()
    return Miss, i


# Su'~'{2, None}
def _r_repeat_4479735376(stream, i, context):
    target = _r_string_4479736208
    _i = i
    times = 0
    output = []
    length = len(stream)
    maxtimes = None
    mintimes = 2
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


# Su'='{2, None}
def _r_repeat_4479811920(stream, i, context):
    target = _r_string_4479811984
    _i = i
    times = 0
    output = []
    length = len(stream)
    maxtimes = None
    mintimes = 2
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


# Su'='{2, None}
def _r_repeat_4479812496(stream, i, context):
    target = _r_string_4479813008
    _i = i
    times = 0
    output = []
    length = len(stream)
    maxtimes = None
    mintimes = 2
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


# (S'\n' (~~(($lstart):nextin ?(nextin < indent or nextin > indent + bwidth))))
def _r_seq_4479709712(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4479712272, _r_peek_4479712656):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (S'\n' (~~$starters))
def _r_seq_4479710672(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4479712592, _r_peek_4479712848):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (($lstart):nextin ?(nextin < indent or nextin > indent + bwidth))
def _r_seq_4479713232(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479734224, _r_if_4479734864):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ($ws? $streamend)
def _r_seq_4479734096(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_opt_4479734544, streamend):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ($ws Su'#!' $identifier)
def _r_seq_4479737296(stream, i, context):
    out = Miss
    _i = i
    for rule in (ws, _r_string_4479783120, identifier):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ($hspace* Su'|>')
def _r_seq_4479783248(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_star_4479784336, _r_string_4479784656):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ($hspace* Su'=')
def _r_seq_4479784720(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_star_4479785232, _r_string_4479785616):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ($hspace* Su'=')
def _r_seq_4479785872(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_star_4479786320, _r_string_4479786704):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((~Su')') Any)
def _r_seq_4479812880(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_not_4479813648, Any):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ($hspace* Su'=')
def _r_seq_4479813200(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_star_4479813584, _r_string_4479814352):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((~~(($lstart):nextin ?(nextin > indent))) (R(.*$)):line ?(line.strip()) $lineend ->(line))
def _r_seq_4479857168(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_peek_4479858128, _r_bind_4479857552, _r_if_4479857872, lineend, _r_do_4479858576):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (($lstart):nextin ?(nextin > indent))
def _r_seq_4479858896(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479859344, _r_if_4479859728):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((~Su'"') Any)
def _r_seq_4481042576(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_not_4481034064, Any):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'(c)' ->(compat.unichr(169)))
def _r_seq_4481291408(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481385296, _r_do_4481387600):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'->' ->(compat.unichr(8594)))
def _r_seq_4481292048(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481292560, _r_do_4481291600):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'(r)' ->(compat.unichr(174)))
def _r_seq_4481292688(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481385168, _r_do_4481386832):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'(tm)' ->(compat.unichr(8482)))
def _r_seq_4481292944(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481385872, _r_do_4481387344):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'<=>' ->(compat.unichr(8660)))
def _r_seq_4481293584(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481292816, _r_do_4481293200):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'=>' ->(compat.unichr(8805)))
def _r_seq_4481293776(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481293008, _r_do_4481290512):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'<=' ->(compat.unichr(8804)))
def _r_seq_4481294096(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481291920, _r_do_4481290320):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'||' $hspace* S'\n' ->(("cell", "th")))
def _r_seq_4481331280(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481335056, _r_star_4481334864, _r_string_4479709328, _r_do_4479709392):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ($break_ ->(("para", None)))
def _r_seq_4481331792(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (break_, _r_do_4479710096):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'|' $hspace* S'\n' (~~$indentinc) ->(("cell", "td")))
def _r_seq_4481332240(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4479709520, _r_star_4481335184, _r_string_4479709840, _r_peek_4479710032, _r_do_4479709264):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (S'\n' ($emptylines | ($ws? $streamend)))
def _r_seq_4481332560(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4479711760, _r_or_4479712464):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'<' ($xname):n ($attrlist):alist $ws Su'>' (@(Su'</', $spans)):tx u'ctag'(n) ->(w.span("xml", tx, tag=n, attrs=alist)))
def _r_seq_4481357968(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481457552, _r_bind_4481034192, _r_bind_4481034512, ws, _r_string_4481458000, _r_bind_4481035984, _r_call_4481456528, _r_do_4481456400):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'<' ($xname):n ($attrlist):alist $ws Su'/>' ->(w.span("xml", '', tag=n, attrs=alist)))
def _r_seq_4481358288(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481042768, _r_bind_4481043600, _r_bind_4481043728, ws, _r_string_4481033552, _r_do_4481034256):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su'<-' ->(compat.unichr(8592)))
def _r_seq_4481429904(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481292304, _r_do_4481293520):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ($hspace* Su'+' $hspace* $keyname)
def _r_seq_4481454352(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_star_4481454480, _r_string_4481455440, _r_star_4481456912, keyname):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((~(Su' ' | Su'))')) Any)
def _r_seq_4481454608(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_not_4481454672, Any):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (S'\n' (~~$starters))
def _r_seq_4481456080(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481334224, _r_peek_4481334544):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# (Su':' $hspace* S'\n' (~~$indentinc) $emptylines? ->(("dt", None)))
def _r_seq_4481456272(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481334416, _r_star_4481334032, _r_string_4481334672, _r_peek_4481334928, _r_opt_4481334608, _r_do_4481334800):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ($hspace+ $keyname)
def _r_seq_4481457424(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_plus_4481455760, keyname):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ((~Su'(') $keyname)
def _r_seq_4481457616(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_not_4481454288, keyname):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# ($linestart $hspace* S'\n')
def _r_seq_4481498128(stream, i, context):
    out = Miss
    _i = i
    for rule in (linestart, _r_star_4481496400, _r_string_4481498256):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# Su'~'*
def _r_star_4479734288(stream, i, context):
    target = _r_string_4479735632
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


# $hspace*
def _r_star_4479735120(stream, i, context):
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


# $hspace*
def _r_star_4479737360(stream, i, context):
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


# $hspace*
def _r_star_4479737808(stream, i, context):
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


# $hspace*
def _r_star_4479783376(stream, i, context):
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


# $hspace*
def _r_star_4479784336(stream, i, context):
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


# $hspace*
def _r_star_4479784784(stream, i, context):
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


# $hspace*
def _r_star_4479785232(stream, i, context):
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


# $hspace*
def _r_star_4479785424(stream, i, context):
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


# $hspace*
def _r_star_4479785488(stream, i, context):
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


# $hspace*
def _r_star_4479786064(stream, i, context):
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


# $hspace*
def _r_star_4479786320(stream, i, context):
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


# $hspace*
def _r_star_4479811856(stream, i, context):
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


# $hspace*
def _r_star_4479812048(stream, i, context):
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


# $hspace*
def _r_star_4479813328(stream, i, context):
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


# $hspace*
def _r_star_4479813584(stream, i, context):
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


# $hspace*
def _r_star_4479814160(stream, i, context):
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


# $hspace*
def _r_star_4479832144(stream, i, context):
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


# ((~~(($lstart):nextin ?(nextin > indent))) (R(.*$)):line ?(line.strip()) $lineend ->(line))*
def _r_star_4479834832(stream, i, context):
    target = _r_seq_4479857168
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


# $hspace*
def _r_star_4479835152(stream, i, context):
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


# $hspace*
def _r_star_4479860304(stream, i, context):
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


# $blocks*
def _r_star_4479894160(stream, i, context):
    target = blocks
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


# ((~Su'"') Any)*
def _r_star_4481040464(stream, i, context):
    target = _r_seq_4481042576
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


# $hspace*
def _r_star_4481293456(stream, i, context):
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


# $hspace*
def _r_star_4481334032(stream, i, context):
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


# $hspace*
def _r_star_4481334864(stream, i, context):
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


# $hspace*
def _r_star_4481335184(stream, i, context):
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


# $attr*
def _r_star_4481358864(stream, i, context):
    target = attr
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


# ($hspace* Su'+' $hspace* $keyname)*
def _r_star_4481454160(stream, i, context):
    target = _r_seq_4481454352
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


# $hspace*
def _r_star_4481454480(stream, i, context):
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


# $hspace*
def _r_star_4481456912(stream, i, context):
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


# $hspace*
def _r_star_4481458128(stream, i, context):
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


# $hspace*
def _r_star_4481496400(stream, i, context):
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


# $hspace*
def _r_star_4481497680(stream, i, context):
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


# S'\n'
def _r_string_4479709328(stream, i, context):
    string = '\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'|'
def _r_string_4479709520(stream, i, context):
    string = u'|'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\n'
def _r_string_4479709840(stream, i, context):
    string = '\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su' '
def _r_string_4479711120(stream, i, context):
    string = u' '
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su' '
def _r_string_4479711184(stream, i, context):
    string = u' '
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'#'
def _r_string_4479711440(stream, i, context):
    string = u'#'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\n'
def _r_string_4479711760(stream, i, context):
    string = '\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\n'
def _r_string_4479712272(stream, i, context):
    string = '\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\n'
def _r_string_4479712592(stream, i, context):
    string = '\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'~~'
def _r_string_4479735504(stream, i, context):
    string = u'~~'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'~'
def _r_string_4479735632(stream, i, context):
    string = u'~'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'~'
def _r_string_4479736208(stream, i, context):
    string = u'~'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'{{{'
def _r_string_4479737040(stream, i, context):
    string = u'{{{'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'}}}'
def _r_string_4479737488(stream, i, context):
    string = u'}}}'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'}}}'
def _r_string_4479737552(stream, i, context):
    string = u'}}}'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'#!'
def _r_string_4479783120(stream, i, context):
    string = u'#!'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'|>'
def _r_string_4479783504(stream, i, context):
    string = u'|>'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'<|'
def _r_string_4479783696(stream, i, context):
    string = u'<|'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'='
def _r_string_4479784592(stream, i, context):
    string = u'='
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'|>'
def _r_string_4479784656(stream, i, context):
    string = u'|>'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'='
def _r_string_4479785616(stream, i, context):
    string = u'='
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'='
def _r_string_4479785936(stream, i, context):
    string = u'='
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'('
def _r_string_4479786256(stream, i, context):
    string = u'('
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'='
def _r_string_4479786704(stream, i, context):
    string = u'='
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'<|'
def _r_string_4479786960(stream, i, context):
    string = u'<|'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su')'
def _r_string_4479811792(stream, i, context):
    string = u')'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'='
def _r_string_4479811984(stream, i, context):
    string = u'='
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\n'
def _r_string_4479812112(stream, i, context):
    string = '\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'='
def _r_string_4479813008(stream, i, context):
    string = u'='
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su')'
def _r_string_4479813968(stream, i, context):
    string = u')'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'='
def _r_string_4479814352(stream, i, context):
    string = u'='
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'@'
def _r_string_4479814480(stream, i, context):
    string = u'@'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\n'
def _r_string_4479814992(stream, i, context):
    string = '\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'"""'
def _r_string_4479815376(stream, i, context):
    string = u'"""'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'"""'
def _r_string_4479815632(stream, i, context):
    string = u'"""'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su':'
def _r_string_4479832336(stream, i, context):
    string = u':'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\n'
def _r_string_4479832528(stream, i, context):
    string = '\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su':'
def _r_string_4479832976(stream, i, context):
    string = u':'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'"""'
def _r_string_4479833552(stream, i, context):
    string = u'"""'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su':'
def _r_string_4479833616(stream, i, context):
    string = u':'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su':'
def _r_string_4479834000(stream, i, context):
    string = u':'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\n'
def _r_string_4479834192(stream, i, context):
    string = '\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\n'
def _r_string_4479835024(stream, i, context):
    string = '\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'#'
def _r_string_4479835216(stream, i, context):
    string = u'#'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'TIP'
def _r_string_4479835600(stream, i, context):
    string = u'TIP'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'WARNING'
def _r_string_4479835856(stream, i, context):
    string = u'WARNING'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'NOTE'
def _r_string_4479835920(stream, i, context):
    string = u'NOTE'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su':'
def _r_string_4479835984(stream, i, context):
    string = u':'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'>>'
def _r_string_4479858640(stream, i, context):
    string = u'>>'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'~~'
def _r_string_4479894416(stream, i, context):
    string = u'~~'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'=='
def _r_string_4479894480(stream, i, context):
    string = u'=='
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'{{{'
def _r_string_4479894672(stream, i, context):
    string = u'{{{'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'/>'
def _r_string_4481033552(stream, i, context):
    string = u'/>'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'>'
def _r_string_4481042448(stream, i, context):
    string = u'>'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'<'
def _r_string_4481042768(stream, i, context):
    string = u'<'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'</'
def _r_string_4481043792(stream, i, context):
    string = u'</'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su')'
def _r_string_4481043856(stream, i, context):
    string = u')'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'-'
def _r_string_4481291856(stream, i, context):
    string = u'-'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'<='
def _r_string_4481291920(stream, i, context):
    string = u'<='
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'<-'
def _r_string_4481292304(stream, i, context):
    string = u'<-'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'---'
def _r_string_4481292368(stream, i, context):
    string = u'---'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'->'
def _r_string_4481292560(stream, i, context):
    string = u'->'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'...'
def _r_string_4481292624(stream, i, context):
    string = u'...'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'<=>'
def _r_string_4481292816(stream, i, context):
    string = u'<=>'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'=>'
def _r_string_4481293008(stream, i, context):
    string = u'=>'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'nt'
def _r_string_4481293264(stream, i, context):
    string = u'nt'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'--'
def _r_string_4481293328(stream, i, context):
    string = u'--'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'LL'
def _r_string_4481293648(stream, i, context):
    string = u'LL'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'x'
def _r_string_4481293712(stream, i, context):
    string = u'x'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'NT'
def _r_string_4481293968(stream, i, context):
    string = u'NT'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'll'
def _r_string_4481294032(stream, i, context):
    string = u'll'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su' '
def _r_string_4481331856(stream, i, context):
    string = u' '
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'))'
def _r_string_4481332112(stream, i, context):
    string = u'))'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\n'
def _r_string_4481334224(stream, i, context):
    string = '\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su':'
def _r_string_4481334416(stream, i, context):
    string = u':'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\n'
def _r_string_4481334672(stream, i, context):
    string = '\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'||'
def _r_string_4481335056(stream, i, context):
    string = u'||'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'_'
def _r_string_4481355984(stream, i, context):
    string = u'_'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'`'
def _r_string_4481356176(stream, i, context):
    string = u'`'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'*'
def _r_string_4481356368(stream, i, context):
    string = u'*'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'"'
def _r_string_4481356624(stream, i, context):
    string = u'"'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'="'
def _r_string_4481356944(stream, i, context):
    string = u'="'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'_'
def _r_string_4481357392(stream, i, context):
    string = u'_'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'+('
def _r_string_4481357584(stream, i, context):
    string = u'+('
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su')'
def _r_string_4481357648(stream, i, context):
    string = u')'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'`'
def _r_string_4481357776(stream, i, context):
    string = u'`'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'_'
def _r_string_4481357840(stream, i, context):
    string = u'_'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'}'
def _r_string_4481358224(stream, i, context):
    string = u'}'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'`'
def _r_string_4481358928(stream, i, context):
    string = u'`'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'%{'
def _r_string_4481359056(stream, i, context):
    string = u'%{'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'*'
def _r_string_4481359248(stream, i, context):
    string = u'*'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'_'
def _r_string_4481359440(stream, i, context):
    string = u'_'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'-->'
def _r_string_4481384848(stream, i, context):
    string = u'-->'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'<!--'
def _r_string_4481385040(stream, i, context):
    string = u'<!--'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'(r)'
def _r_string_4481385168(stream, i, context):
    string = u'(r)'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'(c)'
def _r_string_4481385296(stream, i, context):
    string = u'(c)'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'(tm)'
def _r_string_4481385872(stream, i, context):
    string = u'(tm)'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'-->'
def _r_string_4481386000(stream, i, context):
    string = u'-->'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'//'
def _r_string_4481388112(stream, i, context):
    string = u'//'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'>'
def _r_string_4481388496(stream, i, context):
    string = u'>'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'__'
def _r_string_4481409232(stream, i, context):
    string = u'__'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'>>'
def _r_string_4481409488(stream, i, context):
    string = u'>>'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'__'
def _r_string_4481409552(stream, i, context):
    string = u'__'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'<'
def _r_string_4481409616(stream, i, context):
    string = u'<'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'*'
def _r_string_4481409744(stream, i, context):
    string = u'*'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'<<'
def _r_string_4481410192(stream, i, context):
    string = u'<<'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'>'
def _r_string_4481410320(stream, i, context):
    string = u'>'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'_'
def _r_string_4481410512(stream, i, context):
    string = u'_'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'__'
def _r_string_4481411600(stream, i, context):
    string = u'__'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'>>'
def _r_string_4481411856(stream, i, context):
    string = u'>>'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'_'
def _r_string_4481411920(stream, i, context):
    string = u'_'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'*'
def _r_string_4481412240(stream, i, context):
    string = u'*'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'_'
def _r_string_4481412368(stream, i, context):
    string = u'_'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'*'
def _r_string_4481412560(stream, i, context):
    string = u'*'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'#'
def _r_string_4481430160(stream, i, context):
    string = u'#'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'-'
def _r_string_4481430224(stream, i, context):
    string = u'-'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su';'
def _r_string_4481432400(stream, i, context):
    string = u';'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'&'
def _r_string_4481432784(stream, i, context):
    string = u'&'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su"'"
def _r_string_4481433296(stream, i, context):
    string = u"'"
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'|'
def _r_string_4481454224(stream, i, context):
    string = u'|'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'(('
def _r_string_4481454544(stream, i, context):
    string = u'(('
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'))'
def _r_string_4481455120(stream, i, context):
    string = u'))'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su']'
def _r_string_4481455376(stream, i, context):
    string = u']'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'+'
def _r_string_4481455440(stream, i, context):
    string = u'+'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'('
def _r_string_4481455504(stream, i, context):
    string = u'('
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'</'
def _r_string_4481456592(stream, i, context):
    string = u'</'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'['
def _r_string_4481456720(stream, i, context):
    string = u'['
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'|'
def _r_string_4481456848(stream, i, context):
    string = u'|'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su']'
def _r_string_4481457040(stream, i, context):
    string = u']'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'"'
def _r_string_4481457296(stream, i, context):
    string = u'"'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'<'
def _r_string_4481457552(stream, i, context):
    string = u'<'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'['
def _r_string_4481457808(stream, i, context):
    string = u'['
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'>'
def _r_string_4481458000(stream, i, context):
    string = u'>'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# Su'x'
def _r_string_4481495120(stream, i, context):
    string = u'x'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\r\n'
def _r_string_4481496592(stream, i, context):
    string = '\r\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# S'\n'
def _r_string_4481498256(stream, i, context):
    string = '\n'
    if stream.startswith(string, i, i + len(string)):
        return string, i + len(string)
    return Miss, i


# <((~Su')') Any)+>
def _r_take_4479786832(stream, i, context):
    _i = i
    out, i = _r_plus_4479812304(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# <@($lineend, None)>
def _r_take_4479834704(stream, i, context):
    _i = i
    out, i = _r_mixed_4479857808(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# <@(Ifrozenset([u':', u' ', '\n']), None)>
def _r_take_4479835536(stream, i, context):
    _i = i
    out, i = _r_mixed_4479857360(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# <@((Su')' | (fail $break_)), None)>
def _r_take_4481355856(stream, i, context):
    _i = i
    out, i = _r_mixed_4481359568(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# <((~Su'"') Any)*>
def _r_take_4481357712(stream, i, context):
    _i = i
    out, i = _r_star_4481040464(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# <$digit+>
def _r_take_4481431120(stream, i, context):
    _i = i
    out, i = _r_plus_4481431056(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# <R([A-Za-z_0-9]+)>
def _r_take_4481432912(stream, i, context):
    _i = i
    out, i = _r_regex_4481429840(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# <R([-A-Za-z_0-9]+)>
def _r_take_4481433424(stream, i, context):
    _i = i
    out, i = _r_regex_4481432208(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# <Ifrozenset([u'A', u'C', u'B', u'E', u'D', u'F', u'a', u'c', u'b', u'e', u'd', u'f', u'1', u'0', u'3', u'2', u'5', u'4', u'7', u'6', u'9', u'8'])+>
def _r_take_4481497040(stream, i, context):
    _i = i
    out, i = _r_plus_4481430480(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# $alphachar
def alphachar(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481496784, _r_if_4481495312, _r_do_4481496656):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $alphanum
def alphanum(stream, i, context):
    return r.AlphaNum._accept(stream, i)


# $anonlink
def anonlink(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481456720, targetre, _r_string_4481455376, _r_do_4481457232):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $apos
def apos(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_lookbehind_4481432656, _r_string_4481433296, _r_peek_4481432080, _r_do_4481430736):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $arrows
def arrows(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481432272, _r_or_4481293904, _r_do_4481433040):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $attr
def attr(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (ws, _r_bind_4481359120, _r_string_4481356944, _r_bind_4481359184, _r_string_4481356624, _r_do_4481358096):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $attrlist
def attrlist(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481356560, _r_do_4481040720):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $blocks
def blocks(stream, i, context):
    fm = blocks_fm
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


# $break_
def break_(stream, i, context):
    fm = break__fm
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


# $bullet
def bullet(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479712208, _r_bind_4479712720, _r_bind_4479712976, _r_do_4479733840):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $bullet_body
def bullet_body(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479712336, bullet_ending, _r_do_4479711952):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $bullet_ending
def bullet_ending(stream, i, context):
    fm = bullet_ending_fm
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


# $bullet_start
def bullet_start(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479709968, _r_bind_4479710480, _r_do_4479711056):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $chardec
def chardec(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481496976, _r_do_4481429968):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $charhex
def charhex(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481495120, _r_bind_4481497232, _r_do_4481495184):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $charnum
def charnum(stream, i, context):
    fm = charnum_fm
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


# $code
def code(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481358928, _r_bind_4481409872, _r_string_4481357776, _r_do_4481358608):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $codeblock
def codeblock(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479736336, _r_string_4479737040, _r_bind_4479735952, _r_bind_4479736592, _r_string_4479737488, _r_or_4479737744, _r_do_4479737104):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $comment
def comment(stream, i, context):
    fm = comment_fm
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


# $ctag
def ctag(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481043792, _r_bind_4481358032, _r_if_4481042128, _r_string_4481042448):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $dashes
def dashes(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_not_4481431568, _r_bind_4481429712, _r_not_4481431824, _r_do_4481430992):
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


# $divider
def divider(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479734736, _r_string_4479735504, _r_star_4479735120, lineend, _r_do_4479735760):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $elipsis
def elipsis(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481292624, _r_do_4481291344):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $em
def em(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (wordstart, _r_not_4481410064, _r_string_4481412368, _r_bind_4481409808, _r_string_4481355984, _r_peek_4481356048, wordend, _r_do_4481355920):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $emptylines
def emptylines(stream, i, context):
    target = _r_seq_4481498128
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


# $entity
def entity(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481432784, _r_bind_4481431248, _r_string_4481432400, _r_do_4481433360):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $env
def env(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481359056, _r_bind_4481410704, _r_string_4481358224, _r_do_4481358160):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $glyph
def glyph(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481357584, _r_bind_4481359824, _r_string_4481357648, _r_do_4481358352):
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
    for rule in (_r_bind_4479860560, ws, streamend, _r_do_4479860688):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $heading
def heading(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479785744, _r_bind_4479786384, _r_if_4479812560, _r_star_4479785488, _r_bind_4479811728, _r_star_4479812048, _r_bind_4479812688, _r_if_4479813136, _r_bind_4479812816, _r_star_4479813328, _r_or_4479814224, _r_do_4479813840):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $heading_tag
def heading_tag(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_star_4479786064, _r_string_4479786256, _r_bind_4479786576, _r_string_4479811792, _r_do_4479811664):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $hspace
def hspace(stream, i, context):
    __xs = u'\t '
    if i < len(stream) and stream[i] in __xs:
        return stream[i], i + 1
    else:
        return Miss, i


# $html_comment
def html_comment(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_string_4481385040, _r_mixed_4481386064, _r_string_4481384848, _r_do_4481387664):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $identifier
def identifier(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_peek_4481432976, _r_take_4481432912):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $indentchange
def indentchange(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_opt_4481498448, _r_bind_4481498832, _r_if_4481495632):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $indentdec
def indentdec(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_opt_4481496528, _r_bind_4481498320, _r_if_4481497360):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $indentinc
def indentinc(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_opt_4481498000, _r_bind_4481495824, _r_if_4481497424):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $inline
def inline(stream, i, context):
    fm = inline_fm
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


# $item
def item(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479833488, _r_bind_4479833936, _r_bind_4479834064, itemend, _r_do_4479834448):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $itemend
def itemend(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_opt_4479833104, _r_star_4479832144, break_):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $itemtype
def itemtype(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4479832336, _r_bind_4479815120, _r_string_4479832976, _r_do_4479832912):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $keyname
def keyname(stream, i, context):
    _i = i
    out, i = _r_plus_4481457744(stream, i, context)
    if out is Miss:
        return out, _i
    else:
        return stream[_i:i], i


# $keys
def keys(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481454544, _r_bind_4481457488, _r_bind_4481456656, _r_star_4481458128, _r_string_4481455120, _r_do_4481455248):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $line_comment
def line_comment(stream, i, context):
    out = Miss
    _i = i
    for rule in (linestart, _r_star_4481293456, _r_string_4481388112, _r_mixed_4481387088, lineend, _r_do_4481385552):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $lineend
def lineend(stream, i, context):
    if i >= len(stream):
        return Empty, i
    if stream.startswith("\n", i):
        return "\n", i + 1
    else:
        return Miss, i


# $linestart
def linestart(stream, i, context):
    if i < len(stream) and not stream.startswith(u'\uffff', i):
        if i == 0 or stream.startswith('\n', i - 1):
            return Empty, i
    return Miss, i


# $link
def link(stream, i, context):
    fm = link_fm
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


# $lstart
def lstart(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_opt_4481495952, linestart, _r_bind_4481495440, _r_do_4481497296):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $mult
def mult(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_lookbehind_4481293392, _r_string_4481293712, _r_peek_4481387728, _r_do_4481387280):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $named_entity
def named_entity(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481431312, _r_do_4481430928):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $note
def note(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479834576, _r_bind_4479832720, _r_string_4479834000, _r_bind_4479834896, _r_string_4479834192, _r_peek_4479835408, _r_do_4479835664):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $num_entity
def num_entity(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481430160, _r_bind_4481496720, _r_do_4481430864):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $ord
def ord(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479713104, _r_bind_4479734160, _r_bind_4479734480, _r_do_4479735312):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $ord_start
def ord_start(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479710992, _r_bind_4479710736, _r_do_4479711696):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $para
def para(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481334288, _r_bind_4479709456, _r_bind_4479709584, _r_do_4479710416):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $para_ending
def para_ending(stream, i, context):
    fm = para_ending_fm
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


# $property
def property(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479834640, _r_string_4479835216, _r_bind_4479833296, _r_string_4479835984, _r_star_4479835152, _r_bind_4479836048, lineend, _r_bind_4479836112, _r_opt_4479835280, _r_do_4479857296):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $pxml
def pxml(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479857040, _r_bind_4479857680, _r_bind_4479858320, _r_string_4479858640, _r_bind_4479856848, lineend, _r_do_4479859024):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $section
def section(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_opt_4479813776, linestart, _r_string_4479814480, _r_bind_4479814416, _r_star_4479814160, _r_bind_4479812752, _r_or_4479815504, _r_do_4479815440):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $sep
def sep(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479735824, _r_bind_4479736272, _r_bind_4479736144, sepend, _r_do_4479736528):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $sepend
def sepend(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_star_4479734288, lineend):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $space
def space(stream, i, context):
    __xs = u'\t \n\r'
    if i < len(stream) and stream[i] in __xs:
        return stream[i], i + 1
    else:
        return Miss, i


# $spaceorpunct
def spaceorpunct(stream, i, context):
    __xs = u' "\'\t\r\n-,/.;:?'
    if i < len(stream) and stream[i] in __xs:
        return stream[i], i + 1
    else:
        return Miss, i


# $spans
def spans(stream, i, context):
    fm = spans_fm
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


# $starters
def starters(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (linestart, _r_star_4479860304, _r_or_4479859920):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $streamend
def streamend(stream, i, context):
    return r.StreamEnd._accept(stream, i)


# $streamstart
def streamstart(stream, i, context):
    return (Empty if i == 0 else Miss), i


# $strong
def strong(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (wordstart, _r_not_4481412496, _r_string_4481412240, _r_bind_4481410768, _r_string_4481412560, wordend, _r_peek_4481412112, _r_do_4481412048):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $stylespans
def stylespans(stream, i, context):
    fm = stylespans_fm
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


# $subtitle
def subtitle(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4479783696, _r_star_4479737808, _r_bind_4479736912, _r_do_4479784144):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $summary
def summary(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479814672, _r_string_4479815376, _r_bind_4479814608, _r_string_4479815632, _r_star_4479811856, break_, _r_do_4479833040):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $supertitle
def supertitle(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479736976, _r_star_4479737360, _r_string_4479783504, _r_do_4479783184):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $symbols
def symbols(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4481431504, _r_peek_4481293072, _r_do_4481291728):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $targetre
def targetre(stream, i, context):
    __m = targetre_re.match(stream, i)
    if __m:
        context.update(__m.groupdict())
        return __m.group(0), __m.end()
    return Miss, i


# $textlink
def textlink(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_string_4481457808, _r_bind_4481456016, _r_string_4481456848, targetre, _r_string_4481457040, _r_do_4481331408):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $title
def title(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_bind_4479784272, _r_string_4479784592, _r_star_4479783376, _r_bind_4479784208, _r_bind_4479783632, _r_bind_4479784016, _r_star_4479784784, _r_string_4479785936, _r_star_4479785424, _r_or_4479786128, _r_do_4479786192):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $typog
def typog(stream, i, context):
    fm = typog_fm
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


# $ui
def ui(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (wordstart, _r_not_4481413072, _r_string_4481409232, _r_bind_4481387792, _r_string_4481409552, wordend, _r_peek_4481409104, _r_do_4481411664):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $uisep
def uisep(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_plus_4481387920, _r_string_4481388496, _r_plus_4481387472, _r_do_4481388048):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# $var
def var(stream, i, context):
    context = context.push()

    out = Miss
    _i = i
    for rule in (_r_not_4481410128, _r_string_4481410192, _r_bind_4481384720, _r_string_4481411856, _r_peek_4481412752, _r_do_4481410832):
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


# $wordend
def wordend(stream, i, context):
    fm = wordend_fm
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


# $wordstart
def wordstart(stream, i, context):
    fm = wordstart_fm
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
    target = _r_or_4481498064
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


# $xchar
def xchar(stream, i, context):
    __xs = u'1032547698ACBEDGFIHKJMLONQPSRUTWVYXZ_acbedgfihkjmlonqpsrutwvyxz'
    if i < len(stream) and stream[i] in __xs:
        return stream[i], i + 1
    else:
        return Miss, i


# $xml
def xml(stream, i, context):
    fm = xml_fm
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


# $xname
def xname(stream, i, context):
    out = Miss
    _i = i
    for rule in (_r_peek_4481431952, _r_take_4481433424):
        out, newi = rule(stream, i, context)
        if out is Miss:
            break
        i = newi
    return out, (_i if out is Miss else i)


# 606 functions


_r_do_4479709264_code = r.compile_expr(u'("cell", "td")')
_r_do_4479709392_code = r.compile_expr(u'("cell", "th")')
_r_do_4479710096_code = r.compile_expr(u'("para", None)')
_r_do_4479710416_code = r.compile_expr(u'w.block(nd[0], indent, tx, role=nd[1])')
_r_do_4479711056_code = r.compile_expr(u'len(bs) + len(space)')
_r_do_4479711696_code = r.compile_expr(u'len(ns) + len(space)')
_r_do_4479711952_code = r.compile_expr(u'tx')
_r_do_4479733840_code = r.compile_expr(u"w.block('bullet', indent, tx, blevel=indent+bwidth)")
_r_do_4479735312_code = r.compile_expr(u"w.block('ord', indent, tx, blevel=indent+bwidth)")
_r_do_4479735760_code = r.compile_expr(u'w.block("divider", indent, None)')
_r_do_4479736528_code = r.compile_expr(u'w.block("sep", indent, tx, level=len(line))')
_r_do_4479737104_code = r.compile_expr(u'w.block("pre", indent, tx, lang=lang)')
_r_do_4479783184_code = r.compile_expr(u'w.span("supertitle", tx)')
_r_do_4479783440_code = r.compile_expr(u'None')
_r_do_4479784144_code = r.compile_expr(u'w.span("subtitle", tx)')
_r_do_4479786192_code = r.compile_expr(u'w.block("title", indent, supt + tx + subt, level=0)')
_r_do_4479811664_code = r.compile_expr(u'tag')
_r_do_4479813840_code = r.compile_expr(u'w.block("h", indent, tx, level=len(eqs), id=tag[0] if tag else None, container=True)')
_r_do_4479815440_code = r.compile_expr(u'w.block(n + "_section", 0, tx, level=1, role="section", id=n, container=True)')
_r_do_4479832912_code = r.compile_expr(u'n[0] if n else None')
_r_do_4479833040_code = r.compile_expr(u'w.block("summary", indent, tx)')
_r_do_4479834448_code = r.compile_expr(u'w.block(it or "item", indent, tx, role="item")')
_r_do_4479835664_code = r.compile_expr(u'w.block(it.lower(), indent, tx, role="item")')
_r_do_4479857296_code = r.compile_expr(u'w.block("prop", indent, None, name=k, value=v + "".join(extras))')
_r_do_4479858576_code = r.compile_expr(u'line')
_r_do_4479859024_code = r.compile_expr(u'w.block("pxml", indent, tx, tag=n, attrs=alist)')
_r_do_4479860688_code = r.compile_expr(u'b')
_r_do_4481034256_code = r.compile_expr(u'w.span("xml", \'\', tag=n, attrs=alist)')
_r_do_4481040720_code = r.compile_expr(u'dict(attrs)')
_r_do_4481290320_code = r.compile_expr(u'compat.unichr(8804)')
_r_do_4481290512_code = r.compile_expr(u'compat.unichr(8805)')
_r_do_4481291344_code = r.compile_expr(u'compat.unichr(8230)')
_r_do_4481291600_code = r.compile_expr(u'compat.unichr(8594)')
_r_do_4481291728_code = r.compile_expr(u'c')
_r_do_4481293200_code = r.compile_expr(u'compat.unichr(8660)')
_r_do_4481293520_code = r.compile_expr(u'compat.unichr(8592)')
_r_do_4481331408_code = r.compile_expr(u'w.span("link", tx, scheme=name, value=value)')
_r_do_4481334800_code = r.compile_expr(u'("dt", None)')
_r_do_4481355920_code = r.compile_expr(u'w.span("em", tx)')
_r_do_4481358096_code = r.compile_expr(u'(k, v)')
_r_do_4481358160_code = r.compile_expr(u'w.span("env", [], name=n)')
_r_do_4481358352_code = r.compile_expr(u'w.span("link", None, scheme="Glyph", value=v)')
_r_do_4481358608_code = r.compile_expr(u'w.span("code", tx)')
_r_do_4481385552_code = r.compile_expr(u"''")
_r_do_4481386832_code = r.compile_expr(u'compat.unichr(174)')
_r_do_4481387280_code = r.compile_expr(u'compat.unichr(215)')
_r_do_4481387344_code = r.compile_expr(u'compat.unichr(8482)')
_r_do_4481387600_code = r.compile_expr(u'compat.unichr(169)')
_r_do_4481387664_code = r.compile_expr(u"''")
_r_do_4481388048_code = r.compile_expr(u'" " + compat.unichr(9656) + " "')
_r_do_4481410832_code = r.compile_expr(u'w.span("var", tx)')
_r_do_4481411664_code = r.compile_expr(u'w.span("ui", tx)')
_r_do_4481412048_code = r.compile_expr(u'w.span("strong", tx)')
_r_do_4481429968_code = r.compile_expr(u'int(d)')
_r_do_4481430736_code = r.compile_expr(u'compat.unichr(8217)')
_r_do_4481430864_code = r.compile_expr(u'compat.unichr(num)')
_r_do_4481430928_code = r.compile_expr(u'util.decode_named_entity(n)')
_r_do_4481430992_code = r.compile_expr(u'compat.unichr(8212) if len(d) == 3 else compat.unichr(8211)')
_r_do_4481433040_code = r.compile_expr(u"' ' + c")
_r_do_4481433360_code = r.compile_expr(u'char')
_r_do_4481455248_code = r.compile_expr(u'w.span("keys", None, keys=[k] + kk)')
_r_do_4481456400_code = r.compile_expr(u'w.span("xml", tx, tag=n, attrs=alist)')
_r_do_4481457232_code = r.compile_expr(u'w.span("link", \'\', scheme=name, value=value)')
_r_do_4481495184_code = r.compile_expr(u'int(h, 16)')
_r_do_4481496656_code = r.compile_expr(u'c')
_r_do_4481497296_code = r.compile_expr(u'len(indent)')
_r_if_4479734864_code = r.compile_expr(u'nextin < indent or nextin > indent + bwidth')
_r_if_4479812560_code = r.compile_expr(u'len(eqs) > 1')
_r_if_4479813136_code = r.compile_expr(u'eqs == eqs2')
_r_if_4479857872_code = r.compile_expr(u'line.strip()')
_r_if_4479859728_code = r.compile_expr(u'nextin > indent')
_r_if_4481042128_code = r.compile_expr(u'n == name')
_r_if_4481495312_code = r.compile_expr(u'c.isalpha()')
_r_if_4481495632_code = r.compile_expr(u'nextin != indent')
_r_if_4481497360_code = r.compile_expr(u'nextin < indent')
_r_if_4481497424_code = r.compile_expr(u'nextin > indent')
_r_or_4479712464_fm = {
    None: [(_r_seq_4479734096, False)],
    '\t': [(emptylines, False), (_r_seq_4479734096, False)],
    '\n': [(emptylines, False), (_r_seq_4479734096, False)],
    u' ': [(emptylines, False), (_r_seq_4479734096, False)],
}
_r_or_4479737168_fm = {
    None: [(_r_do_4479783440, False)],
    '\t': [(_r_seq_4479737296, False), (_r_do_4479783440, False)],
    '\n': [(_r_seq_4479737296, False), (_r_do_4479783440, False)],
    '\r': [(_r_seq_4479737296, False), (_r_do_4479783440, False)],
    u' ': [(_r_seq_4479737296, False), (_r_do_4479783440, False)],
    u'#': [(_r_seq_4479737296, False), (_r_do_4479783440, False)],
}
_r_or_4479737744_fm = {
    None: [],
    '\n': [(lineend, False)],
    '\\': [(lineend, False)],
    'f': [(lineend, False), (lineend, False), (lineend, False), (lineend, False)],
    'u': [(lineend, False)],
    u'\uffff': [(streamend, False)],
}
_r_or_4479785680_fm = {
    None: [],
    '\t': [(_r_seq_4479785872, False)],
    u' ': [(_r_seq_4479785872, False)],
    u'<': [(_r_string_4479786960, False)],
    u'=': [(_r_seq_4479785872, False)],
}
_r_or_4479786128_fm = {
    None: [],
    '\n': [(_r_string_4479812112, False)],
    u'\uffff': [(streamend, False)],
}
_r_or_4479814224_fm = {
    None: [],
    '\n': [(_r_string_4479814992, False)],
    u'\uffff': [(streamend, False)],
}
_r_or_4479815504_fm = {
    None: [],
    '\n': [(_r_string_4479832528, False)],
    u'\uffff': [(streamend, False)],
}
_r_or_4479832400_fm = {
    None: [],
    u'\n': [(break_, True)],
    u'"': [(_r_string_4479833552, False)],
    u'\uffff': [(break_, True)],
}
_r_or_4479834960_fm = {
    None: [],
    u'N': [(_r_string_4479835920, False)],
    u'T': [(_r_string_4479835600, False)],
    u'W': [(_r_string_4479835856, False)],
}
_r_or_4479859920_fm = {
    None: [],
    u'#': [(ord_start, True)],
    u'*': [(bullet_start, True)],
    u'-': [(bullet_start, True)],
    u':': [(itemtype, True)],
    u'=': [(_r_string_4479894480, False)],
    u'{': [(_r_string_4479894672, False)],
    u'~': [(_r_string_4479894416, False)],
}
_r_or_4481043344_fm = {
    None: [],
    u'\n': [(_r_failif_4481043472, True)],
    u')': [(_r_string_4481043856, False)],
    u'\uffff': [(_r_failif_4481043472, True)],
}
_r_or_4481292240_fm = {
    None: [],
    u'(': [(_r_seq_4481291408, False), (_r_seq_4481292944, False), (_r_seq_4481292688, False)],
}
_r_or_4481293904_fm = {
    None: [],
    '\t': [(_r_peek_4481386384, False)],
    '\n': [(lineend, False), (_r_peek_4481386384, False)],
    '\r': [(_r_peek_4481386384, False)],
    u' ': [(_r_peek_4481386384, False)],
    '\\': [(lineend, False)],
    'f': [(lineend, False), (lineend, False), (lineend, False), (lineend, False)],
    'u': [(lineend, False)],
}
_r_or_4481357264_fm = {
    None: [],
    u'\n': [(_r_failif_4481356880, True)],
    u'`': [(_r_string_4481356176, False)],
    u'\uffff': [(_r_failif_4481356880, True)],
}
_r_or_4481359312_fm = {
    None: [],
    u'\n': [(_r_failif_4481357136, True)],
    u'_': [(_r_string_4481357840, False)],
    u'\uffff': [(_r_failif_4481357136, True)],
}
_r_or_4481386768_fm = {
    None: [],
    '\t': [(hspace, False)],
    u' ': [(hspace, False)],
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
    u'\uffff': [(streamend, False)],
}
_r_or_4481410448_fm = {
    None: [],
    '\t': [(uisep, False), (inline, True)],
    '\n': [(uisep, False), (inline, True)],
    '\r': [(uisep, False)],
    u' ': [(uisep, False), (inline, True)],
    u'%': [(inline, True)],
    u'&': [(inline, True)],
    u"'": [(inline, True)],
    u'(': [(inline, True)],
    u'*': [(inline, True)],
    u'+': [(inline, True)],
    u'-': [(inline, True)],
    u'.': [(inline, True)],
    u'/': [(inline, True)],
    u'<': [(inline, True)],
    u'=': [(inline, True)],
    u'[': [(inline, True)],
    u'_': [(inline, True)],
    u'`': [(inline, True)],
    u'x': [(inline, True)],
    u'\uffff': [(inline, True)],
}
_r_or_4481411152_fm = {
    None: [],
    u'\n': [(_r_failif_4481410640, True)],
    u'_': [(_r_string_4481411600, False)],
    u'\uffff': [(_r_failif_4481410640, True)],
}
_r_or_4481411728_fm = {
    None: [],
    u'\n': [(_r_failif_4481409296, True)],
    u'>': [(_r_string_4481409488, False)],
    u'\uffff': [(_r_failif_4481409296, True)],
}
_r_or_4481413008_fm = {
    None: [],
    u'\n': [(_r_failif_4481356688, True)],
    u'*': [(_r_string_4481356368, False)],
    u'\uffff': [(_r_failif_4481356688, True)],
}
_r_or_4481429584_fm = {
    None: [],
    u'-': [(_r_seq_4481292048, False)],
    u'<': [(_r_seq_4481429904, False), (_r_seq_4481294096, False), (_r_seq_4481293584, False)],
    u'=': [(_r_seq_4481293776, False)],
}
_r_or_4481429776_fm = {
    None: [],
    u'-': [(_r_string_4481292368, False), (_r_string_4481293328, False)],
}
_r_or_4481430544_fm = {
    None: [],
    u'L': [(_r_string_4481293648, False)],
    u'N': [(_r_string_4481293968, False)],
    u'S': [(_r_in_4481431760, False)],
    u'T': [(_r_in_4481431760, False)],
    u'l': [(_r_string_4481294032, False)],
    u'n': [(_r_string_4481293264, False)],
    u's': [(_r_in_4481431760, False)],
    u't': [(_r_in_4481431760, False)],
}
_r_or_4481432848_fm = {
    None: [(named_entity, True)],
    u'#': [(num_entity, True), (named_entity, True)],
}
_r_or_4481454800_fm = {
    None: [(_r_seq_4481457616, False)],
    '\t': [(_r_seq_4481457424, False), (_r_seq_4481457616, False)],
    u' ': [(_r_seq_4481457424, False), (_r_seq_4481457616, False)],
}
_r_or_4481457104_fm = {
    None: [],
    u' ': [(_r_string_4481331856, False)],
    u')': [(_r_string_4481332112, False)],
}
_r_or_4481498064_fm = {
    None: [],
    '\t': [(hspace, False)],
    '\n': [(vspace, False)],
    '\r': [(vspace, False)],
    u' ': [(hspace, False)],
}
_r_regex_4479857936_re = re.compile(u'.*$', re.UNICODE | re.MULTILINE)
_r_regex_4481429840_re = re.compile(u'[A-Za-z_0-9]+', re.UNICODE | re.MULTILINE)
_r_regex_4481431184_re = re.compile(u'[A-Za-z]+', re.UNICODE | re.MULTILINE)
_r_regex_4481432208_re = re.compile(u'[-A-Za-z_0-9]+', re.UNICODE | re.MULTILINE)
blocks_fm = {
    None: [(codeblock, True), (title, True), (heading, True), (summary, True), (divider, True), (sep, True), (bullet, True), (ord, True), (item, True), (note, True), (property, True), (pxml, True), (para, True)],
    '\t': [(section, True), (codeblock, True), (title, True), (heading, True), (summary, True), (divider, True), (sep, True), (bullet, True), (ord, True), (item, True), (note, True), (property, True), (pxml, True), (para, True)],
    '\n': [(section, True), (codeblock, True), (title, True), (heading, True), (summary, True), (divider, True), (sep, True), (bullet, True), (ord, True), (item, True), (note, True), (property, True), (pxml, True), (para, True)],
    u' ': [(section, True), (codeblock, True), (title, True), (heading, True), (summary, True), (divider, True), (sep, True), (bullet, True), (ord, True), (item, True), (note, True), (property, True), (pxml, True), (para, True)],
    u'@': [(section, True), (codeblock, True), (title, True), (heading, True), (summary, True), (divider, True), (sep, True), (bullet, True), (ord, True), (item, True), (note, True), (property, True), (pxml, True), (para, True)],
}
break__fm = {
    None: [],
    u'\n': [(_r_blockbreak_4470302032, False), (_r_seq_4481456080, True)],
    u'\uffff': [(_r_blockbreak_4470302032, False)],
}
bullet_ending_fm = {
    None: [],
    '\n': [(_r_seq_4481332560, False), (_r_seq_4479709712, True), (_r_seq_4479710672, True)],
    u'\uffff': [(streamend, False)],
}
charnum_fm = {
    None: [],
    u'0': [(chardec, True)],
    u'1': [(chardec, True)],
    u'2': [(chardec, True)],
    u'3': [(chardec, True)],
    u'4': [(chardec, True)],
    u'5': [(chardec, True)],
    u'6': [(chardec, True)],
    u'7': [(chardec, True)],
    u'8': [(chardec, True)],
    u'9': [(chardec, True)],
    u'x': [(charhex, True)],
}
comment_fm = {
    None: [],
    '\t': [(line_comment, False)],
    u' ': [(line_comment, False)],
    u'/': [(line_comment, False)],
    u'<': [(html_comment, False)],
}
inline_fm = {
    None: [],
    '\t': [(spans, True)],
    u'\n': [(_r_failif_4481333264, True)],
    u' ': [(spans, True)],
    u'%': [(spans, True)],
    u'&': [(spans, True)],
    u"'": [(spans, True)],
    u'(': [(spans, True)],
    u'*': [(spans, True)],
    u'+': [(spans, True)],
    u'-': [(spans, True)],
    u'.': [(spans, True)],
    u'/': [(spans, True)],
    u'<': [(spans, True)],
    u'=': [(spans, True)],
    u'[': [(spans, True)],
    u'_': [(spans, True)],
    u'`': [(spans, True)],
    u'x': [(spans, True)],
    u'\uffff': [(_r_failif_4481333264, True)],
}
link_fm = {
    None: [],
    u'[': [(anonlink, False), (textlink, True)],
}
para_ending_fm = {
    None: [],
    u'\n': [(_r_seq_4481331792, True)],
    u':': [(_r_seq_4481456272, True)],
    u'|': [(_r_seq_4481331280, False), (_r_seq_4481332240, True)],
    u'\uffff': [(_r_seq_4481331792, True)],
}
spans_fm = {
    None: [],
    '\t': [(comment, False)],
    u' ': [(comment, False)],
    u'%': [(env, True)],
    u'&': [(entity, True)],
    u"'": [(typog, True)],
    u'(': [(keys, True), (typog, True)],
    u'*': [(strong, True)],
    u'+': [(glyph, True)],
    u'-': [(typog, True)],
    u'.': [(typog, True)],
    u'/': [(comment, False)],
    u'<': [(comment, False), (xml, True), (var, True), (typog, True)],
    u'=': [(typog, True)],
    u'[': [(link, True)],
    u'_': [(ui, True), (em, True)],
    u'`': [(code, True)],
    u'x': [(typog, True)],
}
stylespans_fm = {
    None: [],
    '\t': [(comment, False)],
    u'\n': [(_r_failif_4481332304, True)],
    u' ': [(comment, False)],
    u'%': [(env, True)],
    u'&': [(entity, True)],
    u"'": [(typog, True)],
    u'(': [(typog, True)],
    u'+': [(glyph, True)],
    u'-': [(typog, True)],
    u'.': [(typog, True)],
    u'/': [(comment, False)],
    u'<': [(comment, False), (xml, True), (var, True), (typog, True)],
    u'=': [(typog, True)],
    u'_': [(em, True)],
    u'`': [(code, True)],
    u'x': [(typog, True)],
    u'\uffff': [(_r_failif_4481332304, True)],
}
targetre_re = re.compile(u'((?P<name>[A-Z][-_.A-Za-z0-9]*):)?(?P<value>[^\\]\\n|]*)', re.UNICODE | re.MULTILINE)
typog_fm = {
    None: [],
    u"'": [(apos, True)],
    u'(': [(symbols, True)],
    u'-': [(dashes, True), (arrows, True)],
    u'.': [(elipsis, False)],
    u'<': [(arrows, True)],
    u'=': [(arrows, True)],
    u'x': [(mult, False)],
}
vspace_fm = {
    None: [],
    '\n': [(_r_in_4475775184, False)],
    '\r': [(_r_string_4481496592, False), (_r_in_4475775184, False)],
}
wordend_fm = {
    None: [(_r_peek_4481388368, False)],
    u'\uffff': [(streamend, False), (_r_peek_4481388368, False)],
}
wordstart_fm = {
    None: [(streamstart, False), (_r_not_4481386192, False)],
}
xml_fm = {
    None: [],
    u'<': [(_r_seq_4481358288, True), (_r_seq_4481357968, True)],
}
