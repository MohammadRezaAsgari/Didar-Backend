from django.urls import resolve, reverse
from rest_framework.test import APITestCase


from schedule.api.v1.views import (
    InstructorScheduleByIdAPIView,
    InstructorScheduleListAPIView,
    ScheduleByInstructorAPIView,
)

from schedule.factories import ScheduleFactory
from schedule.models import Schedule
from users.factories import UserFactory, InstructorFactory
from utils.api.error_objects import ErrorObject


class TestInstructorScheduleListAPIView(APITestCase):
    def setUp(self):
        self.url = reverse("schedule:v1:instructor_schedule_list")
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.instructor = InstructorFactory(user=self.user)
        self.schedule = ScheduleFactory(
            instructor=self.instructor, start_time="10:00:00", end_time="12:00:00", day_of_week=1)

    def test_get_schedule_list_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get("success"), True)
        self.assertIn("code", json_response.get("data").get("results")[0])
        self.assertIn("created_at", json_response.get(
            "data").get("results")[0])
        self.assertIn("updated_at", json_response.get(
            "data").get("results")[0])

    def test_post_schedule_valid_data_success(self):
        self.client.force_login(self.user)
        data = {
            "title": "title",
            "day_of_week": 1,
            "start_time": "09:00:00",
            "end_time": "10:00:00",
        }
        response = self.client.post(self.url, data=data)
        json_response = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_response.get("success"), True)

    def test_post_schedule_invalid_data_fail(self):
        self.client.force_login(self.user)
        data = {
            "title": "title",
            "day_of_week": 1,
            "start_time": "09:00:00",
            "end_time": "10:30:00",  # overlaps
        }
        response = self.client.post(self.url, data=data)
        json_response = response.json()

        self.assertEqual(response.status_code, 406)
        self.assertEqual(json_response.get("success"), False)
        self.assertEqual(json_response.get("error").get(
            "code"), ErrorObject.SCHEDULE_OVERLAPS.get("code"))
        self.assertEqual(json_response.get("error").get(
            "msg"), ErrorObject.SCHEDULE_OVERLAPS.get("msg"))

    def test_post_schedule_not_instructor_fail(self):
        self.client.force_login(self.user2)
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 403)

    def test_post_schedule_unauth_fail(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 401)

    def test_resolve_url(self):
        resolver = resolve("/api/v1/instructor/schedules/")
        self.assertEqual(resolver.view_name,
                         "schedule:v1:instructor_schedule_list")
        self.assertEqual(resolver.func.view_class,
                         InstructorScheduleListAPIView)
        self.assertEqual(resolver.namespace, "schedule:v1")
        self.assertEqual(resolver.url_name, "instructor_schedule_list")


class TestInstructorScheduleByIdAPIView(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.instructor = InstructorFactory(user=self.user)
        self.instructor2 = InstructorFactory(user=self.user2)
        self.schedule = ScheduleFactory(
            instructor=self.instructor, start_time="10:00:00", end_time="12:00:00", day_of_week=1)
        self.schedule2 = ScheduleFactory(
            instructor=self.instructor2, start_time="10:00:00", end_time="12:00:00", day_of_week=1)

        self.url = reverse("schedule:v1:instructor_schedule", kwargs={
                           "schedule_code": self.schedule.code})

    def test_get_schedule_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get("success"), True)
        self.assertEqual(json_response.get(
            "data").get("title"), self.schedule.title)

    def test_get_schedule_not_found_fail(self):
        self.client.force_login(self.user)

        url = reverse("schedule:v1:instructor_schedule", kwargs={
            "schedule_code": self.schedule2.code})
        response = self.client.get(url)
        json_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response.get("success"), False)

    def test_patch_schedule_success(self):
        self.client.force_login(self.user)
        data = {
            "title": "new_title"
        }

        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, 204)

        self.schedule.refresh_from_db()
        self.assertEqual(self.schedule.title, "new_title")

    def test_delete_schedule_success(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Schedule.objects.filter(
            code=self.schedule.code).exists(), False)

    def test_resolve_url(self):
        resolver = resolve("/api/v1/instructor/schedules/5/")
        self.assertEqual(resolver.view_name,
                         "schedule:v1:instructor_schedule")
        self.assertEqual(resolver.func.view_class,
                         InstructorScheduleByIdAPIView)
        self.assertEqual(resolver.namespace, "schedule:v1")
        self.assertEqual(resolver.url_name, "instructor_schedule")


class TestScheduleByInstructorAPIView(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.instructor = InstructorFactory(user=self.user)
        self.schedule = ScheduleFactory(
            instructor=self.instructor, start_time="10:00:00", end_time="12:00:00", day_of_week=1)

        self.url = reverse("schedule:v1:schedule_list_by_instructor", kwargs={
                           "instructor_id": self.instructor.id})

    def test_get_schedule_list_success(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        json_response = response.json()
        self.assertEqual(json_response.get("success"), True)
        self.assertEqual(json_response.get("data").get("count"), 1)

    def test_get_schedule_list_unauth_fail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_resolve_url(self):
        resolver = resolve("/api/v1/instructor/5/schedules/")
        self.assertEqual(resolver.view_name,
                         "schedule:v1:schedule_list_by_instructor")
        self.assertEqual(resolver.func.view_class,
                         ScheduleByInstructorAPIView)
        self.assertEqual(resolver.namespace, "schedule:v1")
        self.assertEqual(resolver.url_name, "schedule_list_by_instructor")
