#-*- coding: utf-8 -*-


def fibonachi(n):
    """The calculation of Fibonacci numbers for n > 0.

    If the number is greater than zero, then returns the Fibonacci number.
    Else return 0.
    
    :param n: The number
    :return: returns Fibonacci number

    >>> fibonachi(-10)
    0
    >>> fibonachi(1)
    1
    >>> fibonachi(10)
    55
    """

    if n < 1:
        return 0

    before_last = 0
    last = 1
    result = 1

    for i in range(2, n+1):
        result = before_last + last
        before_last, last = last, result

    return result


if __name__ == "__main__":
    import doctest
    doctest.testmod()
