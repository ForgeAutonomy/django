from django.test import SimpleTestCase
from django.utils.xmlutils import strip_illegal_xml_chars


class StripIllegalXMLCharsTests(SimpleTestCase):
    def test_null_character(self):
        self.assertEqual(strip_illegal_xml_chars("a\x00b"), "ab")

    def test_allowed_whitespace(self):
        self.assertEqual(strip_illegal_xml_chars("a\tb\nc\rd"), "a\tb\nc\rd")

    def test_illegal_characters(self):
        self.assertEqual(strip_illegal_xml_chars("x\x0b\x0cy\ufffe"), "xy")

    def test_empty_string(self):
        self.assertEqual(strip_illegal_xml_chars(""), "")

    def test_allowed_characters(self):
        text = "Hello, world! <tag> & \u00e9\u4e2d\U0001f600"
        self.assertEqual(strip_illegal_xml_chars(text), text)

    def test_bytes(self):
        with self.assertRaises(TypeError):
            strip_illegal_xml_chars(b"abc")
