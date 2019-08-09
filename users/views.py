from django.contrib.auth.forms import UserCreationForm
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .json_response import *


@api_view(["POST"])
def register(request):
    data = json.loads(request.body)['data']
    form = UserCreationForm(data)

    if form.is_valid():
        form.save()
        return Response(create_message("User created successfully"), status=status.HTTP_201_CREATED)
    else:
        return Response(create_message(form.errors), status=status.HTTP_400_BAD_REQUEST)