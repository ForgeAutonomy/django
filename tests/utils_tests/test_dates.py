from django.test import SimpleTestCase
from django.utils.dates import is_weekend


class IsWeekendTests(SimpleTestCase):
    def test_weekdays(self):
        for weekday in range(5):
            with self.subTest(weekday=weekday):
                self.assertIs(is_weekend(weekday), False)

    def test_weekend(self):
        for weekday in (5, 6):
            with self.subTest(weekday=weekday):
                self.assertIs(is_weekend(weekday), True)

    def test_out_of_range(self):
        for weekday in (-1, 7):
            with self.subTest(weekday=weekday):
                with self.assertRaises(ValueError):
                    is_weekend(weekday)

    def test_invalid_type(self):
        for weekday in (True, "5"):
            with self.subTest(weekday=weekday):
                with self.assertRaises(TypeError):
                    is_weekend(weekday)
