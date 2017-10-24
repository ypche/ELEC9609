from django.conf.urls import url
from . import views
from . import newsviews


urlpatterns = [
    # forum
    url(r'^forum/$',views.forum, name='forum'),

    # hot topic
    url(r'^hot_topic/$', views.hot_topic, name='hot_topic'),
    url(r'^topic/(?P<topic_id>[0-9]+)/$', views.topic, name='topic'),
    url(r'^add_topic/$', views.add_topic, name='add_topic'),

    # message
    url(r'^inbox/$', views.inbox, name='inbox'),
    url(r'^message_detail/$', views.message_detail, name='message_detail'),

    # news
    url(r'^news/$', newsviews.news_list, name='news_list'),
    url(r'^news_content/$', newsviews.news_content, name='news_content'),
    url(r'^news_list/$', newsviews.news_list, name='news_list'),

    # album
    url(r'^album/scenery/$', views.album_scenery, name='album_scenery'),
    url(r'^album/people/$', views.album_people, name='album_people'),
    url(r'^album/photo/$', views.album_photo, name='album_photo'),
    url(r'^upload_image/$',views.upload_image, name='upload_image'),

    # home page will be redirected to album_scenery.html
    url(r'^$', views.index, name='index'),

    # login,logout,register
    url(r'^login/$', views.user_login, name="login"),
    url(r'^logout/$', views.user_logout, name="logout"),
    url(r'^register/', views.register, name='register'),

]


