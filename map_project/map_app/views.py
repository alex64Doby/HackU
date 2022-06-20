from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import Users

#API:all
def all(request):
	result =  'show all node'
	return HttpResponse(result)

#API:signup
def signup(request):
	try:
		Users.objects.get(user_id=request["userId"])
		result = {"status": 400}
	except:
		Users.objects.create(user_id=request["userId"],
			user_name=request["userName"], prefecture_id=request["prefectureId"])
		result = {"status": 200}
	return HttpResponse(result)

#API:connection
def connection(request):
	result =  'Accept connection'
	return HttpResponse(result)
