from django.shortcuts import render
from django.http import HttpResponse
import json
import hashlib
from more_itertools import first

from requests import request

from sympy import re
# Create your views here.
from .models import Users, Connections

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

	#各都道府県のユーザ数を求める処理
	from django.db.models import Count
	users_num = [0 for i in range(47)]
	#prefecture_idでGroupByを行い,Count(prefecture_id)を実行
	rows = Users.objects.values('prefecture_id').annotate(total = Count('prefecture_id'))
	for row in rows:
		pid = row['prefecture_id']
		num = row['total']
		users_num[pid] = num

	#つながりの個数をN*Mで割る処理
	for i in range(47):
		for j in range(47):
			M = users_num[i]
			N = users_num[j]
			offline_connections[i][j] /= (N * M)
			online_connections[i][j] /= (N * M)

	response = {"offline_connections": offline_connections, "online_connections": online_connections}
	json_response = json.dumps(response, ensure_ascii=False, indent=2)
	return HttpResponse(json_response)


#API:signup
def signup(request):
	req = json.loads(request.body)
	try:	# if exist same id
		Users.objects.get(user_id=req['userId'])
		result = {'status': 400}
	except:	# create new user
		Users.objects.create(user_id=req['userId'],
			user_name=req['userName'], prefecture_id=req['prefectureId'])
		result = {'status': 200}
	return HttpResponse(json.dumps(result))

#API:signin
def signin(request):
	req = json.loads(request.body)
	try:	# if exist user_id
		Users.objects.get(user_id=req['userId'])
		result = {'status': 200}
	except:	# user_id not found
		result = {'status': 400}
	return HttpResponse(json.dumps(result))

#API:connection
def connection(request):
	from .models import Connections,Users
	request = json.loads(request.body)
	UserId1 = request["userId1"]
	UserId2 = request["userId2"]
	mkhash1 = UserId1 + UserId2
	mkhash2 = UserId2 + UserId1
	hs1 = str(hashlib.md5(mkhash1.encode()).hexdigest())
	hs2 = str(hashlib.md5(mkhash2.encode()).hexdigest())
	# connectionMileageテスト用データ(サーバーからデータを取得する処理を実装する)
	frequency = 1
	distance = 13
	point = connectionMileage(request,request["status"],frequency,distance)
	result = {
		"userId1": UserId1,
		"userId2": UserId2,
		"point":point,
	}
	try: # if exist connection_id
		Connections.objects.get(connection_id=hs1)
		result = {"status": 400}
	except: # register to Connections
		UserId1 = Users.objects.get(user_id=UserId1)
		UserId2 = Users.objects.get(user_id=UserId2)
		SaveData1= Connections(connection_id=hs1, user_id1=UserId1, user_id2=UserId2, status=request["status"])
		SaveData2 = Connections(connection_id=hs2, user_id1=UserId2, user_id2=UserId1, status=request["status"])
		SaveData1.save()
		SaveData2.save()
	return HttpResponse(json.dumps(result))

#API:userByPrefecture
#都道府県ごとのユーザ情報を表示
def userByPrefecture(request):
	request = json.loads(request.body)
	prefectureId = request['prefectureId']
	rows = Users.objects.filter(prefecture_id=prefectureId)
	users = [{"userId":row.user_id, "userName":row.user_name, "prefectureId": row.prefecture_id} for row in rows]
	response = {"users": users}
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
		createdBy = str(row.created_by)#DATETIME -> str
		updatedBy = str(row.updated_by)#DATETIME -> str
		point = row.point
		print(userId2, userName, prefectureId)

		if(row.status == "offline"):
			offline_connections_detail[prefectureId].append({"userId": userId2, "userName": userName, "createdBy": createdBy, "updatedBy": updatedBy, "point": point})
			offline_connections[prefectureId] += 1

		if(row.status == "online"):
			online_connections_detail[prefectureId].append({"userId": userId2, "userName": userName, "createdBy": createdBy, "updatedBy": updatedBy, "point": point})
			online_connections[prefectureId] += 1

	#各都道府県のユーザ数を求める処理
	from django.db.models import Count
	users_num = [0 for i in range(47)]

	#prefecture_idでGroupByを行い,Count(prefecture_id)を実行
	rows = Users.objects.values('prefecture_id').annotate(total = Count('prefecture_id'))
	for row in rows:
		pid = row['prefecture_id']
		num = row['total']
		users_num[pid] = num

	#各都道府県に住むユーザ数Nで割る処理
	for i in range(47):
		N = users_num[i]
		offline_connections[i] /= N
		online_connections[i] /= N

	response = {"offline_connections":offline_connections, "online_connections":online_connections,  "offline_connections_detail": offline_connections_detail, "online_connections_detail": online_connections_detail}
	return HttpResponse(json.dumps(response))

