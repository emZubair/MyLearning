from django.urls import path

from .views import course_chat_room

app_name = 'chat'

urlpatterns = [
    path('<int:course_id>/', course_chat_room, name='course_chat_room'),
]
