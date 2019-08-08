from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
import json


def create_message(status, message):
	data = {
		'status' : status,
		'message' : message
	}

	return json.dumps(data)


def exist_user(username):
	return User.objects.filter(username=username).exists()

def create_user(username, password, email):
	return User.objects.create_user(username=username, email=email, password=password)


@api_view(["POST"])
def register(request):

	# parse request params

	data = json.loads(request.body)['data']
	username = data['user_name']
	password = data['password']
	email = data['email']

	# check user existence

	if exist_user(username):
		return Response(data=create_message("fail", "User existed"), status=200)

	# create user
	try:
		user = create_user(username, password, email)
	except error:
		return Response(data=create_message("fail", "Error: " + error), status=200)
	
	return Response(data=create_message("success", "User created"), status=200)
