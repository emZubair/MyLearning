from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (StudentRegistrationView, StudentEnrollView, StudentCourseListView,
                    StudentCourseDetailsView)


app_name = 'student'

urlpatterns = [
    path('enroll-course/', StudentEnrollView.as_view(), name='student_enroll_course'),
    path('register/', StudentRegistrationView.as_view(), name='student_registration'),

    path('courses/', StudentCourseListView.as_view(), name='student_course_list'),
    path('course/<pk>/', cache_page(60*15)(StudentCourseDetailsView.as_view()), name='student_course_details'),
    path('course/<pk>/<module_id>/', cache_page(60*15)(StudentCourseDetailsView.as_view()),
         name='student_course_detail_module'),

]
