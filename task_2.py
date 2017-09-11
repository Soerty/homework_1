#-*- coding: utf-8 -*-


class UniqObject(object):
    """A class implementing a singleton pattern.

    The class has a static method create_object(). A class
    has a static creative method that creates a new instance
    or returns a previously created instance.

    >>> object_one = UniqObject.create_object()
    >>> object_two = UniqObject.create_object()
    >>> object_one is object_two
    True
    """
    __instance = None

    @staticmethod
    def create_object():
        if UniqObject.__instance is not None:
            return UniqObject.__instance

        object = UniqObject()
        UniqObject.__instance = object
        return object


if __name__ == "__main__":
    import doctest
    doctest.testmod()
