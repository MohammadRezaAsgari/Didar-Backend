import json

from django.db import transaction

from faculty.models import Department, Faculty


class DataImporter:
    @classmethod
    @transaction.atomic
    def importer(cls):
        data = cls._read_data()
        cls._create_department(data)

    @classmethod
    def _read_data(cls):
        with open("faculty/fixtures/department_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    @classmethod
    def _create_department(cls, data) -> None:
        for instance in data:
            faculty_object = Faculty.objects.get(
                id=instance.get("fields").get("faculty")
            )
            Department.objects.get_or_create(
                pk=instance.get("pk"),
                name=instance.get("fields").get("name"),
                faculty=faculty_object,
            )
