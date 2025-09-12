import os
from datetime import datetime, timedelta

from django.db import models
from dotenv import load_dotenv

from users.models import CustomUser
from users.validators import validate_phone_number

load_dotenv(override=True)


class Category(models.Model):
    """Класс для описания отдельных категорий столиков."""

    name = models.CharField(max_length=30, verbose_name="Название")
    description = models.CharField(max_length=150, verbose_name="Описание")
    comment = models.CharField(max_length=150, blank=True, null=True, verbose_name="Дополнительные комментарии")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Table(models.Model):
    """Класс для описания отдельных столов ресторана."""

    seats = models.PositiveSmallIntegerField(verbose_name="Количество мест")
    price = models.IntegerField(verbose_name="Цена бронирования")
    time_open = models.TimeField(
        default=datetime.strptime(os.getenv("TIME_OPEN", "00:00:00"), "%H:%M:%S").time(),
        verbose_name="Время начала бронирования",
    )
    time_close = models.TimeField(
        default=datetime.strptime(os.getenv("TIME_CLOSE", "00:00:00"), "%H:%M:%S").time(),
        verbose_name="Время окончания бронирования",
    )
    comment = models.TextField(blank=True, null=True, verbose_name="Дополнительные комментарии")
    is_available = models.BooleanField(default=True, verbose_name="Доступен для бронирования")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="tables", verbose_name="Категория"
    )

    def __str__(self):
        return f"Стол номер {self.id}"

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"
        ordering = ["-price"]


class Booking(models.Model):
    """Класс для описания отдельной брони."""

    statuses = [("active", "Активна"), ("success", "Проведена"), ("cancelled", "Отменена")]

    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="bookings", verbose_name="Стол")
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name="user_bookings", verbose_name="Пользователь"
    )
    status = models.CharField(max_length=9, choices=statuses, default="active", verbose_name="Статус")
    people = models.SmallIntegerField(verbose_name="Количество персон")
    date = models.DateTimeField(verbose_name="Дата и время брони")
    duration = models.TimeField(default=timedelta(hours=1), verbose_name="Продолжительность брони")

    def __str__(self):
        return (
            f"Бронирование номер {self.id} на {self.date.strftime('%d.%m.%Y %H:%M:%S')} "
            f"пользователем с номером {self.user.phone_number}"
        )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["date"]


class Feedback(models.Model):
    """Класс для описания сообщений обратной связи."""

    name = models.CharField(max_length=50, verbose_name="Имя")
    phone_number = models.CharField(max_length=11, validators=[validate_phone_number], verbose_name="Номер телефона")
    text = models.TextField(verbose_name="Сообщение")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    is_solved = models.BooleanField(default=False, verbose_name="Обработана")

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"
        ordering = ["created_at"]
