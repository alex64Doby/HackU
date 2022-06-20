from django.urls import path
from . import views

urlpatterns = [
	#APIのpathを設定する（path, views.api名, name?）
	path('connection', views.connection, name='connection'),
]