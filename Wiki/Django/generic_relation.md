#### Generic Relation (ContentType)
You need three different fields to set up a generic relation
- `content_type`: A `ForeignKey` field to the ContentType model
- `object_id`: A `PositiveIntegerField` to store the primary key of the related object
- `item`: A `GenericForeignKey` field to the related object combining the two previous fields

```shell
class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
```
Only the content_type and object_id fields have a corresponding column in the database table of this model