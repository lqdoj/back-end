import json

from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.forms import forms
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED)
from rest_framework.viewsets import ModelViewSet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "date_joined")


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, min_length=8, max_length=30)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    """
    Retrieve the current user associated with the token. Returns 200 on
    success, 401 if the token is missing.
    """

    @action(detail=False)
    def me(self, request):
        if request.auth is None:  # Check token
            return Response(status=HTTP_401_UNAUTHORIZED)
        user = request.user  # Retrieve user from token
        serialized = UserSerializer(user)
        return Response(data=serialized.data, status=HTTP_200_OK)

    """
    Custom create function to create users, using custom UserRegistrationForm
    """

    def create(self, request, *args, **kwargs):
        form = UserRegistrationForm(data=json.loads(request.body))
        if form.is_valid():  # Check form data
            form.save()
            return Response(status=HTTP_201_CREATED)
        else:
            return Response(data=form.errors, status=HTTP_400_BAD_REQUEST)

    """
    Custom function to handle PATCH request, use to change user password
    """

    def partial_update(self, request, *args, **kwargs):
        form = PasswordChangeForm(data=json.loads(request.body), user=request.user)
        if form.is_valid():
            form.save()
            return Response(status=HTTP_200_OK)
        else:
            return Response(data=form.errors, status=HTTP_400_BAD_REQUEST)

    """
    Custom function to handle PUT request, use to change user infos
    """

    def update(self, request, *args, **kwargs):
        if (request.auth is None) or (request.user.username != kwargs[self.lookup_field]):
            return Response(status=HTTP_401_UNAUTHORIZED)
        form = CustomUserChangeForm(data=json.loads(request.body), instance=request.user)
        if form.is_valid():
            form.save()
            return Response(status=HTTP_200_OK)
        else:
            return Response(data=form.errors, status=HTTP_400_BAD_REQUEST)
