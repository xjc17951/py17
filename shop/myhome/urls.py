from django.conf.urls import url
from django.contrib import admin
from . views import index_views,list_views,info_views
urlpatterns = [
    url(r'^$', index_views.index,name='myhome_index'),

    url(r'^login/$', index_views.myhome_login,name='myhome_login'),
    url(r'^register/$', index_views.myhome_register,name='myhome_register'),
    url(r'^sendmsg/$', index_views.sendmsg,name='myhome_sendmsg'),
    


    # list
    url(r'^list/$', list_views.myhome_list,name='myhome_list'),
    url(r'^info/$', info_views.myhome_info,name='myhome_info'),

 
   
]