from datetime import datetime

import pytz
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers


class StartEndSerializer(serializers.Serializer):
    dateTime = serializers.DateTimeField()
    timeZone = serializers.CharField()

    def to_representation(self, instance):
        """This method is called for serialization (output)."""
        representation = super().to_representation(instance)

        representation["date_time"] = instance.get("dateTime")
        representation["time_zone"] = instance.get("timeZone")
        del representation["dateTime"]
        del representation["timeZone"]

        return representation

    def validate_timeZone(self, value):
        # Check if the provided timezone is valid
        if value not in pytz.all_timezones:
            raise serializers.ValidationError(f"{value} is not a valid timezone.")
        return value


class GoogleCalendarEventSerializer(serializers.Serializer):
    summary = serializers.CharField(required=False)
    start = StartEndSerializer()
    end = StartEndSerializer()
    htmlLink = serializers.URLField(required=False)
    hangoutLink = serializers.URLField(required=False)

    def to_representation(self, instance):
        """This method is called for serialization (output)."""
        representation = super().to_representation(instance)

        html_link = instance.get("htmlLink", None)
        hangout_link = instance.get("hangoutLink", None)

        if html_link:
            representation["html_link"] = html_link
            del representation["htmlLink"]
        if hangout_link:
            representation["hangout_link"] = hangout_link
            del representation["hangoutLink"]

        return representation


class GoogleCalendarEventInputSerializer(serializers.Serializer):
    summary = serializers.CharField()
    start = StartEndSerializer()
    end = StartEndSerializer()
    attendees_emails = serializers.ListField(required=False)

    def validate_attendees_emails(self, value):
        """Ensure each email in the attendees list is valid."""
        for email in value:
            try:
                # Use Django's validate_email function to validate each email
                validate_email(email)
            except ValidationError:
                raise serializers.ValidationError(
                    f"'{email}' is not a valid email address."
                )

        return value

    def validate(self, data):
        """Ensure the start time is before the end time."""
        start_data = data.get("start")
        end_data = data.get("end")

        # Extract the datetime and timezone values
        start_time = start_data["dateTime"]
        start_timezone = start_data["timeZone"]
        end_time = end_data["dateTime"]
        end_timezone = end_data["timeZone"]

        if start_timezone != end_timezone:
            raise serializers.ValidationError("start and end time zones are not same!")

        now = datetime.now(pytz.timezone(start_timezone))
        # Ensure start time is not in the past
        if start_time < now:
            raise serializers.ValidationError("The start time cannot be in the past.")

        # Check if start time is before end time
        if start_time >= end_time:
            raise serializers.ValidationError(
                "The start time must be before the end time."
            )

        return data
