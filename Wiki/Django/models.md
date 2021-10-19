## Models
Each model has at least one Manager, and it’s called objects by default.
## Relationships
Django provides three most common types of relationships `many-to-one`, `many-to-many` and `one-to-one`.
1. #### Many-to-one relationships
To define a many-to-one relationship, use `django.db.models.ForeignKey` which requires a positional argument: the 
class to which the model is related. Reverse look up uses model name in lower case appended by underscore and set 
keyword `book_set`

Forward access to one-to-many relationships is cached the first time the related object is accessed. 
Subsequent accesses to the foreign key on the same object instance are cached.
```shell
>>> e = Entry.objects.get(id=2)
>>> print(e.blog)  # Hits the database to retrieve the associated Blog.
>>> print(e.blog)  # Doesn't hit the database; uses cached version.
# Note that the select_related() QuerySet method recursively prepopulates the cache of all one-to-many relationships ahead of time.
>>> e = Entry.objects.select_related().get(id=2)
>>> print(e.blog)  # Doesn't hit the database; uses cached version.
>>> print(e.blog)  # Doesn't hit the database; uses cached version.
```
#### select_related
Returns a QuerySet that will “follow” `foreign-key` relationships, selecting additional related-object data when it executes its query. 
This is a performance booster which results in a single more complex query but means later use of foreign-key relationships won’t 
require database queries.

There may be some situations where you wish to call select_related() with a lot of related objects, or where you don’t know 
all of the relations. In these cases it is possible to call select_related() with no arguments.
Chaining select_related calls works in a similar way to other methods - that is that `select_related('foo', 'bar')`
is equivalent to `select_related('foo').select_related('bar')`. select_related is limited to single-valued relationships - `foreign key` and `one-to-one`.

#### prefetch_related()
does a separate lookup for each relationship, and does the ‘joining’ in Python. This allows it to prefetch `many-to-many` 
and `many-to-one` objects, it executed once the main query is executed so each `prefetch_related` results in a separate query.

2. #### Many-to-Many relationships
To define a many-to-many relationship, use `ManyToManyField`, which requires a positional argument: the 
class to which the model is related. It’s suggested, but not required, that the name of a ManyToManyField be a 
plural describing the set of related model objects. Generally, ManyToManyField instances should go in the object 
that’s going to be edited on a form.

When you’re only dealing with many-to-many relationships, sometimes you may need to associate data with the relationship between two models.
For example, consider the case of an application tracking the musical groups which musicians belong to. 
There is a many-to-many relationship between a person and the groups of which they are a member, so you could use a 
ManyToManyField to represent this relationship. However, there is a lot of detail about the membership that you 
might want to collect, such as the date at which the person joined the group.

For these situations, Django allows you to specify the model that will be used to govern the many-to-many relationship. 
You can then put extra fields on the intermediate model. The intermediate model is associated with the ManyToManyField 
using the through argument to point to the model that will act as an intermediary. For our musician example, the code 
would look something like this:
```python
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
```
When you set up the intermediary model, you explicitly specify foreign keys to the models that are involved 
in the many-to-many relationship.

Both ends of a many-to-many relationship get automatic API access to the other end. The API works similar to a
“backward” one-to-many relationship, The model that defines the ManyToManyField uses the attribute name of that 
field itself, whereas the “reverse” model uses the lowercased model name of the original model, plus '_set' 
3. ### One-to-one relationships
`OneToOneField` is used to define this, This is most useful on the primary key of an object when that object 
“extends” another object in some way.  If you define a OneToOneField on your model, instances of that model 
will have access to the related object via an attribute of the model and reverse model can access via lower cased model name.

`Note` If you need to create a relationship on a model that has not yet been defined, you can use the name of 
the model, rather than the model object itself. i.e `manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)`
#### Field Name Restrictions
A field name cannot contain more than one underscore in a row, due to the way Django’s query lookup syntax works and it can't
end with an underscore for same reason.
`get_absolute_url()` tells Django how to calculate the URL for an object.
## Tables
`Verbose name` is an option first positional parameter for all field except relational ones, for those you need to provide 
it using `verbose_name` keyword argument.

`blank and null`: `null` is purely `database-related`, whereas `blank` is `validation-related`. If a field has 
blank=True, form validation will allow entry of an empty value.

#### Table Names
Table names are automatically derived from Django app that you created, followed by underscore and model name.
To override the database table name, use the `db_table` parameter in `class Meta`.

```markdown
For example, if you have an app bookstore (as created by manage.py startapp bookstore), a model defined as class 
Book will have a database table named bookstore_book. This model will then not be used to create any database table. 
```

## Model inheritance
1. ### Abstract base classes
Abstract base classes are useful when you want to put some common information into a number of other models. You write 
your base class and put abstract=True in the Meta class
2. ### Multi-table inheritance
he second type of model inheritance supported by Django is when each model in the hierarchy is a model all by itself.
The inheritance relationship introduces links between the child model and each of its parents (via an automatically-
created OneToOneField).
3. ### Proxy models
You can create, delete and update instances of the proxy model and all the data will be saved as if you were using the 
original (non-proxied) model. The difference is that you can change things like the default model ordering or the 
default manager in the proxy, without having to alter the original.

Proxy models are declared like normal models. You tell Django that it’s a proxy model by setting the proxy attribute of 
the Meta class to True.
```python
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class MyPerson(Person):
    class Meta:
        proxy = True

    def do_something(self):
        # ...
        pass
```
The MyPerson class operates on the same database table as its parent Person class. In particular, any new instances of Person will also be 
accessible through MyPerson
```shell
>>> p = Person.objects.create(first_name="foobar")
>>> MyPerson.objects.get(first_name="foobar")
<MyPerson: foobar>
```
A proxy model must inherit from exactly one non-abstract model class, A proxy model can inherit from any 
number of abstract model classes, providing they do not define any model fields. A proxy model may also 
inherit from any number of proxy models that share a common non-abstract parent class.
4. ### Multiple inheritance
it’s possible for a Django model to inherit from multiple parent models.

A derived class can remove field define in base class setting it None, i.e `field_name = None` 