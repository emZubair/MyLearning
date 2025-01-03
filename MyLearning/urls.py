"""MyLearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static

from prac_models.admin import event_admin_site
from blog.blog_app.sitemaps import PostSiteMap
from edx.courses.views import CourseListView

sitemaps = {
    'posts': PostSiteMap
}

# path('bookmarks/', include('bookmarks.urls', namespace='bookmarks')),
urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('admin/', admin.site.urls),
    path('admin2/', event_admin_site.urls),
    path('blog/', include('blog.urls', namespace='blog')),

    path('edx/', include('edx.urls', namespace='edx')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.view.sitemap')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
