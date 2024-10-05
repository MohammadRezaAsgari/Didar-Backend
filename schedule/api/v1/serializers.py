from rest_framework import serializers

from schedule.models import Schedule


class InstructorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = [
            "code",
            "title",
            "day_of_week",
            "start_time",
            "end_time",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ("created_at", "updated_at")


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = [
            "title",
            "day_of_week",
            "start_time",
            "end_time",
        ]
