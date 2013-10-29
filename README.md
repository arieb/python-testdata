python-testdata
===============

A simple package that generates data for tests.

testdata provides the basic Factory and DictFactory classes that generate content.
it also provides many more specialized factories that provide extended functionality.
every Factory instance knows how many elements its going to generate, this enables us to generate statistical results.

testdata isn't bound to a specifc database, but does include database specfic modules (like MongoDB - mongo_factories.py)
but it will always be clean of database related dependencies.

## Examples
We integrate the awsome fake-factory package to generate data using FakeDataFactory.

lets create a very simple factory that generates Users:

```python
import testdata

class Users(testdata.DictFactory):
    id = testdata.CountingFactory(10)
    firstname = testdata.FakeDataFactory('firstName')
    lastname = testdata.FakeDataFactory('lastName')
    address = testdata.FakeDataFactory('address')
    age = testdata.RandomInteger(10, 30) 
    gender = testdata.RandomSelection(['female', 'male'])

for user in Users(10): # let say we only want 10 users
    print user
    # or more likely you'd want to insert them into your favorite database (MongoDB, ElasticSearch, ..)
```

## Todos
* Add usage documentation for each factory (using doctest maybe?)
* Add tests
* Add GeoLocationFactories to generates Location and distance related data (for example, random points near a central point).
  to a total of a 100 precent. so it will 
* Add Statistical Factories
