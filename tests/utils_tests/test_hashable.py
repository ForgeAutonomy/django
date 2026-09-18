from django.test import SimpleTestCase
from django.utils.hashable import is_hashable, make_hashable


class TestHashable(SimpleTestCase):
    def test_is_hashable(self):
        for value in (1, "a", (1, 2), frozenset(), None):
            with self.subTest(value=value):
                self.assertIs(is_hashable(value), True)

    def test_is_not_hashable(self):
        for value in ([], {}, set(), ([1],)):
            with self.subTest(value=value):
                self.assertIs(is_hashable(value), False)

    def test_make_hashable_is_hashable(self):
        self.assertIs(is_hashable(make_hashable([1, {2: 3}])), True)

    def test_equal(self):
        tests = (
            ([], ()),
            (["a", 1], ("a", 1)),
            ({}, ()),
            ({"a"}, ("a",)),
            (frozenset({"a"}), {"a"}),
            ({"a": 1, "b": 2}, (("a", 1), ("b", 2))),
            ({"b": 2, "a": 1}, (("a", 1), ("b", 2))),
            (("a", ["b", 1]), ("a", ("b", 1))),
            (("a", {"b": 1}), ("a", (("b", 1),))),
        )
        for value, expected in tests:
            with self.subTest(value=value):
                self.assertEqual(make_hashable(value), expected)

    def test_count_equal(self):
        tests = (
            ({"a": 1, "b": ["a", 1]}, (("a", 1), ("b", ("a", 1)))),
            ({"a": 1, "b": ("a", [1, 2])}, (("a", 1), ("b", ("a", (1, 2))))),
        )
        for value, expected in tests:
            with self.subTest(value=value):
                self.assertCountEqual(make_hashable(value), expected)

    def test_unhashable(self):
        class Unhashable:
            __hash__ = None

        with self.assertRaisesMessage(TypeError, "unhashable type: 'Unhashable'"):
            make_hashable(Unhashable())
