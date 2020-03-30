# Create your views here.
from django.http import HttpResponse
from rest_framework import mixins
from rest_framework.permissions import BasePermission
from rest_framework.status import *
from rest_framework.viewsets import GenericViewSet

from lqdoj_backend.paginations import CustomPagination
from submissions.models import Submission
from submissions.serializers import SubmissionSerializer, SubmissionListSerializer


class IsOwnerOrListOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow list request
        if request.method:
            return True

        # If it's modification request, check permission
        if request.auth is None:  # Check token
            return False

        return request.user.is_staff  # Check staff permission


class SubmissionView(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    queryset = Submission.objects.all()
    _paginator = CustomPagination(page_size=10, page_query_param="p")
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        if request.auth is None:
            return HttpResponse(status=HTTP_401_UNAUTHORIZED)
        username = request.user.username
        submission = Submission.objects.get(id=kwargs[self.lookup_field])

        # print(username)
        # print(submission.user.__str__() == username.__str__())

        if submission.user.__str__() == username.__str__():
            return super().retrieve(request, args, kwargs)
        else:
            return HttpResponse(status=HTTP_401_UNAUTHORIZED)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SubmissionSerializer
        return SubmissionListSerializer
