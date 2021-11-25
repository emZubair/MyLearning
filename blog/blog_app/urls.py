from django.urls import path

from .views import post_list, post_details, default_pager

app_name = "posts"

urlpatterns = [
    path('', post_list, name='post_list'),
    path('<msg>/default', default_pager, name='defaulter'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', post_details, name='post_details'),
]
