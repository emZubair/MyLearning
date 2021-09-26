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
Book will have a database table named bookstore_book.
```
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