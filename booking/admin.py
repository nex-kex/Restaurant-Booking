from django.contrib import admin

from .models import Booking, Category, Table


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ["price", "seats", "category", "is_available"]
    list_filter = ["category", "is_available"]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["user", "table", "date", "status"]
    search_fields = ["user"]
    list_filter = ["status", "table"]
