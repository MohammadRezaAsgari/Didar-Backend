import random
import string

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Schedule(models.Model):
    DAY_SATURDAY = 1
    DAY_SUNDAY = 2
    DAY_MONDAY = 3
    DAY_TUESDAY = 4
    DAY_WEDNESDAY = 5
    DAY_THURSDAY = 6

    DAY_CHOICES = [
        (1, "Saturday"),
        (2, "Sunday"),
        (3, "Monday"),
        (4, "Tuesday"),
        (5, "Wednesday"),
        (6, "Thursday"),
    ]

    code = models.CharField(max_length=30, unique=True, blank=True)
    title = models.CharField(max_length=25)
    instructor = models.ForeignKey("users.Instructor", on_delete=models.CASCADE)
    day_of_week = models.PositiveSmallIntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        unique_together = ("instructor", "day_of_week", "start_time", "end_time")

    def __str__(self):
        return f"{self.instructor.user.username} - {self.DAY_CHOICES[self.day_of_week - 1][1]}: {self.start_time} to {self.end_time}"

    def clean(self):
        # Check for overlapping schedules for the same instructor on the same day
        overlapping_schedules = (
            Schedule.objects.filter(
                instructor=self.instructor,
                day_of_week=self.day_of_week,
            )
            .exclude(pk=self.pk)
            .filter(
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
            )
        )
        if overlapping_schedules.exists():
            raise ValidationError(
                _(
                    "This schedule overlaps with another schedule for the same instructor."
                )
            )

    def save(self, *args, **kwargs):
        self.clean()
        if not self.code:
            # Generate a unique code
            self.code = self._generate_unique_code()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_unique_code(cls):
        while True:
            code = cls._generate_code()
            if not cls.objects.filter(code=code).exists():
                return code

    @staticmethod
    def _generate_code():
        """
        This method is used to generate a unique code for the schedule in this format:
        schedule-2023-11-01-A123
        Last 4 chars are random.
        """
        # Generate a random uppercase letter from A-Z
        random_letter = random.choice(string.ascii_uppercase)

        # Generate a random 3 digit number
        random_number = random.randint(100, 999)
        now = timezone.now()
        return (
            f"schedule-{now.year}-{now.month}-{now.day}-{random_letter}{random_number}"
        )
