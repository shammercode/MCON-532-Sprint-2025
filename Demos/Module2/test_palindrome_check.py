import unittest
from Demos.Module2.palindrome_check import is_palindrome


class MyTestCase(unittest.TestCase):
    def test_palindrome_basic(self):
        self.assertEqual(is_palindrome("racecar"), True)
    def test_not_palindrome(self):
        self.assertEqual(is_palindrome("vroom"), False)
    def test_palindrome_spaces(self):
        self.assertEqual(is_palindrome("a man a plan a canal panama"), True)
    def test_palindrome_cases(self):
        self.assertEqual(is_palindrome("RoTaTOr"), True)
    def test_palindrome_not_chars(self):
        self.assertEqual(is_palindrome("kayak!"), True)
    def test_palindrome_single_char(self):
        self.assertEqual(is_palindrome("a"), True)
    def test_palindrome_empty_space(self):
        self.assertEqual(is_palindrome(" "), True)
    def test_palindrome_all_edge_cases(self):
        self.assertEqual(is_palindrome("A Man A Plan A Canal Panama!"), True)
if __name__ == '__main__':
    unittest.main()
