from django.apps import AppConfig


class BlogAppConfig(AppConfig):
    name = 'blog.blog_app'
    verbose_name = 'Posts Application'

    def ready(self):
        import blog.blog_app.signals
