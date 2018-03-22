from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	#url()
	url(r'^$', views.home, name='home'),
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
	#quand on met /mydashboard avec rien, ça nous met la liste de report
    url(r'^dashboard/$', views.report_list, name='report_list'),
    #Quand on met /mydashboard/1, ça nous met les report detail pour le report 1
    url(r'^dashboard/report/(?P<pk>\d+)/$', views.report_detail, name='report_detail'),
    #Quand on met /post/new, ça nous met propose de créer un nouveau post
    url(r'^dashboard/report/new/$', views.report_new, name='report_new'),
    #Quand on met /post/1/edit/ ça nous propose d'éditer le post 1
    url(r'^dashboard/report/(?P<pk>\d+)/edit/$', views.report_edit, name='report_edit'),
    url(r'^api/chart/data/$', views.ChartData.as_view()),
]

