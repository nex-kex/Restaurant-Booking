from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True, verbose_name="Номер телефона", help_text="87777777777")
    email = models.EmailField(unique=True, verbose_name="Email", help_text="my_email@mail.com")
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Имя", help_text="Иван")
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Фамилия", help_text="Иванов")

    token = models.CharField(max_length=100, blank=True, null=True, verbose_name="Токен")
    reset_password_token = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Токен для восстановления пароля"
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
