from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.mixins import FormControlMixin, PhoneNumberMixin

from .models import CustomUser


class CustomUserCreationForm(FormControlMixin, PhoneNumberMixin, UserCreationForm):
    """Форма для создания / регистрации пользователя."""

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("phone_number", "email", "first_name", "last_name", "password1", "password2")
        extra_kwargs = {
            "phone_number": {"required": True},
            "email": {"required": True},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "password1": {"write_only": True},
            "password2": {"write_only": True},
        }
        widgets = {"phone_number": forms.TextInput(attrs={"title": "Введите 11 цифр без дополнительных символов."})}

    @staticmethod
    def beautify_phone_number(pn):
        """Форматирование номера телефона в читаемый вид формата +7 (777) 777-77-77."""
        return f"+7 ({pn[1:4]}) {pn[4:7]}-{pn[7:9]}-{pn[9:]}"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.beautify_phone_number(user.phone_number)
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
