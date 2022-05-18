import logging

from django.core.exceptions import PermissionDenied
from django.http import Http404

from rest_framework.views import set_rollback
from rest_framework import exceptions
from rest_framework.response import Response

from rest_framework_simplejwt.exceptions import InvalidToken

logger = logging.getLogger(__name__)


def exception_handler(exc, context):
    # handler was rewritten in order to provide error codes
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    elif isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        if isinstance(exc, InvalidToken):
            data = exc.detail
        elif isinstance(exc.detail, list):
            data = [{"detail": s, "code": s.code} for s in exc.detail]
        elif isinstance(exc.detail, dict):
            data = {e: [{"detail": s, "code": getattr(s, "code", "")} for s in exc.detail[e]] for e in exc.detail}
        else:
            data = {"non_field_errors": {"detail": exc.detail, "code": exc.default_code}}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None
