#-*- coding: utf-8 -*-
import unittest

from experiment import TextStatistics


class TestTextStatistics(unittest.TestCase):
    def setUp(self):
        articles = ['this and article of.', 'processing of language.']
        self.experiment = TextStatistics(articles)

    def test_get_top_3grams(self):
        self.assertEqual(
            self.experiment.get_top_3grams(n=3),
            [('le ', 'ang', 'art'), (1, 1, 1)]
        )

    def test_get_top_3grams_with_idf(self):
        self.assertEqual(
            self.experiment.get_top_3grams(n=3, use_idf=True),
            [('le ', 'ang', 'art'), (0.30102999566398114, 0.30102999566398114, 0.30102999566398114)]
        )

    def test_get_top_words(self):
        self.assertEqual(
            self.experiment.get_top_words(3),
            [('article', 'processing', 'language'), (1, 1, 1)]
        )

    def test_get_top_words_with_idf(self):
        self.assertEqual(
            self.experiment.get_top_words(3, use_idf=True),
            [('article', 'processing', 'language'), (0.30102999566398114, 0.30102999566398114, 0.30102999566398114)]
        )


if __name__ == '__main__':
    unittest.main()