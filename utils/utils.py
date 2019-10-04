import unicodedata

import config as cf


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def is_mark_known(token_id: str) -> bool:
    for mark in cf.PUNCTUATION_MARKS:
        if token_id == mark:
            if cf.random.random() < cf.SIGN_HIDING_PROBABILITY:
                return True
            else:
                return False
    return True