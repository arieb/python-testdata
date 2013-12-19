import doctest

if __name__ == '__main__':
    import testdata
    doctest.testmod(testdata.base)
    doctest.testmod(testdata.dictonaries)
    doctest.testmod(testdata.factories.datetimes)
    doctest.testmod(testdata.factories.generic)
    doctest.testmod(testdata.factories.sequences)
