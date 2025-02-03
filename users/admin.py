from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Instructor, User


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
    search_fields = ["username", "phone", "email", "first_name", "last_name", "faculty"]
    list_display_links = ["username", "phone", "email"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "phone", "faculty")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "is_staff",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )


class InstructorAdmin(admin.ModelAdmin):
    model = Instructor
    list_display = [
        "username",
        "phone",
        "email",
        "full_name",
        "is_active",
        "is_available_now",
        "department",
    ]

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def username(self, obj):
        return obj.user.username

    def phone(self, obj):
        return obj.user.phone

    def email(self, obj):
        return obj.user.email

    def is_active(self, obj):
        return obj.user.is_active


admin.site.register(User, CustomUserAdmin)
admin.site.register(Instructor, InstructorAdmin)
