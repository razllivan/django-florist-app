from dj_rest_auth.views import LoginView
from drf_spectacular.extensions import (
    OpenApiSerializerExtension,
    OpenApiViewExtension,
)
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiRequest,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    extend_schema_field,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers


class LoginViewSchema(OpenApiViewExtension):
    target_class = "dj_rest_auth.views.LoginView"

    def view_replacement(self):
        @extend_schema_view(
            post=extend_schema(
                summary="JWT Token Generation",
                description="""This endpoint is responsible for generating a
                JSON Web Token (JWT) upon successful authentication and
                setting the generated tokens as cookies in the response.
                <br>
                Response:
                <br>
                200 OK: Returns the generated JWT
                token in the response body and sets the `access-token` and
                `refresh-token` cookies.""",
                responses=LoginView().get_response_serializer(),
            )
        )
        class Fixed(self.target_class):
            pass

        return Fixed


class GetUserFieldFix(OpenApiSerializerExtension):
    target_class = "dj_rest_auth.serializers.JWTSerializerWithExpiration"

    def map_serializer(self, auto_schema, direction):
        from dj_rest_auth.serializers import UserDetailsSerializer

        class Fixed(self.target_class):
            @extend_schema_field(UserDetailsSerializer)
            def get_user(self):
                pass

        return auto_schema._map_serializer(Fixed, direction)


logout_response_serializer = OpenApiResponse(
    response=inline_serializer(
        name="LogoutSerializer",
        fields={
            "title": serializers.CharField(),
        },
    )
)


class LogoutViewSchema(OpenApiViewExtension):
    target_class = "dj_rest_auth.views.LogoutView"

    def view_replacement(self):
        @extend_schema_view(
            post=extend_schema(
                summary="Invalidate JWT Token and log out",
                description="""This endpoint also clears the `access-token`
                and `refresh-token` cookies from the client's browser.
                <br>
                After successful logout, the client should no longer have
                access to protected resources until a new valid token is
                obtained.""",
                examples=[
                    OpenApiExample(
                        "Successful",
                        value={"detail": "Successfully logged out."},
                        response_only=True,
                        status_codes=[200],
                    ),
                    OpenApiExample(
                        "Error",
                        value={"detail": "Token is invalid or expired"},
                        response_only=True,
                        status_codes=[401],
                    ),
                    OpenApiExample(
                        "Error",
                        value={"detail": "An error has occurred."},
                        response_only=True,
                        status_codes=[500],
                    ),
                ],
                responses={
                    200: logout_response_serializer,
                    401: logout_response_serializer,
                    500: logout_response_serializer,
                },
            ),
            get=extend_schema(exclude=True),
        )
        class Fixed(self.target_class):
            pass

        return Fixed


class PasswordChangeViewSchema(OpenApiViewExtension):
    target_class = "dj_rest_auth.views.PasswordChangeView"
    match_subclasses = True

    def view_replacement(self):
        @extend_schema_view(
            post=extend_schema(
                summary="Change user password",
                description="""Takes empty request body and retrieves the
                access token from the cookie.""",
                examples=[
                    OpenApiExample(
                        "Successful",
                        value={"detail": "New password has been saved."},
                        response_only=True,
                        status_codes=[200],
                    ),
                ],
                responses={
                    200: OpenApiResponse(
                        response=inline_serializer(
                            name="PasswordChangeSerializer",
                            fields={
                                "detail": serializers.CharField(),
                            },
                        )
                    ),
                },
            )
        )
        class Fixed(self.target_class):
            pass

        return Fixed


class RefreshViewSchema(OpenApiViewExtension):
    target_class = "rest_framework_simplejwt.views.TokenRefreshView"
    match_subclasses = True

    def view_replacement(self):
        @extend_schema_view(
            post=extend_schema(
                summary="JWT Token Refresh",
                description="""Takes empty request
                body and retrieves the refresh token from the cookie.
                <br>
                If the access token is valid, it returns an access type
                JSON web token and updates the access token in the cookie""",
                request=OpenApiRequest(
                    request=OpenApiTypes.OBJECT,
                    examples=[OpenApiExample("Body", value="{}")],
                ),
            )
        )
        class Fixed(self.target_class):
            pass

        return Fixed


class VerifyViewSchema(OpenApiViewExtension):
    target_class = "rest_framework_simplejwt.views.TokenVerifyView"
    match_subclasses = True

    def view_replacement(self):
        @extend_schema_view(
            post=extend_schema(
                summary="JWT Token Verify",
                description="""Takes empty request body and retrieves the
                access token from the cookie.
                <br>
                If the access token is valid,
                it returns status code 200 without any extra information""",
                request=OpenApiRequest(
                    request=OpenApiTypes.OBJECT,
                    examples=[OpenApiExample("Body", value="{}")],
                ),
            )
        )
        class Fixed(self.target_class):
            pass

        return Fixed


class UserDetailViewSchema(OpenApiViewExtension):
    target_class = "dj_rest_auth.views.UserDetailsView"
    match_subclasses = True

    def view_replacement(self):
        @extend_schema_view(
            get=extend_schema(
                summary="Get user info",
                description="""Retrieves the
                access token from the cookie.
                <br>
                If the access token is valid,
                it returns user information""",
                request=OpenApiRequest(
                    request=OpenApiTypes.OBJECT,
                    examples=[OpenApiExample("Body", value="{}")],
                ),
            ),
            patch=extend_schema(
                summary="Update user info",
                description="""Retrieves the
                access token from the cookie.
                <br>
                If the access token is valid,
                info will be changed""",
            ),
            put=extend_schema(exclude=True),
        )
        class Fixed(self.target_class):
            pass

        return Fixed
