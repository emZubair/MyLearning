from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post


@receiver(m2m_changed, sender=Post.likes)
def users_likes_changed(sender, instance, **kwargs):
    instance.likes = instance.likes.count()
    instance.save()
