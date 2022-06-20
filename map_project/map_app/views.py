from django.shortcuts import render
from django.http import HttpResponse
import hashlib

from requests import request

from sympy import re
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
#既に繋がっている人の処理を考える
def connection(request):
	request = {
		"userId1":"user_id3",
		"userId2":"user_id4", 
		"status":"status",
	}
	userId1 = request["userId1"]
	userId2 = request["userId2"]
	status = request["status"]
	mkhash = userId1 + userId2
	hs = str(hashlib.md5(mkhash.encode()).hexdigest())
	from .models import Connections
	Connections.objects.create(user_id1=userId1, user_id2=userId2, status=status, connection_id=hs)
	result = Connections.objects.filter(connection_id=hs)
	return HttpResponse(result)