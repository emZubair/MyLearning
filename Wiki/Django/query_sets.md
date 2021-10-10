## Query sets
A QuerySet represents a collection of objects from your database. QuerySets are lazy – the act of creating a 
QuerySet doesn’t involve any database activity and Django won’t actually run the query until the QuerySet is evaluated.
Query sets can be limited i.e `A.objects.all()[:5]` 

### Saving Foreign Key & ManyToManyFields
You can save object via foreign key relation by assigning respective object and calling save method. i.e 
`book.author = author_1` then `book.save()`. 

For ManyToMany field use add method i.e `book.publishers.add(pub_1)` for multiple objects `book.publishers.add(pub_1, pub_2)`
### Field Lookups
Basic lookups keyword arguments take the form `field__lookuptype=value`. (That’s a double-underscore) in case 
of a ForeignKey you can specify the field name suffixed with _id.

`F expressions` can then be used in query filters to compare the values of two different fields on the same model instance.
You can also use the double underscore notation to span relationships in an F() object.

Lookup types : `exact, iexact, lte, contains, startswith, endswith`
### Filters
Filters narrow down the query results based on the given parameters. `filter(**kwargs)` Returns a new QuerySet containing objects that match the given lookup parameters.
`exclude(**kwargs)` Returns a new QuerySet containing objects that do not match the given lookup parameters.
You can chain (refine) multiple filters, Each time you refine a QuerySet, you get a brand-new QuerySet that is in no 
way bound to the previous QuerySet.

For multivalued relationships, everything inside a single filter is applied simultaneously to filter out items 
matching all those requirements. Successive filter() calls further restrict the set of objects, but for multi-valued 
relations, they apply to any object linked to the primary model, not necessarily those objects that were selected by an earlier filter() call.

### Aggregate
Following are aggregate operations that can be perfomed on a 
queryset. aggregate includes `Sum`, `Avg`, `Count`, `Max`, `Min`
#### Aggregate
`aggregate()` is a terminal clause for a QuerySet that, when invoked, returns a dictionary of name-value pairs.

```shell
>>> from django.db.models import Avg
>>> Book.objects.aggregate(average_price=Avg('price'))
{'average_price': 34.35}
```

#### Annotate
Per-object summaries can be generated using the `annotate()` clause. When an `annotate()` clause is 
specified, each object in the QuerySet will be annotated with the specified values.

```shell
# Build an annotated queryset
>>> from django.db.models import Count
>>> q = Book.objects.annotate(Count('authors'))
# Interrogate the first object in the queryset
>>> q[0]
<Book: The Definitive Guide to Django>
>>> q[0].authors__count
2
```

` Aliasing` can be used in `annotate` and `aggregate`, i.e 
`annotate(average=Avg("price"))` and `aggregate(average=Avg("price"))`. 

`Note`: If aliasing isn't used then name is derived from the expression, the above cases name would 
be `price_avg`. In case of `annotate`, aliased name can be used
in filter expressions.

```shell
>>> Book.objects.annotate(num_authors=Count('authors')).filter(num_authors__gt=1)
```

`Filter & Order by` can be used with type of `aggregate` function, in following expression 
Each Author in the result set will have the num_books and highly_rated_books attributes
```shell
>>> highly_rated = Count('book', filter=Q(book__rating__gte=7))
>>> Author.objects.annotate(num_books=Count('book'), highly_rated_books=highly_rated)
>>> Book.objects.annotate(num_authors=Count('authors')).order_by('num_authors')
```

`values()` when values is used with annotate, Instead of returning an annotated result 
for each result in the original `QuerySet`, the original results are grouped according to the unique 
combinations of the fields specified in the `values()` clause. If the `values()` clause is applied after the 
`annotate()` clause, you need to explicitly include the aggregate column in `values()`.

For example in the example below, the authors will be grouped by name, so you will only get an annotated result 
for each unique author name. This means if you have two authors with the same name, their results will be merged 
into a single result in the output of the query; the average will be computed as the average over the 
books written by both authors.

```shell
>>> Author.objects.values('name').annotate(average_rating=Avg('book__rating'))
```

It’s difficult to intuit how the ORM will translate complex querysets into SQL queries so when in doubt, 
inspect the SQL with `str(queryset.query)` and write plenty of tests

### F() expressions
When Django encounters an instance of F(), it overrides the standard Python operators to create an 
encapsulated SQL expression, which make it possible to perform operation on DB level instead of pulling object from 
DB to python memory.