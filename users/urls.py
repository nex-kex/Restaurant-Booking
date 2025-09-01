from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views
from .apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    # Registration
    path("register/", views.RegisterView.as_view(), name="register"),
    # Login, logout
    path("login/", views.CustomLoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="booking:main"), name="logout"),
    # Users list, details
    path("", views.UserListView.as_view(), name="user-list"),
    path("<int:pk>/", views.UserDetailView.as_view(), name="user-detail"),
    # User update
    path("<int:pk>/update/", views.UserUpdateView.as_view(), name="user-update"),
    path("<int:pk>/update/password/", views.UserUpdatePasswordView.as_view(), name="password-update"),
    # Password reset
    path("<int:pk>/update/password/<str:token>/", views.UserUpdatePasswordView.as_view(), name="password-reset"),
    path("new_password/", views.UserForgotPassword.as_view(), name="new-password-request"),
    path("email_notification/", views.EmailNotification.as_view(), name="email-notification"),
]
