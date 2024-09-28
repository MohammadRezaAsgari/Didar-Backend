from django.contrib.auth import get_user_model

import factory
from faker import Faker

from faculty.models import Faculty, Department

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