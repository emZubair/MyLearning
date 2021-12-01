from django import template
from django.db.models import Count
from blog.blog_app.models import Post
from django.utils.safestring import mark_safe

from markdown import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.publisher.count()


@register.inclusion_tag('blog/post/latest_post.html')
def show_latest_posts(count=5):
    latest_posts = Post.publisher.all().order_by('-published')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.publisher.annotate(comment_count=Count('comments')).order_by('comment_count')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown(text))
