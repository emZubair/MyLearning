from django.urls import include, path

app_name = 'edx'


urlpatterns = [
    path('chat/', include('edx.chat.urls', namespace='chat')),
    path('courses/', include('edx.courses.urls', namespace='courses')),
    path('students/', include('edx.student.urls', namespace='student')),
    path('courses/api/', include('edx.courses.api.urls', namespace='courses_api')),
]
