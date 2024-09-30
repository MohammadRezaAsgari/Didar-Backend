import json
from django.db import transaction

from faculty.models import Faculty


class DataImporter:
    @classmethod
    @transaction.atomic
    def importer(cls):
        data = cls._read_data()
        cls._create_faculty(data)

    @classmethod
    def _read_data(cls):
        with open("faculty/fixtures/faculty_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    @classmethod
    def _create_faculty(cls, data) -> None:
        for instance in data:
            Faculty.objects.get_or_create(
                pk=instance.get('pk'),
                defaults=instance.get('fields'),
            )
