import unicodedata

import config as cf


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def is_punctuation_token(token: str) -> bool:
    for mark in cf.PUNCTUATION_TOKEN:
        if token == mark:
            return True
    return False

def is_masked_token(token: str) -> bool:
    for mark in cf.MASKED_TOKEN:
        if token == mark:
            return True
    return False