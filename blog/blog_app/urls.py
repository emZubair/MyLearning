from django.urls import path

from .views import post_list, post_details, default_pager, PostListView, share_post

app_name = "posts"


# path('', post_list, name='post_list'),
urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<msg>/default', default_pager, name='defaulter'),
    path('<int:post_id>/share', share_post, name='share_post'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', post_details, name='post_details'),
]
