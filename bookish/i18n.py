# Copyright 2014 Matt Chaput. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
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


import locale
import re


def normalize_language_name(language):
    """
    Attempts to normalize language names (e.g. ``en_us``, ``en-US``, etc.) to a
    lowercase, hyphenated form (``en-us``).
    """

    return language.replace("-", "_").lower()


# From django.utils.translation.trans_real.parse_accept_lang_header
accept_language_re = re.compile(r"""
([A-Za-z]{1,8}(?:-[A-Za-z]{1,8})*|\*)         # "en", "en-au", "x-y-z", "*"
(?:\s*;\s*q=(0(?:\.\d{,3})?|1(?:.0{,3})?))?   # Optional "q=1.00", "q=0.8"
(?:\s*,\s*|$)                                 # Multiple accepts per header.
""", re.VERBOSE)


def parse_accept_lang_header(lang_string):
    """
    Parses the lang_string, which is the body of an HTTP Accept-Language
    header, and returns a list of (lang, q-value), ordered by 'q' values.

    Any format errors in lang_string results in an empty list being returned.
    """

    result = []
    pieces = accept_language_re.split(lang_string)
    if pieces[-1]:
        return []

    for i in range(0, len(pieces) - 1, 3):
        first, lang, priority = pieces[i: i + 3]
        if first:
            return []
        priority = priority and float(priority) or 1.0
        result.append((lang, priority))

    return [lang for lang, pri in sorted(result, key=lambda k: 0 - k[1])]


def is_language_supported(language, supported_languages):
    if not language:
        return None
    normalized = normalize_language(language)
    if not normalized:
        return None

    # Remove the default encoding from locale_alias.
    normalized = normalized.split('.')[0]
    for lang in (normalized, normalized.split('_')[0]):
        if lang.lower() in supported_languages:
            return lang
    return None


def parse_http_accept_language(header_string, available_langs):
    for accept_lang in parse_accept_lang_header(header_string):
        if accept_lang == '*':
            break

        # 'normalized' is the root name of the locale in POSIX format (which is
        # the format used for the directories holding the MO files).
        normalized = locale.locale_alias.get(to_locale(accept_lang, True))
        if not normalized:
            continue

        # Remove the default encoding from locale_alias.
        normalized = normalized.split('.')[0]

        for lang_code in (accept_lang, accept_lang.split('-')[0]):
            lang_code = lang_code.lower()
            if lang_code in available_langs:
                return lang_code
    return None


def language_detection():
    """Select the right language

        1. CookieLanguageMiddleware : Look at the cookie if exists
        2. HttpAcceptLanguageMiddleware : Look at the browser language settings
        3. DefaultLanguageMiddleware : Come back to english

    """
    lang = None

    # Cookie
    if lang is None:
        lang_code = request.cookies.get('django_language', None)
        lang = is_language_supported(lang_code)

    # HttpAcceptLanguageMiddleware
    if lang is None:
        lang = parse_http_accept_language(request.headers.get('Accept-Language', ''))

    # DefaultLanguageMiddleware
    if lang is None:
        lang = 'en'

    return redirect('http://%s.%s/' % (lang, DOMAIN_NAME))
