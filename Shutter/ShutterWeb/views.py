from django.shortcuts import render, redirect
from django.http import Http404
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.db import connection
from .models import Topic, Topiccomment, Message, Photo
from .forms import CommentForm, TopicForm, RegisterForm, photoForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.utils import timezone

# index, index.html will be redirect to album_scenery_new
def index(request):
    return HttpResponseRedirect("album/scenery/new")

def forum(request):
    latest_topic_list=Topic.objects.order_by('-time')
    paginator = Paginator(latest_topic_list, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        latest_topic = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_topic = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_topic = paginator.page(paginator.num_pages)
    context = {'latest_topic': latest_topic}
    return render(request, 'forum.html', context)


def hot_topic(request):
    latest_topic_list=Topic.objects.order_by('-remarks')
    paginator = Paginator(latest_topic_list, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        latest_topic = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_topic = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_topic = paginator.page(paginator.num_pages)
    context = {'latest_topic': latest_topic}
    return render(request, 'hot_topic.html', context)

# View topic detail and add comment
def topic(request, topic_id):
    try:
        topic = Topic.objects.get(pk=topic_id)
        topic.increase_views()
    except Topic.DoesNotExist:
        raise Http404("Topic does not exist")
    if request.method == 'GET':
        form = CommentForm(request.POST)
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            clean_data['topic']= topic
            Topiccomment.objects.create(**clean_data)
            topic.increase_remarks()

    context = {
        'topic': topic,
        'TopicComments':topic.topiccomment_set.all().order_by('-time'),
        'form': form
    }
    return render(request,'topic.html', context)



def add_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
                # file is saved
            form.save()
            return redirect('/ShutterWeb/forum')
    else:
        form = TopicForm()
    return render(request, 'add_topic.html', {'form': form})

def inbox(request):
    if 'messageSortByDate' in request.POST:
        message_list = Message.objects.raw('SELECT * FROM ShutterWeb_message'
                                           ' where author_id = %s or receiver_id = %s'
                                           ' order by time desc' % ('1', '1'))
    elif 'messageSortByUnread' in request.POST:
        message_list = Message.objects.raw('SELECT * FROM ShutterWeb_message'
                                           ' where author_id = %s or receiver_id = %s'
                                           ' and readflag = %s'
                                           ' order by time desc' % ('1', '1', 'UNREAD'))
    elif 'messageSortByFT' in request.POST:
        message_list = Message.objects.raw('SELECT * FROM ShutterWeb_message'
                                           ' where author_id = %s or receiver_id = %s'
                                           ' order by author_id' % ('1', '1'))
    else:
        message_list = Message.objects.raw('SELECT * FROM ShutterWeb_message'
                                           ' where author_id = %s or receiver_id = %s'
                                           ' order by time desc' % ('1', '1'))
    paginator = Paginator(message_list, 5)  # Show 5 messages per page
    paginator.count = len(list(message_list))

    page = request.GET.get('page')
    try:
        latest_message = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_message = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_message = paginator.page(paginator.num_pages)
    context = {'latest_message': latest_message}
    # context = {'latest_message': message_list}
    return render(request, 'inbox.html', context)

def message_detail(request):
    return render(request, 'message_detail.html')


# album
def album_scenery_new(request):
    return render(request, 'album_scenery_new.html')
<<<<<<< HEAD

def album_scenery_hot(request):
    return render(request, 'album_scenery_hot.html')

def album_people_new(request):
    return render(request, 'album_people_new.html')

def album_photo(request):
    return render(request, 'album_photo.html')

=======
def album_scenery_hot(request):
    return render(request, 'album_scenery_hot.html')
def album_people_new(request):
    return render(request, 'album_people_new.html')
def album_people_hot(request):
    return render(request, 'album_people_hot.html')
def album_photo(request):
    return render(request, 'album_photo.html')

def album_upload_image(request):###
    if request.method == 'POST':
        form = photoForm(request.POST,request.FILES)
        if form.is_valid():
            if 'docfile' in request.FILES:
                image = request.FILES["docfile"]
                image.name = str(request.user)+str(timezone.now())+'.jpg'
                s=Photo(photographer_name=request.user,image_path=image)
                s.save()
                HttpResponse('successful')
                return redirect('/ShutterWeb/')
            else:
                return redirect('/ShutterWeb/')
        else:

            image_path = None
            return HttpResponse('fail')
    else:
        return render(request,'album_upload_image.html')



def album_scenery_hot(request):
    return render(request, 'album_scenery_hot.html')

def album_people_new(request):
    return render(request, 'album_people_new.html')

def album_photo(request):
    return render(request, 'album_photo.html')


>>>>>>> e4ce2a2fe11a88db4d6e6c5717bbe649ba13240a


def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username","")
        pass_word = request.POST.get("password","")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request,user)
            return render(request, "album_scenery.html")
        else:
            return render(request,"login.html",{})
    elif request.method == "GET":
        return render(request, "login.html",{})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/ShutterWeb")

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/ShutterWeb")
    else:
        form = RegisterForm()
    return render(request, 'register.html', context={'form': form})
