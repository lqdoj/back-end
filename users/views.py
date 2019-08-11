import json

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import forms
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED)
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

    @action(detail=False)
    def me(self, request):
        try:
            token = request.headers.get(HEADER_TOKEN)
            user = Token.objects.get(key=token).user
            serialized = UserSerializer(user)
            return Response(data=serialized.data, status=HTTP_200_OK)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        form = UserRegistrationForm(json.loads(request.body))
        if form.is_valid():
            form.save()
            return Response(data=create_message(MSG_USER_CREATED), status=HTTP_201_CREATED)
        else:
            return Response(data=form.errors, status=HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        print("Received update request")
        received_token = request.headers.get(HEADER_TOKEN)
        user_from_token = Token.objects.get(key=received_token).user
        user_from_request = json.loads(request.body)

        # Check permission
        permission = False
        if user_from_token.is_staff or (user_from_token.username == user_from_request['username']):
            permission = True

        if permission:
            # Check old password
            if user_from_token.check_password(user_from_request['old_password']):
                if user_from_request['new_password1'] == user_from_request['new_password2']:
                    user_from_token.set_password(user_from_request['new_password1'])
                    user_from_token.save()
                else:
                    return Response(data=create_message(MSG_DIFF_NEW_PASS), status=HTTP_400_BAD_REQUEST)
            else:
                return Response(data=create_message(MSG_WRONG_OLD_PASS), status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)

        return Response(status=HTTP_200_OK)
