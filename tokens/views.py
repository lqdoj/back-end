import json

from django.contrib.auth import authenticate

from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet


class IsAuthenticatedOrCreateOnly(BasePermission):
    def has_permission(self, request, view):
        print(request.method)
        if request.method == "POST":
            return True
        if (request.method != "POST") and (request.method != "DELETE"):
            return False
        print(request.method)
        if request.method == "POST":
            return True
        if request.auth is None:
            return request.method == "POST"
        else:
            return request.user is not None


class TokenView(mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    permission_classes = [IsAuthenticatedOrCreateOnly]
    queryset = Token.objects.all()

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response(data={'token': token.key}, status=HTTP_200_OK)
            else:
                return Response(status=HTTP_400_BAD_REQUEST)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            token = request.auth
            Token.objects.get(key=token).delete()
            return Response(status=HTTP_200_OK)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)
