from rest_framework import permissions
from rest_framework.authtoken.models import Token

from lqdoj_backend.settings import *


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            token = request.headers.get(HEADER_TOKEN)
            user = Token.objects.get(key=token).user
        except:
            return request.method in permissions.SAFE_METHODS
        if user.is_staff:
            return True
        else:
            return request.method in permissions.SAFE_METHODS
