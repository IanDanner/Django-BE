from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^list_quotes$', views.list_quotes),    
    url(r'^new_quote$', views.new_quote),    
    url(r'^add_like/(?P<id>\d+)$', views.add_like),
    url(r'^remove_like/(?P<id>\d+)$', views.remove_like),
    url(r'^view_user/(?P<id>\d+)$', views.view_user),  
]