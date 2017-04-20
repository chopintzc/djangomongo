'''
Created on Jan 18, 2017
url controllers

@author: Zhongchao
'''

from django.conf.urls import patterns, url
from django.views.generic import TemplateView
#from views import PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, TagListView, PostSearchView
from views import *

urlpatterns = patterns('',
	url(r'^search/$', PostSearchView.as_view(), name='post-search'),
	url(r'^add/$', PostCreateView.as_view(), name='post-create'),
	url(r'^topics/$', AddTopicView.as_view(), name='add-topics'),
	url(r'^load/$', LoadfileView.as_view(), name='load-file'),
	url(r'^select/$', SelectTopicView.as_view(), name='select-topics'),
	url(r'^profile/$', ProfileView.as_view(), name='researcher'),
	url(r'^profile/(?P<pk>[\w\d]+)/$', ProfileView.as_view(), name='researcher-profile'),
	url(r'^(?P<pk>[\w\d]+)/$', PostDetailView.as_view(), name='post-detail'),
	url(r'^(?P<pk>[\w\d]+)/edit/$', PostUpdateView.as_view(), name='post-update'),
	url(r'^(?P<pk>[\w\d]+)/delete/$', PostDeleteView.as_view(), name='post-delete'),
	url(r'^add/get_topics/(?P<pk>[\w\d\s]+)/$', 'blog.views.get_topics', name='get_topics'),
	url(r'^([\w\d]+)/edit/get_topics/(?P<pk>[\w\d\s]+)/$', 'blog.views.get_topics', name='get_topics'),
	url(r'^select/get_choices/(?P<pk>[\w\d\s]+)/$', 'blog.views.get_topics', name='get_choices'),
	url(r'^profile/get_choices/(?P<pk>[\w\d\s]+)/$', 'blog.views.get_topics', name='get_profilechoices'),
	url(r'^profile/([\w\d]+)/get_choices/(?P<pk>[\w\d\s]+)/$', 'blog.views.get_topics', name='get_profilechoices'),
	#url(r'^select/get_choices/(?P<pk>[\w\d\s]+)/$', 'blog.views.get_choices', name='get_choices'),
	#url(r'^profile/get_choices/(?P<pk>[\w\d\s]+)/$', 'blog.views.get_profilechoices', name='get_profilechoices'),
	#url(r'^profile/([\w\d]+)/get_choices/(?P<pk>[\w\d\s]+)/$', 'blog.views.get_profilechoices', name='get_profilechoices'),
	url(r'^profile/([\w\d]+)/get_abstract/(?P<pk>[\w\d\s\W]+)/$', 'blog.views.get_abstract', name='get_abstract'),
	url(r'^profile/([\w\d]+)/get_image/(?P<author>[\w\d\s]+)/(?P<filter>[\w\d\s\W]*)/$', 'blog.views.get_image', name='get_image'),
	url(r'^profile/([\w\d]+)/get_title/(?P<pk>[\w\d\s\W]+)/$', 'blog.views.get_title', name='get_title'),
)
