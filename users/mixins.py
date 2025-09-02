from django import forms

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
