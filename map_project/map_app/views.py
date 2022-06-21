from django.shortcuts import render
from django.http import HttpResponse
import json
import hashlib

from requests import request

from sympy import re
# Create your views here.
from .models import Users

#API:all
def all(request):
	result = 'ok'
	from .models import Connections, Users
	offline_connection_with_pid = Connections.objects.filter(status='offline')
	online_connection_with_pid = Connections.objects.filter(status='online')
	offline_pid = [(data.user_id1.prefecture_id, data.user_id2.prefecture_id) for data in offline_connection_with_pid]
	online_pid = [(data.user_id1.prefecture_id, data.user_id2.prefecture_id) for data in online_connection_with_pid]
	offline_connections = [[0] * 47] * 47
	online_connections = [[0] * 47] * 47
	for id1, id2 in offline_pid:
		offline_connections[id1][id2] += 1
	for id1, id2 in online_pid:
		online_connections[id1][id2] += 1
	response = {"offline_connections": offline_connections, "online_connections": online_connections}
	json_response = json.dumps(response, ensure_ascii=False, indent=2)
	return HttpResponse(json_response)


#API:signup
def signup(request):
	try:
		Users.objects.get(user_id=request["userId"])
		result = {"status": 400}
	except:
		Users.objects.create(user_id=request["userId"],
			user_name=request["userName"], prefecture_id=request["prefectureId"])
		result = {"status": 200}
	return HttpResponse(json.dumps(result))


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
