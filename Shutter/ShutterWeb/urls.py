from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^forum/$',views.forum, name='forum'),
    url(r'^topic/(?P<topic_id>[0-9]+)/$', views.topic, name='topic'),

]

