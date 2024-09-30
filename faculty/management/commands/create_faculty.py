from django.core.management.base import BaseCommand, CommandError

from ._faculty_data import DataImporter


class Command(BaseCommand):
    help = "Create faculties Data"

    def handle(self, *args, **options):
        try:
            DataImporter.importer()
        except Exception as e:
            raise CommandError(e)
        self.stdout.write(self.style.SUCCESS(
            "Successfully import Faculty Data!"))
