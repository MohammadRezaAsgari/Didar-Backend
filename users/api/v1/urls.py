from django.urls import path

from users.api.v1.views import (DecoratedRefreshTokenView,
                                InstructorProfileAPIView, LoginPasswordAPIView,
                                LogOutAPIView, UserProfileAPIView)

app_name = "v1"

urlpatterns = [
    # AUTH URLS
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
