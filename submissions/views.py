from django.shortcuts import render


# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from submissions.models import Submission


class SubmissionView(ModelViewSet):
    queryset = Submission.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"


