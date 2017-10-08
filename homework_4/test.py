#-*- coding: utf-8 -*-
import unittest

from rabin import search_rabin_multi


class TestRabinKarpMultiSearch(unittest.TestCase):
    def setUp(self):
        self.text = 'If there is a will, there is a way'

    def test_search_with_empty_patterns(self):
        self.assertEqual(search_rabin_multi(self.text, []), [])

    def test_search_with_empty_text(self):
        self.assertEqual(search_rabin_multi('', []), [])

    def test_left_border_in_search(self):
        self.assertEqual(search_rabin_multi(self.text, ['If']), [[0]])

    def test_right_border_in_search(self):
        self.assertEqual(search_rabin_multi(self.text, ['way']), [[self.text.index('way')]])

    def test_correct_count_return_values(self):
        self.assertEqual(len(search_rabin_multi(self.text, ['is', 'a'])), 2)

    def test_if_patterns_is_tuple(self):
        self.assertEqual(len(search_rabin_multi(self.text, ('is', 'a'))), 2)

    def test_check_correct_structure_in_return_value(self):
        self.assertEqual(search_rabin_multi(self.text, ['If', 'there']), [[0], [3, 20]])



if __name__ == '__main__':
    unittest.main()