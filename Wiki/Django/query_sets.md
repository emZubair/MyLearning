## Query sets
A QuerySet represents a collection of objects from your database. QuerySets are lazy – the act of creating a 
QuerySet doesn’t involve any database activity and Django won’t actually run the query until the QuerySet is evaluated.
Query sets can be limited i.e `A.objects.all()[:5]` 

You can execute a queryset by `iteration`, `repr()`, `len()`, `bool()` using queryset in if statement, 
If there is at least one result, the QuerySet is True, otherwise False 
`NOTE`: If you only need to determine the number of records in the set (and don’t need the actual objects), 
it’s much more efficient to handle a count at the database, Django provides a `count()` method for precisely 
this reason. `Entry.objects.count()` or `Entry.objects.filter(headline__contains='Lennon').count()`


Slicing an unevaluated QuerySet usually returns another unevaluated QuerySet modifying it further 
(e.g., adding more filters, or modifying ordering) is not allowed, but Django will execute the database 
query if you use the “step” parameter of slice syntax, and will return a list. 

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

### Caching and QuerySets
Each QuerySet contains a cache to minimize database access, The first time a QuerySet is evaluated – and, hence, a 
database query happens – Django saves the query results in the QuerySet’s cache and returns the results that have been 
explicitly requested (e.g., the next element, if the QuerySet is being iterated over). 

Limiting the queryset using an array slice or an index will not populate the cache. However, if the entire queryset 
has already been evaluated, the cache will be checked instead:

```shell
>>> queryset = Entry.objects.all()
>>> [entry for entry in queryset] # Queries the database
>>> print(queryset[5]) # Uses cache
>>> print(queryset[5]) # Uses cache
```

### Filters
Filters narrow down the query results based on the given parameters. `filter(**kwargs)` Returns a new QuerySet containing 
objects that match the given lookup parameters. Keyword argument queries – in `filter()`, are `“AND”ed` together
`exclude(**kwargs)` Returns a new QuerySet containing objects that do not match the given lookup parameters.
You can chain (refine) multiple filters, Each time you refine a QuerySet, you get a brand-new QuerySet that is in no 
way bound to the previous QuerySet.

For multivalued relationships, everything inside a single filter is applied simultaneously to filter out items 
matching all those requirements. Successive filter() calls further restrict the set of objects, but for multi-valued 
relations, they apply to any object linked to the primary model, not necessarily those objects that were 
selected by an earlier filter() call.

#### Complex lookups with Q objects
A Q object (django.db.models.Q) is an object used to encapsulate a collection of keyword arguments. Q objects can be
combined using the `& and | operators`. When an operator is used on two Q objects, it yields a new Q object.
`Q(question__startswith='Who') | Q(question__startswith='What')` Q objects can be negated using the ~ operator, 
allowing for combined lookups that combine both a normal query and a negated (NOT) query
`Q(question__startswith='Who') | ~Q(pub_date__year=2005)`
 If you provide multiple Q object arguments to a lookup function, the arguments will be “AND”ed together. 
```shell
Poll.objects.get(
    Q(question__startswith='Who'),
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
)
// translates to 
SELECT * from polls WHERE question LIKE 'Who%'
    AND (pub_date = '2005-05-02' OR pub_date = '2005-05-06')

```

Lookup functions can mix the use of Q objects and keyword arguments. All arguments provided to a lookup function 
(be they keyword arguments or Q objects) are “AND”ed together. However, if a Q object is provided, it must precede 
the definition of any keyword arguments.

Calling `.delete` on Queryset, method immediately deletes the object and returns the number of objects deleted 
and a dictionary with the number of deletions per object type. When Django deletes an object, by default it 
emulates the behavior of the SQL constraint `ON DELETE CASCADE` – in other words, any objects which had foreign keys 
pointing at the object to be deleted will be deleted along with it.

Note that delete() is the only QuerySet method that is not exposed on a Manager itself. This is a safety mechanism 
to prevent you from accidentally requesting `Entry.objects.delete()`, and deleting all the entries. If you do want to 
delete all the objects, then you have to explicitly request a complete query set: `Entry.objects.all().delete()`
#### New Instances 
it is possible to easily create new instance with all fields’ values copied. In the simplest case, you can set `pk to 
None and _state.adding to True`.
```shell
blog = Blog(name='My blog', tagline='Blogging is easy')
blog.save() # blog.pk == 1

blog.pk = None
blog._state.adding = True
blog.save() # blog.pk == 2
```
#### Updating multiple objects at once
The only restriction on the QuerySet being updated is that it can only access one database table: the model’s 
main table.
```shell
# Update all the headlines with pub_date in 2007.
Entry.objects.filter(pub_date__year=2007).update(headline='Everything is the same')
```
Be aware that the `update()` method is converted directly to an SQL statement. It is a bulk operation for direct updates. 
It doesn’t run any `save()` methods on your models, or emit the `pre_save` or `post_save` signals
When you use `F()` objects in an update – you can only reference fields local to the model being updated
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
For example in the example below, the authors will be grouped by name, so you will only get an annotated result 
for each unique author name. This means if you have two authors with the same name, their results will be merged 
into a single result in the output of the query; the average will be computed as the average over the 
books written by both authors.
```shell
>>> Author.objects.values('name').annotate(average_rating=Avg('book__rating'))
```

It’s difficult to intuit how the ORM will translate complex querysets into SQL queries so when in doubt, 
inspect the SQL with `str(queryset.query)` and write plenty of tests

#### order_by()
QuerySet are ordered by the ordering tuple given by the ordering option in the model’s Meta. 
You can override this on a per-QuerySet basis by using the order_by method. To order randomly, use "?",
`Entry.objects.order_by('?')`, it might be slow though. 

Django will use the default ordering on the related model, or order by the related model’s primary key
if there is no `Meta.ordering` specified.
`Entry.objects.order_by(Coalesce('summary', 'headline').desc())`

There’s no way to specify whether ordering should be case sensitive, You can order by a field converted to 
lowercase with Lower which will achieve case-consistent ordering: `Entry.objects.order_by(Lower('headline').desc())`

If you don’t want any ordering to be applied to a query, not even the default ordering, 
call `order_by()` with no parameters, You can tell if a query is ordered or not by checking the 
`QuerySet.ordered` attribute, which will be True if the QuerySet has been ordered in any way.

`asc()` and `desc()` have arguments (nulls_first and nulls_last) that control how null values are sorted.

`values()` when values is used with annotate, Instead of returning an annotated result 
for each result in the original `QuerySet`, the original results are grouped according to the unique 
combinations of the fields specified in the `values()` clause. If the `values()` clause is applied after the 
`annotate()` clause, you need to explicitly include the aggregate column in `values()`.

Each order_by() call will clear any previous ordering. For example, this query will be ordered by 
pub_date and not headline: `Entry.objects.order_by('headline').order_by('pub_date')`


### F() expressions
When Django encounters an instance of F(), it overrides the standard Python operators to create an 
encapsulated SQL expression, which make it possible to perform operation on DB level instead of pulling object from 
DB to python memory.

### alias()
Same as annotate(), but instead of annotating objects in the QuerySet, saves the expression for later reuse with 
other QuerySet methods. This is useful when the result of the expression itself is not needed but it is used for 
filtering, ordering, or as a part of a complex expression.
```shell
>>> from django.db.models import Count
>>> blogs = Blog.objects.alias(entries=Count('entry')).filter(entries__gt=5)
```

alias() allows building complex expressions incrementally, possibly spanning multiple methods and modules, 
refer to the expression parts by their aliases and only use annotate() for the final result.