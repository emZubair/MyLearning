from django.urls import reverse_lazy
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from .models import Post

class LatestPostFeed(Feed):
    title = 'ZeeBlog'
    link = reverse_lazy('blog:posts:post_list')
    description = 'New post of my Blog'

    def items(self):
        return Post.publisher.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
