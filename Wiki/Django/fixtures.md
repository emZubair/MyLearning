#### Fixtures
Fixtures are used to dump database data to json files and load data from those json files to db. You can specify the application to 
limit the dump to that application's models i.e
```shell
python manage.py dumpdata courses --indent=2 --output=edx/courses/fixtures/subjects.json
python manage.py loaddata subjects.json
```
By default, django checks for fixture data under `fixture` folder, but you can specify different name in the `loaddata` command or it can be 
set using `FIXTURE_DIRS` in the django project settings.