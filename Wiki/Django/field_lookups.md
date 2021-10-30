### Field lookups
Field lookups are how you specify the meat of an SQL WHERE clause. They’re specified as keyword arguments to the QuerySet 
methods `filter()`, `exclude()` and `get()`.

As a convenience when no lookup type is provided (like in `Entry.objects.get(id=14)`) the lookup type is assumed to be `exact`.

#### exact
Exact match. If the value provided for comparison is `None`, it will be interpreted as an SQL `NULL`
`Entry.objects.get(id__exact=None)`

#### iexact
Case-insensitive exact match. 

#### contains, icontains
Case-sensitive and Case-insensitive containment test respectively SQL equivalent is `LIKE`

#### in
In a given iterable; often a list, tuple, or queryset. It’s not a common use case, but strings (being iterables) are accepted

`gt` is `greater than`, `gte` is Greater than or equal to, `lt` is less than, `lte` less than or equal to, `startswith`, `istartswith`,
`endswith`, `iendswith`, `range` Range test (inclusive),

`date` For datetime fields, casts the value as date. Allows chaining additional field lookups. Takes a date value.
`year` For date and datetime fields, an exact year match. Allows chaining additional field lookups. Takes an integer year.
`month`, `day`, `week` return the week number (1-52 or 53), `week_day` Takes an integer value representing the day of week from 1 (Sunday) to 7 (Saturday).
`quarter` For date and datetime fields, a ‘quarter of the year’ match, Takes an integer value between 1 and 4 representing the quarter of the year.
`time` For datetime fields, casts the value as time. `hour` takes 0-23, `minute` 0-59, `second` 0-59,

```shell
Entry.objects.get(headline__icontains='Lennon')
Entry.objects.filter(id__in=[1, 3, 4])
Entry.objects.filter(headline__in='abc')
Entry.objects.filter(id__gt=4)
Entry.objects.filter(headline__startswith='Lennon')
Entry.objects.filter(headline__endswith='Lennon')
Entry.objects.filter(pub_date__range=(start_date, end_date))

Entry.objects.filter(pub_date__date__gt=datetime.date(2005, 1, 1))
Entry.objects.filter(pub_date__year__gte=2005)
Entry.objects.filter(pub_date__quarter=2)

```

#### isnull
Takes either True or False, which correspond to SQL queries of IS NULL and IS NOT NULL, respectively.
`Entry.objects.filter(pub_date__isnull=True)`

#### regex, iregex
Case-sensitive regular expression match. `Entry.objects.get(title__regex=r'^(An?|The) +')`