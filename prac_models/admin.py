from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Publisher, Author, Book, Store

admin.site.register(Book)
admin.site.register(Store)
admin.site.register(Author)
admin.site.register(Publisher)

admin.site.site_header = "MyLearning Admin"
admin.site.site_title = "MyLearning Admin Portal"
admin.site.index_title = "Welcome to MyLearning Researcher Portal"


class BookAdminSite(AdminSite):
    site_header = "Book Admin"
    site_title = "Book Admin Portal"
    index_title = "Welcome to Book Researcher Portal"


event_admin_site = BookAdminSite(name='book_admin')


event_admin_site.register(Book)
