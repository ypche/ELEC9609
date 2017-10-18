# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
from json import loads, dumps

from TestModel.models import Test
from TestModel.models import User

 
# 数据库操作
def testdb(request):
    test1 = Test(name='runoob')
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")

# 数据库操作
def userdb(request):
    test1 = User(name='runoob', password='123')
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")

def getuserdb(request):
     if request.method == 'GET' :
       list = User.objects.all()
       newlist=[]
       print(list)
       for user in list:
         dic = {}
         key='uname'
         uvalue=user.name
         dic[key]=uvalue
         key1='upassword'
         kvalue=user.password
         dic[key1]=kvalue
         newlist.append(dic)
       jstr = dumps(newlist)
       return HttpResponse(jstr, content_type='application/json')
    