def searchUser(request):
	request = json.loads(request.body)
	if 'userIdKey' in request:
		userIdKey = request['userIdKey']
	else:
		userIdKey = ''
	if 'userNameKey' in request:
		userNameKey = request['userNameKey']
	else:
		userNameKey = ''
	if 'prefectureId' in request:
		prefectureId = request['prefectureId']
	else:
		prefectureId = ''
	
	rows = Users.objects.filter(user_id__icontains=userIdKey, user_name__icontains=userNameKey, prefecture_id__iexact=prefectureId)
	users = [{"userId":row.user_id, "userName":row.user_name, "prefectureId": row.prefecture_id, "point": row.point} for row in rows]
	response = {"users": users}
	return HttpResponse(json.dumps(response))

def searchUserByUserIdExactly(request):
	request = json.loads(request.body)
	if 'userIdKey' in request:
		userIdKey = request['userIdKey']
	else:
		userIdKey = ''
	rows = Users.objects.filter(user_id__iexact=userIdKey)
	users = [{"userId":row.user_id, "userName":row.user_name, "prefectureId": row.prefecture_id, "point": row.point} for row in rows]
	response = {"users": users}
	return HttpResponse(json.dumps(response))

def searchConnection(request):
	request = json.loads(request.body)
	if 'userId1Key' in request:
		userId1Key = request['userId1Key']
	else:
		userId1Key = ''
	if 'userId2Key' in request:
		userId2Key = request['userId2Key']
	else:
		userId2Key = ''
	if 'pointGreaterThan' in request:
		pointGreaterThan = request['pointGreaterThan']
	else:
		pointGreaterThan = 0
	if 'pointLessThan' in request:
		pointLessThan = request['pointLessThan']
	else:
		pointLessThan = 1000000

	#[TODO]時間での絞り込み（直近１週間、1ヶ月など）
	if(userId1Key != '' and userId2Key != ''):
		rows = Connections.objects.filter(user_id1__user_id__iexact=userId1Key, user_id2__user_id__iexact=userId2Key, point__gt=pointGreaterThan, point__lt = pointLessThan)
	if(userId1Key != '' and userId2Key == ''):
		rows = Connections.objects.filter(user_id1__user_id__iexact=userId1Key, point__gt=pointGreaterThan, point__lt = pointLessThan)
	if(userId1Key == '' and userId2Key == ''):
		rows = Connections.objects.filter(point__gt=pointGreaterThan, point__lt = pointLessThan)
	
	connections = [{"connectionId": row.connection_id, "userId1":row.user_id1.user_id, "userId2":row.user_id2.user_id, "createdBy": str(row.created_by), "updatedBy": str(row.updated_by), "point": row.point} for row in rows]
	response = {"connections": connections}
	return HttpResponse(json.dumps(response))

# 適当に計算式を実装
# Connection Mileage
def connectionMileage(request,status,frequency,distance):
	# jsonから必要なデータを取得し計算に最適化する処理を記述
	UserId1 = request["userId1"]
	UserId2 = request["userId2"]
	# UserIdから距離や最終connectionを取得
	UserId1 = Users.objects.get(user_id=UserId1)
	UserId2 = Users.objects.get(user_id=UserId2)
	basePt = 10
	statusPt = 0
	firstBonusPt = 0
	frequencyPt = 3
	distancePt = 1
	if status == "offline":
		statusPt = 5
	if frequency == 0:
		firstBonusPt = 5
	elif frequency >= 5:
		frequency *= 2
	distance = int(distance/2)
	if distance > 15:
		distancePt = 3
	elif distance > 10:
		distancePt = 2
	elif distance > 5:
		distancePt = 1
	point = basePt + statusPt + frequencyPt + firstBonusPt + distancePt
	
	return(point)