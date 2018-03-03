from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.index),
	url(r'^signin$', views.signin),
	url(r'^log$', views.log),
	url(r'^create$', views.create),
	url(r'^register$', views.register),
	url(r'^home$', views.home),
	url(r'^profile$', views.profile),
	url(r'^edit$', views.edit),
	url(r'^update$', views.update),
	url(r'^upload$', views.upload),
	url(r'^dislike$', views.dislike),
	url(r'^like$', views.like),
	url(r'^logout$', views.logout),
	url(r'^matches$', views.matches),
	url(r'^newmatch$', views.newmatch),
	url(r'^thread/(?P<tid>\d+)$', views.thread),
	url(r'^pstmsg$', views.pstmsg),
	url(r'^savemap$', views.savemap),
	url(r'^upload$', views.upload),
	url(r'^cartest$', views.cartest),
]