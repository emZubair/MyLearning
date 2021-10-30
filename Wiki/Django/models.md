## Models
Each model has at least one Manager, and it’s called objects by default.
By default, Django gives each model an auto-incrementing primary key with the type specified per app in 
`AppConfig.default_auto_field` or globally in the `DEFAULT_AUTO_FIELD` setting which defaults to `'django.db.models.AutoField'`
```shell
from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
```

Table level methods are written in manager class while row level methods are written in model.
#### Model.refresh_from_db(using=None, fields=None)
If you need to reload a model’s values from the database, you can use the `refresh_from_db()` method, calling it with no fields updates 
all the non-deferred values from the database and refills the cache after clearing it.
#### get_absolute_url()
This tells Django how to calculate the URL for an object. Django uses this in its admin interface, and any time it needs 
to figure out a URL for an object.
#### save(self, *args, **kwargs)
Can be overridden by a model to change the default change behaviour for an object. If you use `*args`, `**kwargs` in your 
method definitions, you are guaranteed that your code will automatically support the arguments added in future release of Django.
### Meta options
Model metadata is `“anything that’s not a field”`, such as ordering options `(ordering)`, database table name `(db_table)`, 
or human-readable singular and plural names (verbose_name and verbose_name_plural). Following options can be set using `Meta`

`app_label` If a model is defined outside of an application in INSTALLED_APPS, it must declare which app it belongs to
`db_table` It is strongly advised that you use lowercase table names when you override the table name
`default_related_name` The name that will be used by default for the relation from a related object back to this one. 
The default is `<model_name>_set`.
`verbose_name` A human-readable name for the object, singular: `verbose_name = "pizza"`
`verbose_name_plural` The plural name for the object: `verbose_name_plural = "stories"`
`managed` Django will create the appropriate database tables in migrate or as part of migrations and remove them as part of a 
flush management command. That is, Django manages the database tables’ lifecycles.
`default_permissions` Defaults to ('add', 'change', 'delete', 'view'). You may customize this list, for example, 
by setting this to an empty list if your app doesn’t require any of the default permissions.
`permissions` Extra permissions to enter into the permissions table when creating this object. Add, change, delete, and view 
permissions are automatically created for each model. `permissions = [('can_deliver_pizzas', 'Can deliver pizzas')]`
This is a list or tuple of 2-tuples in the format `(permission_code, human_readable_permission_name)`.
`indexes` A list of indexes that you want to define on the model:
`unique_together` Sets of field names that, taken together, must be unique, This is a list of lists that must be unique when 
considered together: `unique_together = [['driver', 'restaurant']]`
`constraints` A list of constraints that you want to define on the model:
```shell
from django.db import models

class Customer(models.Model):
    age = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(age__gte=18), name='age_gte_18'),
        ]
```






