python-testdata
===============

A simple package that generates data for tests.

testdata provides the basic Factory and DictFactory classes that generate content.
it also provides many more specialized factories that provide extended functionality.
every Factory instance knows how many elements its going to generate, this enables us to generate statistical results.

testdata isn't bound to a specifc database, but does include database specfic modules inside, like - extra.mongodb.py)
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
    # {'firstname': 'Toni', 'lastname': 'Schaden', 'gender': 'female', 'age': 18, 'address': '0641 Homenick Hills\nSouth Branson, RI 70388', 'id': 10}
    # {'firstname': 'Gene', 'lastname': 'Greenfelder', 'gender': 'male', 'age': 17, 'address': '292 Loy Lights Suite 328\nFritzfort, IN 73914', 'id': 11}
    # or more likely you'd want to insert them into your favorite database (MongoDB, ElasticSearch, ..)
```

## Factories
See Docstrings for more examples and doctests.

#### Bases
|Factory Class| Description|
|:-------|:-----------|
| Factory | The base class of all the factories.|
| DictFactory | A very powerful base class. allows sub classing to create factories that generate dicts with a specific schema (see [Examples][#Examples]). |
| ListFactory | A factory that returns on each iteration a list of `elements_per_list` items returned from calls to the given factory. |
| Callable | Gets a callable object as an argument and returns the result of calling the object on every iteration |
| ClonedField | A factory that copies the value of another factory. |
#### Dates
|Factory Class| Description|
|:-------|:-----------|
| RandomDateFactory | Generates random dates (python's datetime) between 2 dates|
| DateIntervalFactory | Generates datetime objects starting from `base` while adding  `delta` to it each iteration.
| RelativeToDatetimeField | Generates datetime object relative to another datetime field, like if you have `start_time` which is a RandomDateFactory field, and want an `end_time` field that is always 15 minutes later.| 

And MUCH MUCH more.. 

## Todos
* Add usage documentation for each factory (using doctest maybe?)
* Add more tests
* Add GeoLocationFactories to generates Location and distance related data (for example, random points near a central point).
* Add Statistical Factories
