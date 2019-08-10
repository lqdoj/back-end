from django.contrib.auth.forms import AuthenticationForm
from rest_framework.status import *
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from lqdoj_backend.json_response import *
from lqdoj_backend.settings import *
from .forms import UserRegistrationForm

from .serializers import UserSerializer


@api_view(["POST"])
def register_handle(request):
    data = json.loads(request.body)['data']
    form = UserRegistrationForm(data)

    if form.is_valid():
        form.save()
        return Response(data=create_message(MSG_USER_CREATED), status=HTTP_201_CREATED)
    else:
        return Response(data=create_message(form.errors), status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_handle(request):
    data = json.loads(request.body)['data']
    form = AuthenticationForm(data=data)

    if form.is_valid():
        user = form.get_user()
        token, created = Token.objects.get_or_create(user=user)
        return Response(data=create_message(token.key), status=HTTP_200_OK)
    else:
        return Response(data=create_message(form.errors), status=HTTP_400_BAD_REQUEST)


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


@api_view(["GET"])
def check_token_handle(request):
    try:
        token = request.headers.get(HEADER_TOKEN)
        user = Token.objects.get(key=token).user
        serializer = UserSerializer(user)
    except:
        return Response(status=HTTP_404_NOT_FOUND)
    if user.is_active:
        return Response(data=serializer.data, status=HTTP_200_OK)
    else:
        return Response(status=HTTP_404_NOT_FOUND)
