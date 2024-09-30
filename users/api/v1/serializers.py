from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from faculty.api.v1.serializers import DepartmentSerializer, FacultySerializer
from users.models import Instructor

User = get_user_model()


class LoginPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class LoginOutputSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)
    gender = serializers.IntegerField(
        help_text='ENUM  `1:Male`, `2:Female`'
    )
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()
    access_token_expires_at = serializers.SerializerMethodField()

    def _get_token(self, obj):
        # This method only called once
        self.refresh_token = RefreshToken.for_user(obj)
        self.access_token = self.refresh_token.access_token

    def get_access(self, obj) -> str:
        if not hasattr(self, 'access_token'):
            self._get_token(obj)
        return str(self.access_token)

    def get_refresh(self, obj) -> str:
        if not hasattr(self, 'refresh_token'):
            self._get_token(obj)
        return str(self.refresh_token)

    def get_access_token_expires_at(self, obj):
        if not hasattr(self, 'access_token'):
            self._get_token(obj)
        # Calculate expiration time from the access token
        expiration_timestamp = self.access_token['exp'] if 'exp' in self.access_token else None
        return expiration_timestamp

    class Meta:
        model = User
        fields = [
            'phone',
            'email',
            'username',
            'first_name',
            'last_name',
            'gender',
            'faculty',
            'access',
            'refresh',
            'access_token_expires_at',
            'is_instructor',
        ]


class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)


class InstructorSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Instructor
        fields = [
            'bio',
            'room_phone',
            'room_number',
            'is_available_now',
            'department',
        ]

class UserProfileSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField(source='get_phone')
    gender = serializers.IntegerField(
        help_text='ENUM  `1:Male`, `2:Female`'
    )
    instructor = InstructorSerializer(read_only=True)
    faculty = FacultySerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'phone',
            'first_name',
            'last_name',
            'email',
            'gender',
            'is_instructor',
            'instructor',
            'faculty',
        ]

    def get_phone(self, obj):
        user_phone = obj.phone
        if user_phone:
            str_list = list(str(user_phone))
            str_list[-4] = str_list[-5] = str_list[-6] = '*'
            return ''.join(str_list)
        return user_phone

    def get_instructor(self, obj):
        if obj.is_instructor:
            return obj.instructor
        return None


class UserProfileInputSerializer(serializers.ModelSerializer):
    gender = serializers.IntegerField(
        help_text='ENUM  `1:Male`, `2:Female`'
    )

    class Meta:
        model = User
        fields = [
            'phone',
            'email',
            'first_name',
            'last_name',
            'gender',
        ]
