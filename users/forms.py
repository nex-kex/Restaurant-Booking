from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.mixins import FormControlMixin, PhoneNumberMixin

from .models import CustomUser


class CustomUserCreationForm(FormControlMixin, PhoneNumberMixin, UserCreationForm):
    """Форма для создания / регистрации пользователя."""

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("phone_number", "email", "first_name", "last_name", "password1", "password2")
        extra_kwargs = {
            "phone_number": {"required": True, "placeholder": "87771234567"},
            "email": {"required": True},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "password1": {"write_only": True},
            "password2": {"write_only": True},
        }
        widgets = {
            "phone_number": forms.TextInput(
                attrs={"title": "Введите 11 цифр без дополнительных символов.", "placeholder": "87771234567"}
            ),
            "email": forms.TextInput(attrs={"placeholder": "my_email@mail.com"}),
            "first_name": forms.TextInput(attrs={"placeholder": "Иван"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Иванов"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.phone_number
        if commit:
            user.save()
        return user


class UserEditForm(FormControlMixin, PhoneNumberMixin, forms.ModelForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("phone_number", "email", "first_name", "last_name")


class PasswordEditForm(FormControlMixin, UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ()


class LoginForm(FormControlMixin, AuthenticationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("phone_number", "password")
