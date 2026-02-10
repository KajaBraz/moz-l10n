from unittest import TestCase

from moz.l10n.formats import Format
from moz.l10n.message import parse_message, get_string_word_count, get_word_count


class TestMessageWordCount(TestCase):
    def testPatternMessage(self):
        assert get_word_count(parse_message(Format.fluent,
                                            '{ -brand-short-name } został opracowany przez <label data-l10n-name="community-mozillaLink">{ -vendor-short-name(case: "acc") }</label>, która jest <label data-l10n-name="community-creditsLink">globalną społecznością</label>, starającą się zapewnić, by Internet pozostał otwarty, publiczny i dostępny dla wszystkich.')) == 35
        assert get_word_count(parse_message(Format.fluent, "{ -brand-short-name } 正在播放媒体")) == 5
        assert get_word_count(parse_message(Format.fluent, "{ $version } ({ $bits }-bit)")) == 3
        assert get_word_count(parse_message(Format.fluent, "{ $version } ({ $isodate }) ({ $bits }-bit)")) == 4
        assert get_word_count(parse_message(Format.fluent,
                                            'Create or sign in to your { -fxaccount-brand-name(capitalization: "sentence") } on the device where your logins are saved.community-2 = abc { -brand-short-name } został opracowany przez <label data-l10n-name="community-mozillaLink">{ -vendor-short-name(case: "acc") }</label>, która jest <label data-l10n-name="community-creditsLink">globalną społecznością</label>, starającą się zapewnić, by Internet pozostał otwarty, publiczny i dostępny dla wszystkich.')) == 53
        assert get_word_count(parse_message(Format.fluent,
                                            'This breach occurred on { DATETIME($date, day: "numeric", month: "long", year: "numeric") }')) == 5

    def testSelectMessage(self):
        msgs = [
            """{ $total ->
                [one] { $count } of { $total } login
               *[other] { $count } of { $total } logins
            }""",
            """{ $total ->
                [zero] { $count } من أصل { $total } كلمات السر
                [one] كلمة واحدة من أصل { $total } كلمات السر
                [two] كلمتان من أصل { $total } كلمات السر
                [few] { $count } من أصل { $total } كلمات السر
                [many] { $count } من أصل { $total } كلمة السر
               *[other] { $count } من أصل { $total } كلمة السر
           }""",
            """{ PLATFORM() ->
                [windows] To select a different search engine go to <a data-l10n-name="link-options">Options</a>
               *[other] To select a different search engine go to <a data-l10n-name="link-options">Preferences</a>
            }"""]
        assert get_word_count(parse_message(Format.fluent, msgs[0])) == 4
        assert get_word_count(parse_message(Format.fluent, msgs[1])) == 6
        assert get_word_count(parse_message(Format.fluent, msgs[2])) == 16

    def test_raw_strings(self):
        assert get_string_word_count("") == 0
        assert get_string_word_count("a,b,c,d") == 4
        assert get_string_word_count("Multilingual word counter.") == 3
        assert get_string_word_count("it works great, isn't it? Just try it: (123), 123, 123%, ...") == 12
        assert get_string_word_count("up-to-date") == 3
        assert get_string_word_count("Name:\n{username}") == 2
        assert get_string_word_count("Username (A-Z)") == 3
        assert get_string_word_count("Add “%1$S” as an application for %2$S links?") == 10
        assert get_string_word_count("eccolo, perché, è") == 3
        assert get_string_word_count("Espace fine insécable : Fin") == 4
        assert get_string_word_count("多语言单词计数器，尝试中文。") == 7
        assert get_string_word_count("多語言單字計數器，嘗試中文。") == 7
        assert get_string_word_count("多言語ワードカウンター、日本語に挑戦。") == 10
        assert get_string_word_count("다국어 단어 카운터, 한국어를 시도해 보세요.") == 6
        assert get_string_word_count("عداد الكلمات متعدد اللغات، جرب اللغة العربية.") == 7
        assert get_string_word_count("Mozilla 浏览器的用户。") == 5
        assert get_string_word_count("Mozilla ブラウザのユーザー。") == 6
        assert get_string_word_count("Mozilla 123 ブラウザのユーザー。") == 7
        assert get_string_word_count(":) 🙂 , _ - * & $ % @ ! ... …") == 0
