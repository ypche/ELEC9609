from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^forum/$',views.forum, name='forum'),
    url(r'^hot_topic/$', views.hot_topic, name='hot_topic'),
    url(r'^topic/(?P<topic_id>[0-9]+)/$', views.topic, name='topic'),
    url(r'^add_topic/$', views.add_topic, name='add_topic'),
    url(r'^inbox/$', views.inbox, name='inbox'),
    url(r'^message_detail/$', views.message_detail, name='message_detail'),
    url(r'^news/$', views.news_list, name='news_list'),

]

