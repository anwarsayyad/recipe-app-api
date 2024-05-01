"""
Sample tests
"""
from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):
    """Test the calc module."""
    def test_add_numbrs(self):
        """Test adding numbers together."""
        res = calc.add(5, 5)
        self.assertEqual(res, 10)

    def test_subtract_numbers(self):
        """Test Subtracking numbers."""
        res = calc.subtract(15, 10)
        self.assertEqual(res, 5)
