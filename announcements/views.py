from rest_framework import viewsets

from .models import Announcement
from lqdoj_backend.serializers import AnnouncementSerializer
from lqdoj_backend.permissions import IsStaffOrReadOnly
from lqdoj_backend.paginations import CustomPagination


class AnnouncementsView(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = (IsStaffOrReadOnly,)
    _paginator = CustomPagination(page_size=5, page_query_param="p")
