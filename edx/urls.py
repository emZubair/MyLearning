from django.urls import include, path

app_name = 'edx'


urlpatterns = [
    path('courses/', include('edx.courses.urls', namespace='courses')),
    path('students/', include('edx.student.urls', namespace='student')),
]
