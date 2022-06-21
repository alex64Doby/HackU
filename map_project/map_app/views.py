from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.

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
