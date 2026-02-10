from typing import Tuple

from moz.l10n.model import Message, PatternMessage, SelectMessage, Pattern


def get_word_count(msg: Message) -> int:
    """
    Estimate the number of words in a message.
    In case of PatternMessage, assume that the non-string pattern elements (Expression and Markup) count as one word
    and return the number of words in string patterns.
    In case of SelectMessage, apply the pattern logic and return the average word count of its variants.
    """
    if type(msg) == PatternMessage:
        return _estimate_pattern_word_count(msg.pattern)
    elif type(msg) == SelectMessage:
        cnt = sum(_estimate_pattern_word_count(v) for v in msg.variants.values())
        return round(cnt / len(msg.variants))
    raise ValueError("Unsupported message type")


def get_string_word_count(s: str) -> int:
    """
    Get number of words in a plain string.
    Omit any non-alphanumeric characters.
    Consider agglutinated form words and closed compound words as one word.
    Handle multilingual (diverse alphabetic) text.
    """
    cnt = 0
    word_started = False
    for ch in s:
        is_zh_ja, mult = _get_char_multiplier(ch)
        if is_zh_ja:
            if word_started:
                cnt += 1
                word_started = False
            cnt += mult
        elif ch.isalnum():
            word_started = True
        elif word_started:
            cnt += 1
            word_started = False
    if word_started:
        cnt += 1
    return round(cnt)


def _estimate_pattern_word_count(pattern: Pattern) -> int:
    """
    Calculate the estimated number of words in a pattern.
    """
    return sum(get_string_word_count(el) if type(el) == str else 1 for el in pattern)


def _get_char_multiplier(ch: str) -> Tuple[bool, float]:
    """
    Check if a character is from Chinese or Japanese alphabet.
    If so, apply coefficient of 0.6 to account for the words spanning across multiple characters.
    """
    ch_code = ord(ch)
    if (19968 <= ch_code <= 40959) or (12352 <= ch_code <= 12543):
        return True, 0.6
    return False, 1
