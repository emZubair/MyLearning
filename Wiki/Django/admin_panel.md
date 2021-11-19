### Admin Panel

#### Changing Django Site Title
Site header for Django Admin site can be changed by setting site objects attribute in `admin.py file.
```shell
admin.site.site_header = "MyLearning Admin"
admin.site.site_title = "MyLearning Admin Portal"
admin.site.index_title = "Welcome to MyLearning Researcher Portal"
```

Similarly Add/Delete button can be removed writing admin manage for a particular model and overriding the following two methods.
```shell
def has_add_permission(self, request):
    return False

def has_delete_permission(self, request, obj=None):
    return False
```
#### Edit Multiple models
To be able to edit multiple objects from one Django admin, you need to use inlines.
```shell
class VillainInline(admin.StackedInline):
    model = Villain
# Similarly you can also use TabularInline 
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...

    inlines = [VillainInline]
```
You can make fields readonly only once an object is created
```shell
def get_readonly_fields(self, request, obj=None):
    if obj:
        return ["name", "category"]
    else:
        return []
```
`formfield_for_foreignkey` is used to customize foreign key values, `raw_id_fields` is used to show a popup to edit FK objects.
