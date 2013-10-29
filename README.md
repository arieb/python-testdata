python-testdata
===============

A simple package that generates data for tests.

testdata provides the basic Factory and DictFactory classes that generate content.
it also provides many more specialized factories that provide extended functionality.
every Factory instance knows how many elements its going to generate, this enables us to generate statistical results.

testdata isn't bound to a specifc database, but does include database specfic modules (like MongoDB - mongo_factories.py)
but it will always be clean of database related dependencies.

# Examples
```python
We integrate the awsome fake-factory package to generate data using FakeDataFactory.

lets create a very simple factory that generates Users:

import testdata

class User(testdata.DictFactory):
    id = testdata.CountingFactory(10)
    firstname = testdata.FakeDataFactory('firstName')
    lastname = testdata.FakeDataFactory('lastName')
    address = testdata.FakeDataFactory('address')
    age = testdata.RandomInteger(10, 30) 
    gender = testdata.RandomSelection(['female', 'male'])
```
