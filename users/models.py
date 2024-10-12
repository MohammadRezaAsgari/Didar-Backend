from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from users.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=500, unique=True)
    phone = models.CharField(max_length=255, null=True, blank=True, unique=True)
    email = models.EmailField(max_length=255, null=True, blank=True, unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)

    faculty = models.ForeignKey(
        "faculty.Faculty",
        on_delete=models.SET_NULL,
        related_name="students",
        null=True,
        blank=True,
    )

    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDERS = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    )
    gender = models.PositiveSmallIntegerField(choices=GENDERS, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USER_ID_FIELD = "id"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def is_instructor(self):
        return hasattr(self, "instructor")

    def get_full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}"

    def get_current_week_range(self):
        now = datetime.utcnow()
        days_since_saturday = (now.weekday() + 2) % 7
        last_saturday = now - timedelta(days=days_since_saturday)
        thursday = last_saturday + timedelta(days=5)

        time_min = now.isoformat() + "Z"
        time_max = thursday.isoformat() + "Z"

        return time_min, time_max

    def get_google_calendar_events(self):
        social_user = self.social_auth.get(provider="google-oauth2")

        credentials = Credentials(
            token=social_user.extra_data["access_token"],
            refresh_token=social_user.extra_data["refresh_token"],
            client_id=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            client_secret=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            token_uri="https://oauth2.googleapis.com/token",
        )

        # Build Google Calendar API client
        service = build("calendar", "v3", credentials=credentials)

        time_min, time_max = self.get_current_week_range()
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=time_min,  # From now (to exclude past events)
                timeMax=time_max,  # Until Thursday
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])
        return events


class Instructor(models.Model):
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="instructor"
    )
    bio = models.TextField(blank=True, null=True)
    room_phone = models.CharField(max_length=255, null=True, blank=True, unique=True)
    room_number = models.PositiveIntegerField(null=True, blank=True, unique=True)
    is_available_now = models.BooleanField(default=False)
    department = models.ForeignKey(
        "faculty.Department", on_delete=models.CASCADE, related_name="instructors"
    )

    def __str__(self):
        return f"{self.user.username}"
