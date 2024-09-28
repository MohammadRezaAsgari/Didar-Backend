from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = [
        "username",
        "phone",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_superuser",
    ]
    list_filter = [
        "is_active",
        "is_superuser",
    ]
    search_fields = ["username", "phone", "email", "first_name", "last_name"]
    list_display_links = ["username", "phone", "email"]


    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {
         "fields": ("first_name", "last_name", "email", "phone")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
