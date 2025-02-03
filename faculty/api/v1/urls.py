from django.urls import path

from faculty.api.v1.views import (
    DepartmentByIdAPIView,
    DepartmentInstructorListAPIView,
    FacultyByIdAPIView,
    FacultyDepartmentListAPIView,
    FacultyListAPIView,
    InstructorListAPIView,
    InstructorByIDAPIView,
)

app_name = "v1"

urlpatterns = [
    path("faculties/", FacultyListAPIView.as_view(), name="faculty_list"),
    path(
        "faculties/<int:faculty_id>/",
        FacultyByIdAPIView.as_view(),
        name="faculty_by_id",
    ),
    path(
        "faculties/<int:faculty_id>/departments/",
        FacultyDepartmentListAPIView.as_view(),
        name="department_list",
    ),
    path(
        "departments/<int:department_id>/",
        DepartmentByIdAPIView.as_view(),
        name="department_by_id",
    ),
    path(
        "departments/<int:department_id>/instructors/",
        DepartmentInstructorListAPIView.as_view(),
        name="department_instructors",
    ),
    path(
        "instructors/",
        InstructorListAPIView.as_view(),
        name="instructors",
    ),
    path(
        "instructors/<int:instructor_id>/",
        InstructorByIDAPIView.as_view(),
        name="instructor_details",
    ),
]
