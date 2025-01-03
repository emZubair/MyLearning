### Operators that return new QuerySets
#### AND (&), OR (|)
Combines two QuerySets using the SQL AND operator, The following are equivalent:
```shell
Model.objects.filter(x=1) & Model.objects.filter(y=2)
Model.objects.filter(x=1, y=2)
from django.db.models import Q
Model.objects.filter(Q(x=1) & Q(y=2))

Model.objects.filter(x=1) | Model.objects.filter(y=2)
Model.objects.filter(Q(x=1) | Q(y=2))

```
### Methods that do not return QuerySets
The following QuerySet methods evaluate the QuerySet and return something other than a QuerySet. These methods do not use a cache.
Rather, they query the database each time they’re called.
#### get(**kwargs)
Returns the object matching the given lookup parameters, You should use lookups that are guaranteed unique, such as the primary key 
or fields in a unique constraint. `Entry.objects.get(id=1)`
If you expect a queryset to already return one row, you can use get() without any arguments to return the object for that row,
`Entry.objects.filter(pk=1).get()`. 
If `get()` doesn’t find any object, it raises a `Model.DoesNotExist` exception or `get()` finds more than one object, 
it raises a `Model.MultipleObjectsReturned` exception.
#### create(**kwargs) and get_or_create(defaults=None, **kwargs)
`create()` convenience method for creating an object and saving it all in one step. `get_or_create(**kwargs)` a convenience method 
for looking up an object with the given kwargs or creating one if necessary.
Returns a tuple of (object, created), where object is the retrieved or created object and created is a boolean specifying 
whether a new object was created.
You can specify more complex conditions for the retrieved object by chaining `get_or_create()` with `filter()` and using Q objects. 
For example, to retrieve Robert or Bob Marley if either exists, and create the latter otherwise:
```shell
from django.db.models import Q

obj, created = Person.objects.filter(
    Q(first_name='Bob') | Q(first_name='Robert'),
).get_or_create(last_name='Marley', defaults={'first_name': 'Bob'})
```
#### update_or_create(defaults=None, **kwargs)
A convenience method for updating an object with the given kwargs, creating a new one if necessary. The defaults is a dictionary 
of `(field, value)` pairs used to update the object. The values in defaults can be callables.
#### bulk_create(objs, batch_size=None, ignore_conflicts=False), bulk_update(objs, fields, batch_size=None)
This method inserts the provided list of objects into the database in an efficient manner (generally `only 1 query`, 
no matter how many objects there are), and returns created objects as a list, in the same order as provided
```shell
>>> objs = Entry.objects.bulk_create([
...     Entry(headline='This is a test'),
...     Entry(headline='This is only a test'),
... ])
```
The model’s `save()` method will not be called, and the `pre_save` and `post_save` signals will not be sent.
#### count()
Returns an integer representing the number of objects in the database matching the QuerySet.

#### in_bulk(id_list=None, *, field_name='pk')
Takes a list of field values (id_list) and the field_name for those values, and returns a dictionary mapping each value to an 
instance of the object with the given field value. `field_name` must be a unique field or a distinct field (if there’s only one 
field specified in `distinct()`). `field_name` defaults to the primary key.
```shell
>>> Blog.objects.in_bulk([1])
{1: <Blog: Beatles Blog>}
>>> Blog.objects.in_bulk(['beatles_blog'], field_name='slug')
{'beatles_blog': <Blog: Beatles Blog>}
```
If you pass in_bulk() an empty list, you’ll get an empty dictionary. If id_list isn’t provided, all objects in the queryset are returned.

#### latest(*fields), earliest(*fields)
Returns the latest `(last)` object in the table based on the given field(s). `Entry.objects.latest('pub_date')`, You can also choose the 
latest based on several fields, while `earliest()` returns the oldest `(first)` result. Both throw exception if no match found.

#### first(), last()
Returns the first object matched by the queryset, or `None` if there is no matching object, 
`Article.objects.order_by('title', 'pub_date').first()`, `last()` returns the last or none.

#### exists()
Returns True if the QuerySet contains any results, and False if not. This tries to perform the query in the simplest and fastest 
way possible, but it does execute nearly the same query as a normal QuerySet query.
```shell
entry = Entry.objects.get(pk=123)
if some_queryset.filter(pk=entry.pk).exists():
    print("Entry contained in queryset")
# Above approach will be faster than 
if entry in some_queryset:
   print("Entry contained in QuerySet")    
```

#### update(**kwargs)
Performs an SQL update query for the specified fields, and returns the number of rows matched (which may not be equal to the number 
of rows updated if some rows already have the new value).
The update() method is applied instantly, and the only restriction on the QuerySet that is updated is that it can only update columns 
in the model’s main table, not on related models.
If you’re just updating a record and don’t need to do anything with the model object, the most efficient approach is to call `update()`, 
rather than loading the model object into memory.
```shell
>>> Entry.objects.filter(pub_date__year=2010).update(comments_on=False, headline='This is old')
>>> Entry.objects.update(blog__name='foo') # Won't work!
# Instead of this :point_down:
e = Entry.objects.get(id=10)
e.comments_on = False
e.save() # Do this :point_down: 
Entry.objects.filter(id=10).update(comments_on=False)

```
`Note:` Finally, realize that update() does an update at the SQL level and, thus, does not call any `save()` methods on your models, 
nor does it emit the `pre_save` or `post_save` signals

#### delete()
Performs an SQL delete query on all rows in the QuerySet and returns the number of objects deleted and a dictionary with the 
number of deletions per object type.
The `delete()` method does a bulk delete and does not call any `delete()` methods on your models. It does, however, emit the 
`pre_delete` and `post_delete` signals for all deleted objects (including cascaded deletions).

#### explain(format=None, **options)
Returns a string of the QuerySet’s execution plan, which details how the database would execute the query, including any indexes 
or joins that would be used. Knowing these details may help you improve the performance of slow queries.
```shell
>>> print(Blog.objects.filter(title='My Blog').explain())
Seq Scan on blog  (cost=0.00..35.50 rows=10 width=12)
  Filter: (title = 'My Blog'::bpchar)
```