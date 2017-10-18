from django.conf.urls import *
from . import view,testdb
 
urlpatterns = [
    url(r'^hello$', view.hello),
    url(r'^calendar$', view.calendar),
    url(r'^login$', view.login),
    url(r'^testdb$', testdb.testdb),
    #url(r'^trydb$', trydb.trydb),
    url(r'^userdb$', testdb.userdb),
    url(r'^getuserdb$', testdb.getuserdb),
]