#-*- coding: utf-8 -*-
from __future__ import division
import re
import math
from collections import Counter

from pattern.web import Wikipedia
from pattern.web import plaintext


class WikiParser:
    def __init__(self):
        self.wiki = Wikipedia()

    def get_articles(self, start, depth, max_count=None):
        """Returns all articles starting with `start`

        `start` is the initial article. `depth` is the depth of the
        search for articles on cross-references. `max_count` is
        maximum number of returned articles. Articles are returned
        as an array of lines, where each line is an article without
        punctuation marks, except points. For example:

        >>> parser = WikiParser()
        >>> title = 'Natural language processing'
        >>> len(parser.get_articles(title, depth=1)) is 1
        True
        """
        atricles = []
        housing = [start]
        current_depth = 0

        while current_depth < depth:
            # Links in the current article to other articles
            cross_references = []

            # To extract one article, while in the corpus there are articles
            while housing:
                article = self.wiki.article(housing.pop())
                cross_references.extend(article.links)

                # Find all sentence in article
                sentences = re.findall(r'(.*?\w+[\.\?\!\;])', article.plaintext())
                # Find all words in each sentence
                words_in_sentences = [re.findall(r'\w+', sentence) for sentence in sentences]
                # Join all words in each sentence
                words = [' '.join(i) + '.' for i in words_in_sentences]
                # Save the current article as a processed string
                atricles.append(' '.join(words).lower())

            current_depth += 1
            housing.extend(cross_references)

        return atricles[:max_count]


class TextStatistics:
    def __init__(self, articles):
        self.articles = articles
        self.articles_in_one_line = ' '.join(self.articles)
        stop_words = ['the', 'of', 'and', 'a', 'in', 'to', 'is', 'for', 'as',
            'an', 'this', 'at', 'not', 'which', 'that', 'are', 'on', 'by', 'or',
            'be', 'with', 's', 'it', 'from']
        self.words = filter(lambda x: x not in stop_words,
                            re.findall(r'\w+', self.articles_in_one_line))

    def _tuple_from_counter(self, counter):
        return [tuple(i[0] for i in counter), tuple(i[1] for i in counter)]

    def get_top_3grams(self, n=None, use_idf=False):
        """Returns the most frequent trigrams from all articles

        `n` is the number of the most frequent trigrams that must be
        returned. `use_idf` is the flag at which the frequency is
        calculated as an IDF parameter.

        >>> articles = ['this and article of.', 'processing of language.']
        >>> experiment = TextStatistics(articles)
        >>> experiment.get_top_3grams(n=3)
        [('le ', 'ang', 'art'), (1, 1, 1)]
        >>> experiment.get_top_3grams(n=3, use_idf=True)
        [('le ', 'ang', 'art'), (0.30102999566398114, 0.30102999566398114, 0.30102999566398114)]
        """
        n_gramms = []

        # Split all words by letters
        letters = list(' '.join(self.words))

        for i in range(2, len(letters)):
            first, second, third = letters[i-2], letters[i-1], letters[i]

            # Skip n-gramm If there are more than two spaces in a row
            if (first == second == ' ') or (second == third == ' '):
                continue

            n_gramms.append(''.join([first, second, third]))

        # Get top n-gramms
        top_n_gramms = Counter(n_gramms).most_common(n)

        if not use_idf:
            return self._tuple_from_counter(top_n_gramms)

        top_n_gramms_with_idf = []
        for n_gramm, freq in top_n_gramms:
            idf = math.log(len(self.articles) / self.articles_in_one_line.count(n_gramm), 10)
            top_n_gramms_with_idf.append((n_gramm, idf))
        
        return self._tuple_from_counter(top_n_gramms_with_idf)

    def get_top_words(self, n=None, use_idf=False):
        """Returns the most frequent words from all articles

        `n` is the number of the most frequent words that must be
        returned. `use_idf` is the flag at which the frequency is
        calculated as an IDF parameter.

        >>> articles = ['this and article of and.', 'processing of language of.']
        >>> experiment = TextStatistics(articles)
        >>> experiment.get_top_words(3)
        [('article', 'processing', 'language'), (1, 1, 1)]
        >>> experiment.get_top_words(3, use_idf=True)
        [('article', 'processing', 'language'), (0.30102999566398114, 0.30102999566398114, 0.30102999566398114)]
        """

        top_words = Counter(self.words).most_common(n)

        if not use_idf:
            return self._tuple_from_counter(top_words)

        top_words_with_idf = []
        for n_gramm, freq in top_words:
            idf = math.log(self.articles_in_one_line.count('.') /
                           self.articles_in_one_line.count(n_gramm), 10)
            top_words_with_idf.append((n_gramm, idf))

        return self._tuple_from_counter(top_words_with_idf)


class Experiment:
    @staticmethod
    def show_results():
        """
        Top 20 words by housing:
            language - 1.00883192489
            can - 1.2218728848
            was - 1.43634278818
            retrieved - 1.46547698624
            such - 1.48163363481
            have - 1.47482850526
            speech - 1.48715557166
            words - 1.48410982165
            english - 1.51557347295
            word - 1.16023816799
            used - 1.48632279195
            languages - 1.52486835928
            has - 1.45761860871
            p - -0.177891577044
            other - 1.41113487303
            also - 1.56985203602
            1 - 0.385151817281
            may - 1.58734276818
            one - 1.17542204226
            text - 1.39985386262
        Top 20 n-gramms by housing:
            ed  - -2.05487107024
            ion - -2.05303666632
            ing - -2.03471126614
            tio - -1.99775191021
            es  - -1.92889100939
            ng  - -1.9593006881
            on  - -1.99334037033
             co - -1.93647003109
            er  - -1.89033595476
            ati - -1.90282437247
            al  - -1.8836922876
            ent - -1.84174701184
             re - -1.82695461841
             in - -2.11257950376
             pr - -1.74275927529
            the - -2.34078886142
            ter - -1.70631880647
             ma - -1.67609691457
             th - -2.39386120557
            ly  - -1.63423624499
        """
        title = 'Natural language processing'

        article = WikiParser().get_articles(title, depth=2)
        staticstics = TextStatistics(article)

        print 'Top 20 words by housing:'
        top = staticstics.get_top_words(20, use_idf=True)
        for word, freq in zip(top[0], top[1]):
            print '  %s - %s' % (word, freq)

        print 'Top 20 n-gramms by housing:'
        top = staticstics.get_top_3grams(20, use_idf=True)
        for n_gramm, freq in zip(top[0], top[1]):
            print '  %s - %s' % (n_gramm, freq)

        article = WikiParser().get_articles(title, depth=1)
        staticstics = TextStatistics(article)



if __name__ == "__main__":
    import doctest
    doctest.testmod()
    Experiment.show_results()