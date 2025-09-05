from django.contrib import admin

from .models import Booking, Category, Table, Feedback


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ["id", "price", "seats", "category", "is_available"]
    list_filter = ["category", "is_available"]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "table", "date", "status"]
    search_fields = ["user"]
    list_filter = ["status", "table"]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "phone_number", "is_solved", "text"]
    search_fields = ["text"]
    list_filter = ["is_solved"]
