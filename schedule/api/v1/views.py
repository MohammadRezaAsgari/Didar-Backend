from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.core.exceptions import ValidationError

from schedule.api.v1.serializers import (
    InstructorScheduleSerializer,
    ScheduleSerializer
)

from schedule.models import Schedule
from users.models import Instructor
from utils.api.error_objects import ErrorObject
from utils.api.mixins import BadRequestSerializerMixin
from utils.api.responses import error_response, success_response
from utils.permissions import IsAuthenticatedAndActive, IsInstructor


class InstructorScheduleListAPIView(BadRequestSerializerMixin, ListAPIView):
    permission_classes = [IsInstructor]
    serializer_class = InstructorScheduleSerializer

    def get_queryset(self):
        schedule_objs = Schedule.objects.filter(
            instructor=self.request.user.instructor
        ).order_by('-day_of_week')
        return schedule_objs

    @extend_schema(
        request=None,
        parameters=[],
        responses={200: InstructorScheduleSerializer},
        auth=None,
        operation_id="InstructorScheduleList",
        tags=["Schedule"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        request=ScheduleSerializer,
        responses={201: ScheduleSerializer},
        operation_id="CreateSchedule",
        tags=["Schedule"],
    )
    def post(self, request, *args, **kwargs):
        serializer = ScheduleSerializer(
            data=request.data)
        if not serializer.is_valid():
            return self.serializer_error_response(serializer)

        try:
            serializer.save(instructor=request.user.instructor)
        except ValidationError:
            return error_response(
                error=ErrorObject.SCHEDULE_OVERLAPS, status_code=status.HTTP_406_NOT_ACCEPTABLE
            )
        return success_response(data=serializer.data, status_code=status.HTTP_201_CREATED)


class InstructorScheduleByIdAPIView(BadRequestSerializerMixin, APIView):
    permission_classes = [IsInstructor]

    @extend_schema(
        request=None,
        responses={200: InstructorScheduleSerializer},
        auth=None,
        operation_id="RetrieveSchedule",
        tags=["Schedule"],
    )
    def get(self, request, *args, **kwargs):
        schedule_code = self.kwargs.get('schedule_code')
        try:
            schedule_obj = Schedule.objects.get(code=schedule_code, instructor=request.user.instructor)
        except Schedule.DoesNotExist:
            return error_response(
                error=ErrorObject.SCHEDULE_NOT_EXISTS, status_code=status.HTTP_404_NOT_FOUND
            )
        response = InstructorScheduleSerializer(schedule_obj)
        return success_response(data=response.data, status_code=status.HTTP_200_OK)

    @extend_schema(
        request=ScheduleSerializer,
        responses={204: {}},
        auth=None,
        operation_id='UpdateSchedule',
        tags=['Schedule'],
    )
    def patch(self, request, *args, **kwargs):
        schedule_code = self.kwargs.get('schedule_code')
        try:
            schedule_obj = Schedule.objects.get(
                code=schedule_code, instructor=request.user.instructor)
        except Schedule.DoesNotExist:
            return error_response(
                error=ErrorObject.SCHEDULE_NOT_EXISTS, status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = ScheduleSerializer(
            schedule_obj, data=request.data, partial=True)
        if not serializer.is_valid():
            return self.serializer_error_response(serializer)

        try:
            serializer.save()
        except ValidationError:
            return error_response(
                error=ErrorObject.SCHEDULE_OVERLAPS, status_code=status.HTTP_406_NOT_ACCEPTABLE
            )

        return success_response(data={}, status_code=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        request=None,
        responses={204: {}},
        auth=None,
        operation_id="DeleteSchedule",
        tags=["Schedule"],
    )
    def delete(self, request, *args, **kwargs):
        schedule_code = self.kwargs.get('schedule_code')
        try:
            schedule_obj = Schedule.objects.get(
                code=schedule_code, instructor=request.user.instructor)
        except Schedule.DoesNotExist:
            return error_response(
                error=ErrorObject.SCHEDULE_NOT_EXISTS, status_code=status.HTTP_404_NOT_FOUND
            )
        schedule_obj.delete()
        return success_response(data={}, status_code=status.HTTP_204_NO_CONTENT)


class ScheduleByInstructorAPIView(BadRequestSerializerMixin, ListAPIView):
    permission_classes = [IsAuthenticatedAndActive]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        instructor_obj = Instructor.objects.get(
            id=self.kwargs.get('instructor_id'))
        schedule_objs = Schedule.objects.filter(
            instructor=instructor_obj
        ).order_by('-day_of_week')
        return schedule_objs

    @extend_schema(
        request=None,
        parameters=[],
        responses={200: ScheduleSerializer},
        auth=None,
        operation_id="ScheduleList",
        tags=["Schedule"],
    )
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Instructor.DoesNotExist:
            return error_response(error=ErrorObject.INSTRUCTOR_NOT_EXISTS, status_code=status.HTTP_404_NOT_FOUND)
