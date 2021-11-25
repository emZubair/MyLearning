from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    """Publisher manager to support custom functionality"""

    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'DRAFT'),
        ('published', 'PUBLISHED')
    )
    title = models.CharField(max_length=64)
    body = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=64, unique_for_date='published')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    published = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()
    publisher = PublishedManager()

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:posts:post_details', args=[
            self.published.year, self.published.month, self.published.day, self.slug
        ])
