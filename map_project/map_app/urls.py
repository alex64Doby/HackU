from django.urls import path
from . import views

urlpatterns = [
	#APIのpathを設定する（path, views.api名, name?）
	path('connection', views.connection, name='connection'),
	path('all', views.all, name='all'),
	path('signup', views.signup, name='signup'),
	path('userByPrefecture', views.userByPrefecture, name= 'userByPrefecture')
]