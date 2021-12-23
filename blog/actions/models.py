from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
    user = models.ForeignKey('auth.User', related_name='actions',
                             db_index=True, on_delete=models.CASCADE)
    details = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    target_tc = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj',
                                  on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_tc', 'target_id')

    class Meta:
        ordering = ('-created',)
