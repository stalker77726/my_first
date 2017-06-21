from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^login/$', views.user_login, name='login'),
]