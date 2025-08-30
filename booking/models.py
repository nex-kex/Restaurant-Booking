import os
from datetime import datetime, timedelta

from django.db import models
from dotenv import load_dotenv

from users.models import CustomUser

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
        default=datetime.strptime(os.getenv("TIME_OPEN"), "%H:%M:%S").time(), verbose_name="Время начала бронирования"
    )
    time_close = models.TimeField(
        default=datetime.strptime(os.getenv("TIME_CLOSE"), "%H:%M:%S").time(),
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
        ordering = ["price"]


class Booking(models.Model):
    """Класс для описания отдельной брони."""

    statuses = [("active", "Активна"), ("success", "Проведена"), ("cancelled", "Отменена")]

    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="bookings", verbose_name="Стол")
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name="user_bookings", verbose_name="Пользователь"
    )
    status = models.CharField(max_length=9, choices=statuses, default=statuses[0], verbose_name="Статус")
    people = models.SmallIntegerField(verbose_name="Количество персон")
    date = models.DateTimeField(verbose_name="Дата и время брони")
    duration = models.TimeField(default=timedelta(hours=1), verbose_name="Продолжительность брони")

    def __str__(self):
        return f"Бронь на {self.date} пользователем {self.user}"

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"
        ordering = ["status", "date"]
