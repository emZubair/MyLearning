#### distinct()
Returns a new QuerySet that uses SELECT DISTINCT in its SQL query. This eliminates duplicate rows from the query results.
By default, a QuerySet will not eliminate duplicate rows as in a query rarely there is rarely a scenario where duplicate 
records are returned but if your query spans multiple tables, it’s possible to get duplicate results when a QuerySet is evaluated.
If you are using `distinct()` be careful about ordering by related models. Similarly, when using `distinct()` and `values()` together, 
be careful when ordering by fields not in the values() call.

#### values()
Returns a QuerySet that returns dictionaries, rather than model instances, when used as an iterable, each of those dictionaries 
represents an object, with the keys corresponding to the attribute names of model objects. The `values()` method takes optional 
positional arguments, `*fields`, which specify field names to which the SELECT should be limited.
```shell
# This list contains a Blog object.
>>> Blog.objects.filter(name__startswith='Beatles')
<QuerySet [<Blog: Beatles Blog>]>

# This list contains a dictionary.
>>> Blog.objects.filter(name__startswith='Beatles').values()
<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>

>>> Blog.objects.values()
<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>
>>> Blog.objects.values('id', 'name')
<QuerySet [{'id': 1, 'name': 'Beatles Blog'}]>

# The values() method also takes optional keyword arguments, **expressions, which are passed through to annotate():
>>> from django.db.models.functions import Lower
>>> Blog.objects.values(lower_name=Lower('name'))
<QuerySet [{'lower_name': 'beatles blog'}]>
```

#### values_list()
This is similar to values() except that instead of returning dictionaries, it returns tuples when iterated over. Each tuple contains 
the value from the respective field or expression passed into the values_list() call
```shell
>>> Entry.objects.values_list('id', 'headline')
<QuerySet [(1, 'First entry'), ...]>
>>> from django.db.models.functions import Lower
>>> Entry.objects.values_list('id', Lower('headline'))
<QuerySet [(1, 'first entry'), ...]>

# f you only pass in a single field, you can also pass in the flat parameter. If True, this will mean the returned results are 
# single values, rather than one-tuples.

>>> Entry.objects.values_list('id').order_by('id')
<QuerySet[(1,), (2,), (3,), ...]>

>>> Entry.objects.values_list('id', flat=True).order_by('id')
<QuerySet [1, 2, 3, ...]>
# You can pass named=True to get results as a namedtuple():

>>> Entry.objects.values_list('id', 'headline', named=True)
<QuerySet [Row(id=1, headline='First entry'), ...]>
```
It is an error to pass in flat when there is more than one field. If you don’t pass any values to `values_list()`, 
it will return all the fields in the model, in the order they were declared.



