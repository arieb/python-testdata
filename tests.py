import doctest

if __name__ == '__main__':
    import testdata
    doctest.testmod(testdata.base)
    doctest.testmod(testdata.dictionary)
    doctest.testmod(testdata.factories.statistical)
    doctest.testmod(testdata.factories.datetimes)
    doctest.testmod(testdata.factories.generic)
    doctest.testmod(testdata.factories.sequences)
    doctest.testmod(testdata.factories.numbers)
