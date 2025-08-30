from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, email, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Необходимо указать номер телефона")
        if not email:
            raise ValueError("Необходимо указать номер email")

        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, email, password, **extra_fields)


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
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
