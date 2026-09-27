import re
import unittest

from django.test import SimpleTestCase
from django.utils import regex_helper
from django.utils.regex_helper import has_named_group


class NormalizeTests(unittest.TestCase):
    def test_empty(self):
        pattern = r""
        expected = [("", [])]
        result = regex_helper.normalize(pattern)
        self.assertEqual(result, expected)

    def test_escape(self):
        pattern = r"\\\^\$\.\|\?\*\+\(\)\["
        expected = [("\\^$.|?*+()[", [])]
        result = regex_helper.normalize(pattern)
        self.assertEqual(result, expected)

    def test_group_positional(self):
        pattern = r"(.*)-(.+)"
        expected = [("%(_0)s-%(_1)s", ["_0", "_1"])]
        result = regex_helper.normalize(pattern)
        self.assertEqual(result, expected)

    def test_group_noncapturing(self):
        pattern = r"(?:non-capturing)"
        expected = [("non-capturing", [])]
        result = regex_helper.normalize(pattern)
        self.assertEqual(result, expected)

    def test_group_named(self):
        pattern = r"(?P<first_group_name>.*)-(?P<second_group_name>.*)"
        expected = [
            (
                "%(first_group_name)s-%(second_group_name)s",
                ["first_group_name", "second_group_name"],
            )
        ]
        result = regex_helper.normalize(pattern)
        self.assertEqual(result, expected)

    def test_group_backreference(self):
        pattern = r"(?P<first_group_name>.*)-(?P=first_group_name)"
        expected = [("%(first_group_name)s-%(first_group_name)s", ["first_group_name"])]
        result = regex_helper.normalize(pattern)
        self.assertEqual(result, expected)


class HasNamedGroupTests(unittest.TestCase):
    def test_named_group(self):
        self.assertIs(has_named_group(r"(?P<pk>\d+)"), True)

    def test_positional_group(self):
        self.assertIs(has_named_group(r"(\d+)"), False)

    def test_no_group(self):
        self.assertIs(has_named_group(r"^$"), False)

    def test_invalid_pattern(self):
        with self.assertRaises(re.error):
            has_named_group(r"(")

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            has_named_group(1)


class LazyReCompileTests(SimpleTestCase):
    def test_flags_with_pre_compiled_regex(self):
        test_pattern = re.compile("test")
        lazy_test_pattern = regex_helper._lazy_re_compile(test_pattern, re.I)
        msg = "flags must be empty if regex is passed pre-compiled"
        with self.assertRaisesMessage(AssertionError, msg):
            lazy_test_pattern.match("TEST")
