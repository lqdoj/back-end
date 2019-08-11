from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ModelViewSet

from lqdoj_backend.serializers import UserSerializer
from lqdoj_backend.settings import *


@api_view(["POST"])
def logout_handle(request):
    try:
        token = request.headers.get(HEADER_TOKEN)
        Token.objects.get(key=token).delete()
    except Exception as exp:
        print(exp)
    else:
        print(token)
    finally:
        return Response(status=200)


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
