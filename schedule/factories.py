import factory
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()


# class UserFactory(factory.django.DjangoModelFactory):
#     email = factory.Faker("email")
#     password = factory.PostGenerationMethodCall("set_password", "dolphins")
#     username = factory.Faker("user_name")
#     first_name = factory.Faker("first_name")
#     last_name = factory.Faker("last_name")
#     phone = factory.Sequence(lambda n: f"+989123456{n:03}")

#     class Meta:
#         model = User
#         django_get_or_create = ("email", "phone", "username")


# class InstructorFactory(factory.django.DjangoModelFactory):
#     department = factory.SubFactory(DepartmentFactory)
#     user = factory.SubFactory(UserFactory)

#     class Meta:
#         model = Instructor
