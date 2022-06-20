from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

#API:connection
def connection(request):
	result =  'Accept connection'
	return HttpResponse(result)