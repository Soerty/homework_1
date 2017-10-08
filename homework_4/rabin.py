#-*- coding: utf-8 -*-
import random


class PolynomialHash:
    _prime_numbers = [
           2,   31,   73,  127,  179,  233,  283,  353,  419,  467,
         547,  607,  661,  739,  811,  877,  947, 1019, 1087, 1153,
        1229, 1297, 1381, 1453, 1523, 1597, 1663, 1741, 1823, 1901,
        1993, 2063, 2131, 2221, 2293, 2371, 2437, 2539, 2621, 2689,
        2749, 2833, 2909, 3001, 3083, 3187, 3259, 3343, 3433, 3517
    ]
    q = random.choice(_prime_numbers)
    x = random.randint(0, q - 1)

    def __init__(self, string):
        self.string = string

    @property
    def hash(self):
        """Modification of the polynomial hash proposed by Ditzfelbinger

        >>> poly_hash = PolynomialHash('hello world')
        >>> poly_hash.q, poly_hash.x = 811, 240
        >>> poly_hash.hash
        2520
        """
        hash = 0

        for index, letter in enumerate(self.string):
            hash += (ord(letter) * (self.x ** len(self.string) - index)) % self.q

        return hash


def search_rabin_naive(text, pattern):
    """Implements the Rabin-Karp algorithm

    The Rabin-Karp algorithm is a string search algorithm that looks
    for a pattern, that is, a substring, in the text, using hashing.

    >>> search_rabin_naive('hello world, hello', 'hello')
    [0, 13]
    >>> search_rabin_naive('bla bla and bla', 'nothing')
    []
    """
    indices = []

    for index in range(len(text) - len(pattern) + 1):
        if text[index: index + len(pattern)] == pattern:
            indices.append(index)

    return indices


def search_rabin_multi(text, patterns):
    """Implements the Rabin-Karp algorithm with multi-search

    This implementation can search for several patterns in a string,
    returning a list of occurrences for each pattern.

    >>> search_rabin_multi('hello world, hello', ['hello', 'world'])
    [[0, 13], [6]]
    >>> search_rabin_multi('bla bla and bla', ['bla', 'nothing'])
    [[0, 4, 12], []]
    """
    indices = []
    hash_patterns = (PolynomialHash(pattern) for pattern in patterns)

    for pattern in hash_patterns:
        text_patterns = (
            [index, PolynomialHash(text[index: index + len(pattern.string)])]
                for index in range(len(text) - len(pattern.string) + 1)
        )
        indices.append([i for i, tp in text_patterns if tp.hash == pattern.hash])

    return indices



if __name__ == '__main__':
    import doctest
    doctest.testmod()