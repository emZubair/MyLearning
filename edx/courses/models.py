from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string

from .fields import OrderField


class Subject(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)

    class Meta:
        ordering = ['id',]

    def __str__(self):
        return self.title


class Course(models.Model):
    author = models.ForeignKey(User, related_name='courses_created',
                               on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order} {self.title}'


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE,
                               limit_choices_to={'model__in': ('text', 'video', 'file', 'image')})
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    author = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def render(self):
        return render_to_string(f'courses/content/{self._meta.model_name}.html', {'item': self})

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()

    def __str__(self):
        return f"Text type:{self.title}"


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    image = models.ImageField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()
