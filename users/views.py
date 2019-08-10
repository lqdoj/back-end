from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from lqdoj_backend.json_response import *
from lqdoj_backend.settings import *


@api_view(["POST"])
def register_handle(request):
    data = json.loads(request.body)['data']
    form = UserCreationForm(data)

    if form.is_valid():
        form.save()
        return Response(data=create_message(MSG_USER_CREATED), status=status.HTTP_201_CREATED)
    else:
        return Response(data=create_message(form.errors), status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_handle(request):
    data = json.loads(request.body)['data']
    form = AuthenticationForm(data=data)

    if form.is_valid():
        user = form.get_user()
        token, created = Token.objects.get_or_create(user=user)
        return Response(data=create_message(token.key), status=status.HTTP_200_OK)
    else:
        return Response(data=create_message(form.errors), status=status.HTTP_400_BAD_REQUEST)


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
