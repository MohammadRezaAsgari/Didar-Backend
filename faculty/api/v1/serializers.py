from rest_framework import serializers

from faculty.models import Faculty, Department


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = [
            'id',
            'name',
        ]


class FacultyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = [
            'id',
            'name',
        ]

class DepartmentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()

    class Meta:
        model = Department
        fields = [
            'id',
            'name',
            'faculty',
        ]


class DepartmentDetailsSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()

    class Meta:
        model = Department
        fields = [
            'id',
            'name',
            'faculty',
        ]
