from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from faculty.api.v1.serializers import (DepartmentDetailsSerializer,
                                        DepartmentSerializer,
                                        FacultyDetailsSerializer,
                                        FacultySerializer)
from faculty.models import Department, Faculty
from users.api.v1.serializers import InstructorListSerializer, InstructorSerializer
from users.models import Instructor
from utils.api.error_objects import ErrorObject
from utils.api.mixins import BadRequestSerializerMixin
from utils.api.responses import error_response, success_response
from utils.permissions import IsAuthenticatedAndActive


class FacultyListAPIView(BadRequestSerializerMixin, ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = FacultySerializer
    queryset = Faculty.objects.all()

    @extend_schema(
        request=None,
        parameters=[],
        responses={200: FacultySerializer},
        auth=None,
        operation_id="FacultyList",
        tags=["Faculty"],
    )
    def get(self, request, *args, **kwargs):
        """
        get list of the faculties
        """
        return super().get(request, *args, **kwargs)


class FacultyByIdAPIView(BadRequestSerializerMixin, APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=None,
        responses={200: FacultyDetailsSerializer},
        auth=None,
        operation_id="RetrieveFaculty",
        tags=["Faculty"],
    )
    def get(self, request, *args, **kwargs):
        """
        get a faculty details
        """
        faculty_id = kwargs.get("faculty_id")
        try:
            faculty_obj = Faculty.objects.get(id=faculty_id)
        except Faculty.DoesNotExist:
            return error_response(
                error=ErrorObject.FACULTY_NOT_EXISTS,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        response = FacultyDetailsSerializer(faculty_obj)
        return success_response(data=response.data, status_code=status.HTTP_200_OK)


class FacultyDepartmentListAPIView(BadRequestSerializerMixin, ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        faculty_id = self.kwargs.get("faculty_id")
        try:
            faculty_obj = Faculty.objects.get(id=faculty_id)
        except Faculty.DoesNotExist:
            raise Faculty.DoesNotExist
        return Department.objects.filter(faculty=faculty_obj)

    @extend_schema(
        request=None,
        parameters=[],
        responses={200: DepartmentSerializer},
        auth=None,
        operation_id="FacultyDepartmentList",
        tags=["Faculty"],
    )
    def get(self, request, *args, **kwargs):
        """
        get list of the departments of a faculty
        """
        try:
            return super().get(request, *args, **kwargs)
        except Faculty.DoesNotExist:
            return error_response(
                error=ErrorObject.FACULTY_NOT_EXISTS,
                status_code=status.HTTP_404_NOT_FOUND,
            )


class DepartmentByIdAPIView(BadRequestSerializerMixin, APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=None,
        responses={200: DepartmentDetailsSerializer},
        auth=None,
        operation_id="RetrieveDepartment",
        tags=["Faculty"],
    )
    def get(self, request, *args, **kwargs):
        """
        get a department details
        """
        department_id = kwargs.get("department_id")
        try:
            department_obj = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return error_response(
                error=ErrorObject.DEPARTMENT_NOT_EXISTS,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        response = DepartmentDetailsSerializer(department_obj)
        return success_response(data=response.data, status_code=status.HTTP_200_OK)


class DepartmentInstructorListAPIView(BadRequestSerializerMixin, ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = InstructorListSerializer

    def get_queryset(self):
        department_id = self.kwargs.get("department_id")
        try:
            department_obj = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            raise Department.DoesNotExist
        return department_obj.instructors.all()

    @extend_schema(
        request=None,
        parameters=[],
        responses={200: InstructorListSerializer},
        auth=None,
        operation_id="DepartmentInstructorsList",
        tags=["Faculty"],
    )
    def get(self, request, *args, **kwargs):
        """
        get list of the instructors of a department
        """
        try:
            return super().get(request, *args, **kwargs)
        except Department.DoesNotExist:
            return error_response(
                error=ErrorObject.DEPARTMENT_NOT_EXISTS,
                status_code=status.HTTP_404_NOT_FOUND,
            )


class InstructorListAPIView(BadRequestSerializerMixin, ListAPIView):
    permission_classes = [IsAuthenticatedAndActive]
    serializer_class = InstructorListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "department",
        "department__faculty",
    ]

    def get_queryset(self):
        return Instructor.objects.all()

    @extend_schema(
        request=None,
        parameters=[],
        responses={200: InstructorListSerializer},
        auth=None,
        operation_id="InstructorsList",
        tags=["Faculty"],
    )
    def get(self, request, *args, **kwargs):
        """
        get list of the instructors
        """
        return super().get(request, *args, **kwargs)


class InstructorByIDAPIView(BadRequestSerializerMixin, APIView):
    permission_classes = [IsAuthenticatedAndActive]

    @extend_schema(
        request=None,
        parameters=[],
        responses={200: InstructorSerializer},
        auth=None,
        operation_id="InstructorById",
        tags=["Faculty"],
    )
    def get(self, request, *args, **kwargs):
        """
        get instructor details by id
        """
        try:
            instructor_obj = Instructor.objects.get(id=kwargs.get("instructor_id"))
        except Instructor.DoesNotExist:
            return error_response(
                error=ErrorObject.NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        response = InstructorSerializer(instructor_obj)
        return success_response(data=response.data, status_code=status.HTTP_200_OK)
