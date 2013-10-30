import doctest

if __name__ == '__main__':
    import testdata
    doctest.testmod(testdata.date_factories)
    doctest.testmod(testdata.base_factories)
