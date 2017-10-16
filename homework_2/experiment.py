#-*- coding: utf-8 -*-
import re
from collections import Counter

from pattern.web import Wikipedia
from pattern.web import plaintext


class WikiParser:
    def __init__(self):
        self.wiki = Wikipedia()

    def get_articles(self, start, depth, max_count=15):
        atricles = []
        housing = [start]
        current_depth = 0
        current_count = 0

        while current_depth < depth:
            cross_references = []
            while housing and current_count < max_count:
                article = self.wiki.article(housing.pop())
                words = re.findall(r'\w+', article.plaintext())

                cross_references.extend(article.links)
                atricles.append(' '.join(words).lower())

                current_count += 1

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
            word - 387
            language - 351
            web - 264
            sense - 254
            turing - 253
            words - 249
            test - 241
            turkish - 232
            can - 216
            such - 181
            has - 168
            machine - 164
            was - 158
            retrieved - 155
            learning - 148
            e - 145
            wordnet - 145
            have - 145
            one - 136
            disambiguation - 134
        Top 20 n-gramms by housing:
            word sense disambiguation - 93
            world wide web - 66
            natural language processing - 40
            association computational linguistics - 33
            turkish language association - 22
            meeting association computational - 19
            annual meeting association - 19
            press isbn 0 - 17
            isbn 978 0 - 16
            word sense induction - 16
            oxford university press - 15
            retrieved 27 july - 15
            retrieved 2007 03 - 14
            27 july 2009 - 14
            university press isbn - 13
            wide web consortium - 13
            t rk e - 13
            tim berners lee - 11
            2007 retrieved 2007 - 11
            lexical knowledge base - 10
        Top 5 words for article 'Natural language processing':
            language - 59
            natural - 35
            such - 30
            processing - 24
            text - 22
        Top 5 n-gramms for article 'Natural language processing':
            natural language processing - 12
            hand written rules - 6
            machine learning algorithms - 5
            isbn 978 0 - 5
            natural language understanding - 3
        """
        title = 'Natural language processing'

        article = WikiParser().get_articles(title, depth=2)
        staticstics = TextStatistics(article)

        print ('Top 20 words by housing:')
        top = staticstics.get_top_words(20)
        for word, freq in zip(top[0], top[1]):
            print ('  %s - %s' % (word, freq))

        print ('Top 20 n-gramms by housing:')
        top = staticstics.get_top_3grams(20)
        for n_gramm, freq in zip(top[0], top[1]):
            print ('  %s - %s' % (n_gramm, freq))

        article = WikiParser().get_articles(title, depth=1)
        staticstics = TextStatistics(article)

        print ('Top 5 words for article \'%s\':' % title)
        top = staticstics.get_top_words(5)
        for word, freq in zip(top[0], top[1]):
            print ('  %s - %s' % (word, freq))


        print ('Top 5 n-gramms for article \'%s\':' % title)
        top = staticstics.get_top_3grams(5)
        for n_gramm, freq in zip(top[0], top[1]):
            print ('  %s - %s' % (n_gramm, freq))


if __name__ == '__main__':
    Experiment.show_results()
