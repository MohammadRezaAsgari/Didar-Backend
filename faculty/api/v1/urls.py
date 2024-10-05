from django.urls import path

from faculty.api.v1.views import (
    FacultyListAPIView,
    FacultyByIdAPIView,
    FacultyDepartmentListAPIView,
    DepartmentByIdAPIView,
    DepartmentInstructorListAPIView,
)

app_name = 'v1'

urlpatterns = [
    path("faculties/",
         FacultyListAPIView.as_view(),
         name="faculty_list"),
    path("faculties/<int:faculty_id>/",
         FacultyByIdAPIView.as_view(),
         name="faculty_by_id"),
    path("faculties/<int:faculty_id>/departments/",
         FacultyDepartmentListAPIView.as_view(),
         name="department_list"),
    path("departments/<int:department_id>/",
         DepartmentByIdAPIView.as_view(),
         name="department_by_id"),
    path("departments/<int:department_id>/instructors/",
         DepartmentInstructorListAPIView.as_view(),
         name="department_instructors"),
]
