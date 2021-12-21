from django.urls import path, include
from .account.views import dashboard


app_name = 'bookmarks'

urlpatterns = [
    path('account/', include('bookmarks.account.urls', namespace='account')),
    path('images/', include('bookmarks.images.urls', namespace='images')),
]
# 127.0.0.1:8000/images/create/?title=%20Django%20and%20Duke&url=https://upload.wikimedia.org/wikipedia/commons/8/85/Django_Reinhardt_and_Duke_Ellington_%28Gottlieb%29.jpg