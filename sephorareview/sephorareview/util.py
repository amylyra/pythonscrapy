import bleach
#import re


def strip_html(html_str):
    """remove all HTML markup using the Bleach lib"""
    return bleach.clean(html_str, tags=[], attributes={},
                        styles=[], strip=True)


def trim_whitespace(str):
    return str.strip()
