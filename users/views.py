import json

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import forms
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED,
                                   HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.viewsets import ModelViewSet

from lqdoj_backend.json_response import create_message
from lqdoj_backend.settings import *


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, min_length=8, max_length=30)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", 'password1', 'password2')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    """
    Custom retrieve function to retrieve user from username instead of id.
    """

    def retrieve(self, request, *args, **kwargs):
        try:
            user = self.queryset.get(username=kwargs["pk"])
        except User.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        serialized = UserSerializer(user)
        return Response(data=serialized.data, status=HTTP_200_OK)

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
        form = UserRegistrationForm(json.loads(request.body))
        if form.is_valid():  # Check form data
            form.save()
            return Response(status=HTTP_201_CREATED)
        else:
            return Response(data=form.errors, status=HTTP_400_BAD_REQUEST)

    """
    Custom function to handle PATCH request, use to change user password
    """

    def partial_update(self, request, *args, **kwargs):
        if request.auth is None:
            return Response(status=HTTP_401_UNAUTHORIZED)

        try:
            user_from_token = request.user
            request_data = json.loads(request.body)
            username = kwargs["pk"]
        except KeyError:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

        # Check permission
        permission = False
        if user_from_token.username == username:
            permission = True

        if permission:
            # Check old password
            if user_from_token.check_password(request_data['old_password']):
                if request_data['new_password1'] == request_data['new_password2']:
                    user_from_token.set_password(request_data['new_password1'])
                    user_from_token.save()
                else:
                    return Response(data=create_message(MSG_DIFF_NEW_PASS), status=HTTP_400_BAD_REQUEST)
            else:
                return Response(data=create_message(MSG_WRONG_OLD_PASS), status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)

        return Response(status=HTTP_200_OK)
