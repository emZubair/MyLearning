from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from taggit.managers import TaggableManager


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
    likes = models.PositiveIntegerField(default=0)

    tags = TaggableManager()
    objects = models.Manager()
    publisher = PublishedManager()

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title

    def increment_likes(self):
        self.likes += 1

    def decrement_likes(self):
        if self.likes > 0:
            self.likes -= 1

    def get_absolute_url(self):
        return reverse('blog:posts:post_details', args=[
            self.published.year, self.published.month, self.published.day, self.slug
        ])


class Comment(models.Model):
    """
    Commented related a specific Post
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=64)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'A comment by {self.name} on {self.post}'
