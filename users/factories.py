from django.contrib.auth import get_user_model

import factory
from faker import Faker

User = get_user_model()
fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "dolphins")
    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = factory.Sequence(lambda n: f"+989123456{n:03}")

    class Meta:
        model = User
        django_get_or_create = ("email", "phone", "username")
