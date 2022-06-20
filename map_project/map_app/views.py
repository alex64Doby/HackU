from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

#API:all
def all(request):
	result =  'show all node'
	return HttpResponse(result)

#API:signup
def signup(request):
	result =  'signup'
	return HttpResponse(result)

#API:connection
def connection(request):
	result =  'Accept connection'
	return HttpResponse(result)