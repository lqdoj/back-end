from django.forms import ModelForm
from rest_framework import permissions, serializers
from rest_framework import viewsets
from rest_framework.authtoken.models import Token

from lqdoj_backend.paginations import CustomPagination
from lqdoj_backend.settings import *
from .models import Announcement


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


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'


class AnnouncementsView(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = (IsStaffOrReadOnly,)
    _paginator = CustomPagination(page_size=5, page_query_param="p")
