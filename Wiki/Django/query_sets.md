## Query sets

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

It’s difficult to intuit how the ORM will translate complex querysets into SQL queries so when in doubt, 
inspect the SQL with `str(queryset.query)` and write plenty of tests