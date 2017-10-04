#-*- coding: utf-8 -*-
import re
from collections import Counter

from pattern.web import Wikipedia
from pattern.web import plaintext


class WikiParser:
    def __init__(self):
        self.wiki = Wikipedia()

    def get_articles(self, start, depth, max_count=None):
        atricles = []
        housing = [start]
        current_depth = 0

        while current_depth < depth:
            cross_references = []
            while housing:
                article = self.wiki.article(housing.pop())
                words = re.findall(r'\w+', article.plaintext())

                cross_references.extend(article.links)
                atricles.append(' '.join(words).lower())

            current_depth += 1
            housing.extend(cross_references)

        return atricles[:max_count]


class TextStatistics:
    def __init__(self, articles):
        self.articles = articles
        words = ' '.join(self.articles).split()
        self.words = [word for word in words if not word.isdigit()]

    def _tuple_from_counter(self, counter):
        return [tuple(i[0] for i in counter), tuple(i[1] for i in counter)]

    def get_top_3grams(self, n=None):
        n_gramms = []

        for index in range(2, len(self.words)):
            first = self.words[index-2]
            second = self.words[index-1]
            third = self.words[index]
            n_gramms.append('%s %s %s' % (first, second, third))

        return self._tuple_from_counter(Counter(n_gramms).most_common(n))


    def get_top_words(self, n=None):
        return self._tuple_from_counter(Counter(self.words).most_common(n))


class Experiment:
    @staticmethod
    def show_results():
        """
        Top 20 words by housing:
            the - 33761
            of - 22246
            and - 16226
            a - 14957
            in - 14163
            to - 11992
            is - 8605
            for - 6141
            as - 5507
            that - 4853
            are - 4288
            on - 3853
            language - 3814
            by - 3792
            or - 3768
            with - 3406
            be - 3387
            s - 3056
            it - 2732
            from - 2709
        Top 20 n-gramms by housing:
            from the original - 306
            archived from the - 296
            natural language processing - 285
            the original on - 238
            the use of - 235
            as well as - 220
            one of the - 194
            proceedings of the - 188
            a b c - 186
            part of speech - 177
            cambridge university press - 160
            the european union - 155
            such as the - 154
            the number of - 144
            university press isbn - 141
            for example the - 139
            of the european - 138
            a number of - 138
            a set of - 131
            based on the - 130
        Top 5 words for article 'Natural language processing':
            of - 155
            the - 148
            a - 83
            and - 70
            language - 59
        Top 5 n-gramms for article 'Natural language processing':
            natural language processing - 12
            hand written rules - 6
            a chunk of - 6
            chunk of text - 6
            machine learning algorithms - 5
        """
        title = 'Natural language processing'

        article = WikiParser().get_articles(title, depth=2)
        staticstics = TextStatistics(article)

        print 'Top 20 words by housing:'
        top = staticstics.get_top_words(20)
        for word, freq in zip(top[0], top[1]):
            print '  %s - %s' % (word, freq)

        print 'Top 20 n-gramms by housing:'
        top = staticstics.get_top_3grams(20)
        for n_gramm, freq in zip(top[0], top[1]):
            print '  %s - %s' % (n_gramm, freq)

        article = WikiParser().get_articles(title, depth=1)
        staticstics = TextStatistics(article)

        print 'Top 5 words for article \'%s\':' % title
        top = staticstics.get_top_words(5)
        for word, freq in zip(top[0], top[1]):
            print '  %s - %s' % (word, freq)


        print 'Top 5 n-gramms for article \'%s\':' % title
        top = staticstics.get_top_3grams(5)
        for n_gramm, freq in zip(top[0], top[1]):
            print '  %s - %s' % (n_gramm, freq)


if __name__ == '__main__':
    Experiment.show_results()
