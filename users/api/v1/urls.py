from django.urls import path

from users.api.v1.views import (CheckGoogleAuthAPIView,
                                DecoratedRefreshTokenView,
                                InstructorProfileAPIView, LoginPasswordAPIView,
                                LogOutAPIView, UserProfileAPIView)

app_name = "v1"

urlpatterns = [
    # AUTH URLS
    path(
        "auth/check-google-auth-exist/",
        CheckGoogleAuthAPIView.as_view(),
        name="check_google_auth",
    ),
    # Login flow API
    path("auth/login-password/", LoginPasswordAPIView.as_view(), name="login_password"),
    # --
    path("auth/refresh/", DecoratedRefreshTokenView.as_view(), name="token_refresh"),
    path("auth/logout/", LogOutAPIView.as_view(), name="logout"),
    path("auth/me/", UserProfileAPIView.as_view(), name="user_profile"),
    path(
        "auth/instructor/",
        InstructorProfileAPIView.as_view(),
        name="instructor_profile",
    ),
]
