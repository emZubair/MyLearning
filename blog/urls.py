from django.urls import include, path

app_name = 'blog'

urlpatterns = [
    path('post/', include(('blog.blog_app.urls', 'posts')))
]
