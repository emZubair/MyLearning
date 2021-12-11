from django.urls import path, include
from .account.views import dashboard


app_name = 'bookmarks'

urlpatterns = [
    path('account/', include('bookmarks.account.urls', namespace='account')),
]
