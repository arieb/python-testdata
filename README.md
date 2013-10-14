python-testdata
===============

A simple package that generates data for tests.

# Example
```python
class UserFactory(DictFactory):
    firstname = StringFactory(min_chars=3, max_chars=10)
    lastname = StringFactory(prefix="N", max_chars=10)
    age = RandomSelection(xrange(1, 60))
    email = StringFactory(suffix="@mail.com", max_char=10)

TAGS = ["mongodb", "python", "mongo", "foo"]

class PostFactory(DictFactory):
    owner = FieldFromDocument("collection_name", "id", default=None)
    tags = ListFactory(element_amount=3, choices=TAGS)
    comment = CommentFactory

class Comment(DictFactory):
    creation_date = DateFactory(max=datetime.now(), min=datetime.now()- datetime.timedelta(day=1))
    content = LoremIpsumFactory(max_chars=30)


for user in UserFactory(100):
    # do something with the new user user

```
