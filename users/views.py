from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json


data = {
	'username' : '',
	'password' : '',
	'email': ''
}


# Create your views here.
@api_view(["POST"])
def register(request):
	# username = request.body
	print(request.body.decode('utf-8'))
	data = {
		'params' : request.body.decode('utf-8')
	}
	return Response(data, status=200)