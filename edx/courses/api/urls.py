from django.urls import path, include
from rest_framework import routers

from .views import (SubjectListView, SubjectDetailsView, CourseEnrollView, CourseListView)

router = routers.DefaultRouter()
router.register('courses', CourseListView)

app_name = 'courses_api'

urlpatterns = [
    path('', include(router.urls)),
    path('subjects/', SubjectListView.as_view(), name='subject_list'),
    path('subjects/<pk>/', SubjectDetailsView.as_view(), name='subject_details'),
]
# path('subject/<pk>/enroll/', CourseEnrollView.as_view(), name='course_enroll'),
