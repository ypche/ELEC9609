from django.conf.urls import url
from . import views
from . import newsviews


urlpatterns = [
    # home page will be redirected to album_scenery_new.html
    url(r'^$', views.index, name='index'),

    # forum
    url(r'^forum/$',views.forum, name='forum'),
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
    url(r'^album/$', views.album_scenery_new, name='album_scenery_new'),
    url(r'^album/scenery/new/$', views.album_scenery_new, name='album_scenery_new'),
    url(r'^album/scenery/hot/$', views.album_scenery_hot, name='album_scenery_hot'),
    url(r'^album/people/new/$', views.album_people_new, name='album_people_new'),
    url(r'^album/people/hot/$', views.album_people_hot, name='album_people_hot'),
    url(r'^album/photo/(\d+)/$', views.album_photo, name='album_photo'),
    #url(r'^album/photo/$', views.album_photo, name='album_photo'),
    url(r'^album/upload_image/$', views.album_upload_image, name='album_upload_image'),

    # login,logout,register
    url(r'^login/$', views.user_login, name="login"),
    url(r'^logout/$', views.user_logout, name="logout"),
    url(r'^register/', views.register, name='register'),

]


