from django.conf.urls import url
from . import views
from . import newsviews


urlpatterns = [
    url(r'^forum/$',views.forum, name='forum'),
    url(r'^hot_topic/$', views.hot_topic, name='hot_topic'),
    url(r'^topic/(?P<topic_id>[0-9]+)/$', views.topic, name='topic'),
    url(r'^add_topic/$', views.add_topic, name='add_topic'),
    url(r'^inbox/$', views.inbox, name='inbox'),
    url(r'^message_detail/$', views.message_detail, name='message_detail'),
    url(r'^news/$', newsviews.news_list, name='news_list'),
    url(r'^news_content/$', newsviews.news_content, name='news_content'),
    url(r'^news_list/$', newsviews.news_list, name='news_list'),

    # scenery and people of album
    url(r'^album_scenery/$', views.album_scenery, name='album_scenery'),
    url(r'^album_people/$', views.album_people, name='album_people'),
    # home page
    url(r'^$', views.album_scenery, name='home'),

]

