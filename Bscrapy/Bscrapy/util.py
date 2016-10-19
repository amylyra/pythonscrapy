import bleach
#import re


def strip_html(html_str):
    """remove all HTML markup using the Bleach lib"""
    return bleach.clean(html_str, tags=[], attributes={},
                        styles=[], strip=True)


def decoding(l):
    return [il.decode() for il in l]


def trim_whitespace(trs):
    return [ls.replace('\n', '').replace('\t', '').strip()
            for ls in trs]
