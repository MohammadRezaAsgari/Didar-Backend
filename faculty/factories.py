import factory
from django.contrib.auth import get_user_model
from faker import Faker

from faculty.models import Department, Faculty

fake = Faker()


class FacultyFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = Faculty
        django_get_or_create = ("name",)


class DepartmentFactory(factory.django.DjangoModelFactory):
    faculty = factory.SubFactory(FacultyFactory)
    name = factory.Faker("word")

    class Meta:
        model = Department
        django_get_or_create = ("name",)
