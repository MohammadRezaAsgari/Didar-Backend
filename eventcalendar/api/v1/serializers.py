from django.contrib.auth import get_user_model
from rest_framework import serializers


class EventTimeSerializer(serializers.Serializer):
    date_time = serializers.DateTimeField()
    time_zone = serializers.CharField()


class GoogleCalendarEventSerializer(serializers.Serializer):
    summary = serializers.CharField()
    start = EventTimeSerializer()
    end = EventTimeSerializer()
    htmlLink = serializers.CharField()
    hangout_link = serializers.CharField(required=False)
