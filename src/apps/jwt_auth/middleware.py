import json

from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from config.settings import REST_AUTH


# The decision to add these middleware classes on January 22, 2024, was based
# on a solution found in the GitHub issue #97 of the dj-rest-auth repository
# https://github.com/iMerica/dj-rest-auth/issues/97
# The purpose of adding these middleware classes is to address an issue
# related to calling certain endpoints that use the simple_jwt library. The
# issue arises because simple_jwt expects the token to be passed in the
# request body, but when using HTTP-only cookies, the token data is sent in
# the request headers instead. To solve this issue, the provided middleware
# classes (MoveJWTCookieIntoTheBody) are
# implemented. These middleware classes intercept the requests and modify
# them to move the token data from the request headers to the request body.
class MoveJWTCookieIntoTheBody(MiddlewareMixin):
    """
    for Django Rest Framework JWT's POST "/token-verify" endpoint --- check
    for an access token in the request.COOKIES and if, add it to the body
    payload.
    """

    def __init__(self, get_response):  # noqa
        self.get_response = get_response

    def __call__(self, request):
        # sourcery skip: inline-immediately-returned-variable
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        # sourcery skip: remove-pass-body, remove-redundant-pass,
        # swap-if-else-branches
        if (
            request.path == reverse("auth:token-verify")
            and REST_AUTH["JWT_AUTH_COOKIE"] in request.COOKIES
        ):
            if request.body != b"":
                data = json.loads(request.body)
                data["token"] = request.COOKIES[REST_AUTH["JWT_AUTH_COOKIE"]]
                request._body = json.dumps(data).encode("utf-8")
            else:
                # I cannot create a body if it is not passed so the client
                # must send '{}'
                pass

        return None
