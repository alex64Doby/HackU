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
	offline_connections = [[0 for j in range(47)] for i in range(47)]
	online_connections = [[0 for j in range(47)] for i in range(47)]
	for id1, id2 in offline_pid:
		offline_connections[id1][id2] += 1
	for id1, id2 in online_pid:
		online_connections[id1][id2] += 1
	response = {"offline_connections": offline_connections, "online_connections": online_connections}
	json_response = json.dumps(response, ensure_ascii=False, indent=2)
	return HttpResponse(json_response)


#API:signup
def signup(request):
	request = json.loads(request.body)
	try:
		Users.objects.get(user_id=request['userId'])
		result = {'status': 400}
	except:
		Users.objects.create(user_id=request['userId'],
			user_name=request['userName'], prefecture_id=request['prefectureId'])
		result = {'status': 200}
	return HttpResponse(json.dumps(result))

#API:connection
#既に繋がっている人の処理を考える
def connection(request):
	from .models import Connections,Users
	request = json.loads(request.body)
	UserId1 = request["userId1"]
	UserId2 = request["userId2"]
	mkhash = UserId1 + UserId2
	hs = str(hashlib.md5(mkhash.encode()).hexdigest())
	# エラーチェック用(既に存在するデータ)
	# hs = "86cbce9d-b046-4c12-bb5a-b90ba73c"
	try:
		Connections.objects.get(connection_id=hs)
		result = {"status": 400}
	except:
		# エラー発生中(1行目と2~3行目は同じ処理内容)
		# Connections.objects.create(connection_id=hs ,user_id1=request["userId1"] ,user_id2=request["userId2"],status=request["status"])
		# SaveData = Connections(connection_id=hs ,user_id1=UserId1 ,user_id2=UserId2,status=request["status"])
		# SaveData.save()
		result = {
		"connection_id": hs,
		"userId1": UserId1,
		"userId2": UserId2,
		}
	return HttpResponse(json.dumps(result))

#API:userByPrefecture
#都道府県ごとのユーザ情報を表示
def userByPrefecture(request):
	request = json.loads(request.body)
	prefectureId = request['prefectureId']
	rows = Users.objects.filter(prefecture_id=prefectureId)
	response = [{"userId":row.user_id, "userName":row.user_name} for row in rows]
	return HttpResponse(json.dumps(response))

#API:connectionByUser
#ユーザごとのつながりを表示
def connectionByUser(request):
	request = json.loads(request.body)
	userId = request['userId']

	from .models import Connections
	rows = Connections.objects.filter(user_id1 = userId)

	offline_connections_detail = [[] for i in range(47)]
	online_connections_detail = [[] for i in range(47)]

	offline_connections = [0 for i in range(47)]
	online_connections = [0 for i in range(47)]

	for row in rows:
		userId2 = row.user_id2.user_id
		userName = row.user_id2.user_name
		prefectureId = row.user_id2.prefecture_id
		print(userId2, userName, prefectureId)

		if(row.status == "offline"):
			offline_connections_detail[prefectureId].append({"userId": userId2, "userName": userName})
			offline_connections[prefectureId] += 1

		if(row.status == "online"):
			online_connections_detail[prefectureId].append({"userId": userId2, "userName": userName})
			online_connections[prefectureId] += 1

	response = {"offline_connections":offline_connections, "online_connections":online_connections,  "offline_connections_detail": offline_connections_detail, "online_connections_detail": online_connections_detail}
	return HttpResponse(json.dumps(response))
		