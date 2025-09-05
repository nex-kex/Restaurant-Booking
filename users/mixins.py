from django import forms
from django.core.exceptions import PermissionDenied

from .validators import validate_phone_number


class FormControlMixin:
    """Миксин для форматирования полей ввода."""

    def __init__(self, *args, **kwargs):
        super(FormControlMixin, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-control"})


class PhoneNumberMixin:
    """Миксин для добавления валидации номера телефона в формы."""

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        return validate_phone_number(phone_number)


class StaffRequiredMixin:
    """Миксин для проверки staff статуса."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("У вас нет прав для выполнения этого действия")
        return super().dispatch(request, *args, **kwargs)


class PersonalDataMixin:
    """Миксин для проверки прав на доступ к данным о других пользователях."""
    def get_object(self, **kwargs):
        user_profile = super().get_object()
        user = self.request.user
        if not user.is_staff:
            if user != user_profile:
                raise PermissionDenied("У вас нет прав для доступа к этой странице.")
        return user_profile
