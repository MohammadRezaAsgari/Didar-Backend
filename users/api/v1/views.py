from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from social_django.models import UserSocialAuth
from social_django.utils import load_strategy

from users.api.v1.serializers import (GoogleAuthExistsSerializer,
                                      InstructorSerializer,
                                      LoginOutputSerializer,
                                      LoginPasswordSerializer,
                                      LogOutSerializer,
                                      UserProfileInputSerializer,
                                      UserProfileSerializer)
from utils.api.error_objects import ErrorObject
from utils.api.mixins import BadRequestSerializerMixin
from utils.api.responses import error_response, success_response
from utils.permissions import IsAuthenticatedAndActive, IsInstructor

User = get_user_model()


class LoginPasswordAPIView(BadRequestSerializerMixin, APIView):
    """
    Login a user with input username and password
    """

    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginPasswordSerializer,
        responses={200: LoginOutputSerializer},
        auth=None,
        operation_id="LoginWithPassword",
        tags=["Auth"],
    )
    def post(self, request):
        serializer = LoginPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return self.serializer_error_response(serializer)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        try:
            user_obj = User.objects.get(username=username, is_active=True)
        except User.DoesNotExist:
            return error_response(
                error=ErrorObject.USER_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND
            )

        # User can log in with their password
        if not user_obj.check_password(password):
            return error_response(
                error=ErrorObject.UN_AUTH, status_code=status.HTTP_401_UNAUTHORIZED
            )

        output = LoginOutputSerializer(user_obj, context={"request": request})
        return success_response(data=output.data, status_code=status.HTTP_200_OK)


class DecoratedRefreshTokenView(TokenRefreshView):
    """
    Refresh Token
    """

    serializer_class = TokenRefreshSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        request=TokenRefreshSerializer,
        responses={200: TokenRefreshSerializer},
        operation_id="RefreshToken",
        tags=["Auth"],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid()
        except TokenError:
            return error_response(
                error=ErrorObject.INVALID_TOKEN,
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        return success_response(
            data=serializer.validated_data, status_code=status.HTTP_200_OK
        )


class LogOutAPIView(BadRequestSerializerMixin, APIView):
    """
    Move refresh token to blacklist. Also needs to destroy stored access token from frontend.
    """

    permission_classes = [IsAuthenticatedAndActive]

    @extend_schema(
        request=LogOutSerializer,
        responses={200: None},
        operation_id="LogOut",
        tags=["Auth"],
    )
    def post(self, request):
        serializer = LogOutSerializer(data=request.data)
        if not serializer.is_valid():
            return self.serializer_error_response(serializer)
        refresh_token = serializer.validated_data.get("refresh")
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return error_response(
                error=ErrorObject.INVALID_TOKEN,
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )
        return success_response(data={}, status_code=status.HTTP_200_OK)


class UserProfileAPIView(BadRequestSerializerMixin, APIView):
    permission_classes = [IsAuthenticatedAndActive]

    @extend_schema(
        request=None,
        responses={200: UserProfileSerializer},
        auth=None,
        operation_id="UserProfile",
        tags=["Auth"],
    )
    def get(self, request):
        """
        get user profile info

        gender ==> `1:Male`, `2:Female`
        """
        user = request.user
        response = UserProfileSerializer(user)
        return success_response(data=response.data)

    @extend_schema(
        request=UserProfileInputSerializer,
        responses={204: {}},
        auth=None,
        operation_id="UserProfileUpdate",
        tags=["Auth"],
    )
    def patch(self, request):
        """
        update user info

        gender ==> `1:Male`, `2:Female`
        """
        user = request.user
        serializer = UserProfileInputSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return success_response(data={}, status_code=status.HTTP_204_NO_CONTENT)


class InstructorProfileAPIView(BadRequestSerializerMixin, APIView):
    permission_classes = [IsAuthenticatedAndActive, IsInstructor]

    @extend_schema(
        request=InstructorSerializer,
        responses={204: {}},
        auth=None,
        operation_id="InstructorProfileUpdate",
        tags=["Auth"],
    )
    def patch(self, request):
        """
        update instructor profile details
        """
        instructor_obj = request.user.instructor
        serializer = InstructorSerializer(
            instructor_obj, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return error_response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return success_response(data={}, status_code=status.HTTP_204_NO_CONTENT)


class CheckGoogleAuthAPIView(BadRequestSerializerMixin, APIView):
    permission_classes = [IsAuthenticatedAndActive, IsInstructor]

    @extend_schema(
        request=None,
        parameters=[],
        responses={200: GoogleAuthExistsSerializer},
        auth=None,
        operation_id="GoogleAuthExists",
        tags=["Auth"],
    )
    def get(self, request, *args, **kwargs):
        """
        Check if Google Credential exists.
        """

        user_social_auth: UserSocialAuth = UserSocialAuth.objects.filter(
            user_id=request.user.id, provider="google-oauth2"
        ).exists()
        if not user_social_auth:
            return success_response(
                data={"google_credential_exist": False},
                status_code=status.HTTP_200_OK,
            )

        user_social_auth = UserSocialAuth.objects.filter(
            user_id=request.user.id, provider="google-oauth2"
        ).last()
        try:
            if user_social_auth.access_token_expired():
                    # Load strategy and backend
                    strategy = load_strategy(request)

                    # Refresh the token
                    user_social_auth.refresh_token(strategy=strategy)

                    # Update the access token and expiration time
                    user_social_auth.save()
                    return success_response(
                        data={"google_credential_exist": True},
                        status_code=status.HTTP_200_OK,
                    )
        except Exception:
            return success_response(
                data={"google_credential_exist": False},
                status_code=status.HTTP_200_OK,
            )

        return success_response(
            data={"google_credential_exist": True},
            status_code=status.HTTP_200_OK,
        )
