from django.urls import path
from django.contrib.auth import views as auth_views

from .views import login_user, dashboard, register, edit_user

app_name = 'account'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('edit_profile/', edit_user, name='edit_profile'),
    path('login2/', auth_views.LoginView.as_view(), name='login2'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
