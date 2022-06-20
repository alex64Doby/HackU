from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

#API:all
def all(request):
	result =  'show all node'
	return HttpResponse(result)

#API:signup
def signup(request):
	request = {
   "userId": "testId2",
   "userName": "testName",
   "prefectureId": 0,
}
	userid = request["userId"]
	userName = request["userName"]
	prefectureid = request["prefectureId"]
	# result =  'signup'
	from .models import Users
	Users.objects.create(user_id=userid, user_name=userName, prefecture_id=prefectureid)
	result = Users.objects.all()
	return HttpResponse(result)

#API:connection
def connection(request):
	result =  'Accept connection'
	return HttpResponse(result)
