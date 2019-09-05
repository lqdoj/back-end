from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from tasks.models import Task
from tasks.serializers import TaskListSerializer, TaskSerializer


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow all readonly request
        if request.method in permissions.SAFE_METHODS:
            return True

        # If it's modification request, check permission
        if request.auth is None:  # Check token
            return False

        return request.user.is_staff  # Check staff permission


class TaskView(ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = (IsStaffOrReadOnly,)

    """
    Override get_serializer_class(self) function to specify what serializer will be used
    """

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskSerializer
        return TaskListSerializer
