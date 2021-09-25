from django.contrib import admin
from .models import Publisher, Author, Book, Store


admin.site.register(Book)
admin.site.register(Store)
admin.site.register(Author)
admin.site.register(Publisher)
