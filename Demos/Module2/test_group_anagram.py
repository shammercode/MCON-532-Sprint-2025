import unittest

from Demos.Module2.group_anagram import group_anagrams


class TestGroupAnagram(unittest.TestCase):
    def test_group_anagram(self):
        words = ["listen", "silent", "enlist", "rat", "tar", "art", "star"]
        result = group_anagrams(words)

        # Sorting values to ensure order doesn't affect the comparison
        sorted_groups = {key: sorted(value) for key, value in result.items()}

        self.assertTrue(sorted_groups == {
            "eilnst": ["enlist", "listen", "silent"],
            "art": ["art", "rat", "tar"],
            "arst": ["star"]
        })

if __name__ == '__main__':
    unittest.main()
