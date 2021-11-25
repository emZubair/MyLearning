from django.contrib import admin
# from django.contrib.auth.models import User, Group
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published', 'status', 'slug')
    list_filter = ('author', 'published', 'status')
    search_fields = ('title', 'body')
    raw_id_fields = ('author', )
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published'
    ordering = ('status', 'published')

# admin.site.unregister(User)
# admin.site.unregister(Group)
