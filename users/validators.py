from django.core.validators import ValidationError


def validate_phone_number(phone_number):
    """Валидация номера телефона. Проверяет, что номер состоит только из цифр и имеет длину 11 символов."""

    if not phone_number:
        return phone_number

    if str(phone_number[0]) not in ["7", "8"]:
        raise ValidationError("Номер телефона должен начинаться с 7 или 8.")

    if not phone_number.isdigit():
        raise ValidationError("Номер телефона должен содержать только цифры.")

    if len(phone_number) != 11:
        raise ValidationError("Номер телефона должен состоять из 11 цифр.")

    return phone_number
