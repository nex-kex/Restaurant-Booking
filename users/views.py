import os
import secrets

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .forms import (CustomUserCreationForm, LoginForm, PasswordEditForm,
                    UserEditForm)
from .models import CustomUser


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    form_class = LoginForm


class LogoutView(View):
    template_name = "users/logout.html"
    next_page = reverse_lazy("booking:main")


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("booking:main")


class UserDetailView(DetailView):
    model = CustomUser
    template_name = "users/user_detail.html"


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser


class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = "users/user_form.html"
    form_class = UserEditForm
    success_url = reverse_lazy("booking:main")


class UserUpdatePasswordView(UpdateView):
    model = CustomUser
    template_name = "users/user_form.html"
    form_class = PasswordEditForm
    success_url = reverse_lazy("booking:main")

    def get_object(self, queryset=None):
        # Если есть токен в URL - восстановления пароля
        if "token" in self.kwargs:
            user = get_object_or_404(CustomUser, pk=self.kwargs["pk"], reset_password_token=self.kwargs["token"])
            return user
        return super().get_object(queryset)

    def form_valid(self, form):
        if "token" in self.kwargs:
            user = form.instance
            user.reset_password_token = None
            user.save()
        return super().form_valid(form)


class UserDeleteView(DeleteView):
    model = CustomUser
    success_url = reverse_lazy("booking:main")


class EmailNotification(TemplateView):
    template_name = "users/email_notification.html"


class UserForgotPassword(View):
    template_name = "users/forgotten_password.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return redirect("users:register")

        token = secrets.token_hex(16)
        user.reset_password_token = token
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/users/{user.pk}/reset_password/{token}"

        self._send_reset_password_email(user.email, url)

        return redirect("users:email_notification")

    def _send_reset_password_email(self, email, url):
        subject = "Восстановление пароля"
        message = f"Для восстановления пароля перейдите по ссылке: {url}"
        send_mail(subject, message, os.getenv("EMAIL_HOST_USER"), [email])
