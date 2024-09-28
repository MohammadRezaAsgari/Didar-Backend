from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from users.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=500, unique=True)
    phone = models.CharField(max_length=255, null=True,
                             blank=True, unique=True)
    email = models.EmailField(
        max_length=255, null=True, blank=True, unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)

    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDERS = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    )
    gender = models.PositiveSmallIntegerField(
        choices=GENDERS, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USER_ID_FIELD = "id"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def is_instructor(self):
        return hasattr(self, "instructor")


class Instructor(models.Model):
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="instructor")
    bio = models.TextField(blank=True, null=True)
    room_phone = models.CharField(max_length=255, null=True,
                                  blank=True, unique=True)
    room_number = models.PositiveIntegerField(null=True, blank=True, unique=True)
    is_available_now = models.BooleanField(default=False)
    department = models.ForeignKey(
        "faculty.Department", on_delete=models.CASCADE, related_name="instructors")
    # weekly_schedule

    def __str__(self):
        return f"{self.user.username}"
