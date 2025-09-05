import os
import secrets

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from booking.models import Booking
from .forms import (CustomUserCreationForm, LoginForm, PasswordEditForm,
                    UserEditForm)
from .models import CustomUser


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    form_class = LoginForm


class LogoutView(LoginRequiredMixin, View):
    template_name = "users/logout.html"
    next_page = reverse_lazy("booking:main")


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("booking:main")

    def form_valid(self, form):
        user = form.save()
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/user_detail.html"

    # Список бронирований отдельного пользователя
    def get_context_data(self, **kwargs):
        user = self.object
        context = super().get_context_data(**kwargs)
        context["user_bookings"] = Booking.objects.filter(user=user)
        return context

    # Запрещает обычному пользователю просматривать чужие профили
    def get_object(self, **kwargs):
        user_profile = super().get_object()
        user = self.request.user
        if not user.is_staff:
            if user != user_profile:
                raise PermissionDenied("У вас нет прав для доступа к этой странице.")
        return user_profile


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser

    # Запрещает обычному пользователю просматривать чужие профили
    def get_queryset(self, **kwargs):
        user = self.request.user
        if not user.is_staff:
            raise PermissionDenied("У вас нет прав для доступа к этой странице.")
        return CustomUser.objects.all()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "users/user_form.html"
    form_class = UserEditForm

    def get_success_url(self):
        return reverse_lazy("users:user-detail", kwargs={"pk": self.object.pk})

    # Запрещает обычному пользователю изменять чужие профили
    def get_object(self, **kwargs):
        user_profile = super().get_object()
        user = self.request.user
        if not user.is_staff:
            if user != user_profile:
                raise PermissionDenied("У вас нет прав для доступа к этой странице.")
        return user_profile


class UserUpdatePasswordView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "users/user_form.html"
    form_class = PasswordEditForm
    success_url = reverse_lazy("booking:main")

    def get_object(self, **kwargs):

        # Запрещает любому пользователю изменять чужие профили
        user_profile = super().get_object()
        user = self.request.user
        if user != user_profile:
            raise PermissionDenied("У вас нет прав для доступа к этой странице.")

        if "reset_password_token" in self.kwargs:
            user = get_object_or_404(
                CustomUser, pk=self.kwargs["pk"], reset_password_token=self.kwargs["reset_password_token"]
            )
            return user

        return user_profile

    def form_valid(self, form):
        if "token" in self.kwargs:
            user = form.instance
            user.reset_password_token = None
            user.set_password(form.cleaned_data["password1"])
            user.save()

        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response

    def get_success_url(self):
        return reverse_lazy("booking:main")


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy("booking:main")

    # Запрещает обычному пользователю удалять профили
    def get_object(self, **kwargs):
        user = self.request.user
        if not user.is_staff:
            raise PermissionDenied("У вас нет прав для доступа к этой странице.")
        return super().get_object()


class EmailNotification(TemplateView):
    template_name = "users/email_notification.html"


class UserForgotPassword(View):
    template_name = "users/forgotten_password.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")

        # Если такого пользователя нет в системе, перенаправляет на регистрацию
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return redirect("users:register")

        token = secrets.token_hex(16)
        user.reset_password_token = token
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/users/{user.pk}/update/password/{token}"

        self._send_reset_password_email(user.email, url)

        return redirect("users:email-notification")

    def _send_reset_password_email(self, email, url):
        subject = "Восстановление пароля"
        message = f"Для восстановления пароля перейдите по ссылке: {url}"
        send_mail(subject, message, os.getenv("EMAIL_HOST_USER"), [email])
