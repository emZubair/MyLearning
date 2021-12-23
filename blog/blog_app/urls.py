from django.urls import path
from django.contrib.sitemaps.views import sitemap

from .views import (post_list, post_details, default_pager, PostListView, share_post,
                    post_search, like_post, list_users, user_details, follow_user, popular_posts)
from .sitemaps import PostSiteMap
from .feeds import LatestPostFeed

app_name = "posts"


sitemaps = {
    'posts': PostSiteMap
}


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('feed/', LatestPostFeed(), name='post_feed'),
    path('like/', like_post, name='like_post'),
    path('search/', post_search, name='total_posts'),
    path('popular/', popular_posts, name='popular_post'),
    path('<msg>/default', default_pager, name='defaulter'),
    path('<int:post_id>/share', share_post, name='share_post'),
    path('tag/<slug:tag_slug>', post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', post_details, name='post_details'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('list_users', list_users, name='list_users'),
    path('follow_user/', follow_user, name='follow_user'),
    path('<username>/', user_details, name='user_details'),
]
