from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    UserDetailsView,
)
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

app_name = "jwt-auth"
urlpatterns = [
    path("api/auth/login/", LoginView.as_view(), name="login"),
    path("api/auth/logout/", LogoutView.as_view(), name="logout"),
    path(
        "api/auth/password/change/",
        PasswordChangeView.as_view(),
        name="password_change",
    ),
    path("api/auth/user/", UserDetailsView.as_view(), name="user-details"),
    path(
        "api/auth/token/verify/",
        TokenVerifyView.as_view(),
        name="token-verify",
    ),
    path(
        "api/auth/token/refresh/",
        get_refresh_view().as_view(),
        name="token-refresh",
    ),
]
