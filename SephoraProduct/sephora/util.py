import bleach
#import re


def strip_html(html_str):
    """remove all HTML markup using the Bleach lib"""
    return bleach.clean(html_str, tags=[], attributes={},
                        styles=[], strip=True)


def decoding(l):
    return l.decode()


def trim_whitespace(trs):
    if not trs:
        return None
    return trs.replace('\n', '').replace('\t', '').replace('\r', '').strip()
