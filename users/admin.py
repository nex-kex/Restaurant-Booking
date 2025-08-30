from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["phone_number", "email", "first_name", "last_name"]
    ordering = ["first_name", "last_name"]
    search_fields = ["phone_number", "email", "first_name", "last_name"]
