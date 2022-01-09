from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import (CourseCreateView, CourseUpdateView, CourseDeleteView, ManageCourseListView,
                    CourseModuleUpdateView, ContentCreateUpdateView, ContentDeleteView, ModuleContentListView)

app_name = 'courses'

urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),

    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('<pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('<pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('mine/', ManageCourseListView.as_view(), name='manage_course_list'),
    path('<pk>/module/', CourseModuleUpdateView.as_view(), name='course_update_module'),
    path('module/<int:module_id>/content/<model_name>/create/', ContentCreateUpdateView.as_view(),
         name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<id>/', ContentCreateUpdateView.as_view(),
         name='module_content_update'),
    path('content/<int:id>/delete/', ContentDeleteView.as_view(), name='module_content_delete'),
    path('module/<int:module_id>/', ModuleContentListView.as_view(), name='module_content_list'),
]
