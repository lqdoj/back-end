from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .json_response import *


@api_view(["POST"])
def register_handle(request):
    data = json.loads(request.body)['data']
    form = UserCreationForm(data)

    if form.is_valid():
        form.save()
        return Response(data=create_message("User created successfully"), status=status.HTTP_201_CREATED)
    else:
        return Response(data=create_message(form.errors), status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_handle(request):
    data = json.loads(request.body)['data']
    form = AuthenticationForm(data=data)

    if form.is_valid():
        user = form.get_user()
        token, created = Token.objects.get_or_create(user=user)
        print(created)
        return Response(data=create_message(token.key), status=status.HTTP_200_OK)
    else:
        return Response(data=create_message(form.errors), status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def logout_handle(request):
    token = request.headers.get("LQDOJ-TOKEN")
    try:
        Token.objects.get(key=token).delete()
    except Exception as exp:
        print(exp)
    else:
        print("Logout " + token)
    finally:
        return Response(status=200)
