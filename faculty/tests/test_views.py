from django.urls import resolve, reverse
from rest_framework.test import APITestCase

from faculty.api.v1.views import (
    DepartmentInstructorListAPIView,
    FacultyListAPIView,
    FacultyByIdAPIView,
    FacultyDepartmentListAPIView,
    DepartmentByIdAPIView,
)
from faculty.factories import DepartmentFactory, FacultyFactory
from users.factories import InstructorFactory, UserFactory


class TestFacultyListAPIView(APITestCase):
    def setUp(self):
        self.url = reverse('faculty:v1:faculty_list')
        self.faculties = FacultyFactory.create_batch(10)

    def test_get_faculty_list_success(self):
        response = self.client.get(self.url)
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('success'), True)
        self.assertEqual(json_response.get('data').get('count'), 10)
        self.assertIn('id', json_response.get('data').get('results')[0])
        self.assertIn('name', json_response.get('data').get('results')[0])

    def test_resolve_url(self):
        resolver = resolve('/api/v1/faculties/')
        self.assertEqual(resolver.view_name, 'faculty:v1:faculty_list')
        self.assertEqual(resolver.func.view_class, FacultyListAPIView)
        self.assertEqual(resolver.namespace, 'faculty:v1')
        self.assertEqual(resolver.url_name, 'faculty_list')


class TestFacultyByIdAPIView(APITestCase):
    def setUp(self):
        self.faculty = FacultyFactory()
        self.url = reverse('faculty:v1:faculty_by_id', kwargs={
                           'faculty_id': self.faculty.id})

    def test_get_faculty_by_id_success(self):
        response = self.client.get(self.url)
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('success'), True)
        self.assertIn('id', json_response.get('data'))
        self.assertIn('name', json_response.get('data'))

    def test_get_faculty_by_id_not_fount_fail(self):
        url = reverse('faculty:v1:faculty_by_id', kwargs={'faculty_id': 999})
        response = self.client.get(url)
        json_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response.get('success'), False)

    def test_resolve_url(self):
        resolver = resolve('/api/v1/faculties/5/')
        self.assertEqual(resolver.view_name, 'faculty:v1:faculty_by_id')
        self.assertEqual(resolver.func.view_class, FacultyByIdAPIView)
        self.assertEqual(resolver.namespace, 'faculty:v1')
        self.assertEqual(resolver.url_name, 'faculty_by_id')


class TestFacultyDepartmentListAPIView(APITestCase):
    def setUp(self):
        self.faculty = FacultyFactory()
        self.department1 = DepartmentFactory(faculty=self.faculty)
        self.department2 = DepartmentFactory(faculty=self.faculty)
        self.url = reverse('faculty:v1:department_list', kwargs={
                           'faculty_id': self.faculty.id})

    def test_get_faculty_departments_list_success(self):
        response = self.client.get(self.url)
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('success'), True)
        self.assertEqual(json_response.get('data').get('count'), 2)
        self.assertEqual(json_response.get('data').get('results')[
                         0].get('faculty').get('id'), self.faculty.id)
        self.assertIn('id', json_response.get('data').get('results')[0])
        self.assertIn('name', json_response.get('data').get('results')[0])

    def test_get_faculty_departments_list_not_found_fail(self):
        url = reverse('faculty:v1:department_list', kwargs={'faculty_id': 999})
        response = self.client.get(url)
        json_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response.get('success'), False)

    def test_resolve_url(self):
        resolver = resolve('/api/v1/faculties/5/departments/')
        self.assertEqual(resolver.view_name, 'faculty:v1:department_list')
        self.assertEqual(resolver.func.view_class,
                         FacultyDepartmentListAPIView)
        self.assertEqual(resolver.namespace, 'faculty:v1')
        self.assertEqual(resolver.url_name, 'department_list')


class TestDepartmentByIdAPIView(APITestCase):
    def setUp(self):
        self.faculty = FacultyFactory()
        self.department = DepartmentFactory(faculty=self.faculty)
        self.url = reverse('faculty:v1:department_by_id', kwargs={
                           'department_id': self.department.id})

    def test_get_faculty_department_by_id_success(self):
        response = self.client.get(self.url)
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('success'), True)
        self.assertEqual(json_response.get('data').get(
            'faculty').get('id'), self.faculty.id)
        self.assertIn('id', json_response.get('data'))
        self.assertIn('name', json_response.get('data'))

    def test_get_faculty_department_by_id_not_found_fail(self):
        url = reverse('faculty:v1:department_by_id',
                      kwargs={'department_id': 99})
        response = self.client.get(url)
        json_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response.get('success'), False)

    def test_resolve_url(self):
        resolver = resolve('/api/v1/departments/1/')
        self.assertEqual(resolver.view_name, 'faculty:v1:department_by_id')
        self.assertEqual(resolver.func.view_class,
                         DepartmentByIdAPIView)
        self.assertEqual(resolver.namespace, 'faculty:v1')
        self.assertEqual(resolver.url_name, 'department_by_id')


class TestDepartmentInstructorListAPIView(APITestCase):
    def setUp(self):
        self.faculty = FacultyFactory()
        self.department = DepartmentFactory(faculty=self.faculty)
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.instructor1 = InstructorFactory(
            user=self.user1, department=self.department)
        self.instructor2 = InstructorFactory(
            user=self.user2, department=self.department)
        self.url = reverse('faculty:v1:department_instructors', kwargs={
                           'department_id': self.department.id})

    def test_get_department_instructors_list_success(self):
        response = self.client.get(self.url)
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('success'), True)
        self.assertEqual(json_response.get('data').get('count'), 2)
        self.assertIn('id', json_response.get('data').get('results')[0])
        self.assertIn('name', json_response.get('data').get('results')[0])

    def test_get_department_instructors_list_not_found_fail(self):
        url = reverse('faculty:v1:department_instructors',
                      kwargs={'department_id': 99})
        response = self.client.get(url)
        json_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response.get('success'), False)

    def test_resolve_url(self):
        resolver = resolve('/api/v1/departments/1/instructors/')
        self.assertEqual(resolver.view_name,
                         'faculty:v1:department_instructors')
        self.assertEqual(resolver.func.view_class,
                         DepartmentInstructorListAPIView)
        self.assertEqual(resolver.namespace, 'faculty:v1')
        self.assertEqual(resolver.url_name, 'department_instructors')
