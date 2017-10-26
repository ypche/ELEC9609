from django.shortcuts import render, redirect
from django.http import Http404
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.db import connection
from .models import Topic, Topiccomment, Message, Photo
from .forms import CommentForm, TopicForm, RegisterForm, photoForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.utils import timezone
from django.views.generic.base import View


# index, index.html will be redirect to album_scenery_new
def index(request):
    return HttpResponseRedirect("album/scenery/new")

def forum(request):
    latest_topic_list=Topic.objects.order_by('-time')
    paginator = Paginator(latest_topic_list, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    print(page)
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

    newest_photo_list = Photo.objects.order_by('-time')
    #print(newest_photo_list)
    # 9 photos per page
    paginator = Paginator(newest_photo_list, 3)
    page = request.GET.get('page')
    #print(page)
    try:
        newest_photos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        newest_photos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        newest_photos = paginator.page(paginator.num_pages)
    #print(page)
    context = {'newest_photos': newest_photos}
    return render(request, 'album_scenery_new.html', context)

def album_scenery_hot(request):
    return render(request, 'album_scenery_hot.html')
def album_people_new(request):
    return render(request, 'album_people_new.html')
def album_people_hot(request):
    return render(request, 'album_people_hot.html')

def album_photo(request, photo_id):
    context = {'photo_id': photo_id}
    return render(request, 'album_photo.html', context)

# upload photo
def album_upload_image(request):
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

def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username","")
        pass_word = request.POST.get("password","")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request,user)
            return render(request, "album_people_new.html")
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


class UserinfoView(View):
    def get(self,request):
        return  render(request, 'user_profile.html',{})

from django.shortcuts import render, redirect
from django.http import Http404
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.db import connection
from .models import Topic, Topiccomment, Message, Photo, PhotoComment
from .forms import CommentForm, TopicForm, RegisterForm, photoForm, photocommentForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.utils import timezone
from . import filters
from django.contrib.auth.decorators import login_required

# index, index.html will be redirect to album_scenery_new
def index(request):
    return HttpResponseRedirect("album/scenery/new")

def forum(request):
    latest_topic_list=Topic.objects.order_by('-category').order_by('-time')
    paginator = Paginator(latest_topic_list, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    print(page)
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
@login_required(login_url='/ShutterWeb/login')
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
            Topiccomment.author=request.user
            topic.increase_remarks()

    context = {
        'topic': topic,
        'TopicComments':topic.topiccomment_set.all().order_by('-time'),
        'form': form
    }
    return render(request,'topic.html', context)


@login_required(login_url='/ShutterWeb/login')
def add_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            form=form.save(commit=False)
            form.author = request.user
            # author=request.user
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
    # filter out all scenery photos (category = 1) and order by time
    newest_scenery_photos_list = Photo.objects.filter(category=1).order_by('-time')
    # 9 photos per page
    paginator = Paginator(newest_scenery_photos_list, 9)
    page = request.GET.get('page')
    try:
        newest_scenery_photos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        newest_scenery_photos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        newest_scenery_photos = paginator.page(paginator.num_pages)
    photos_list = newest_scenery_photos
    context = {'newest_scenery_photos': newest_scenery_photos, 'photos_list': photos_list}
    #return render(request, 'album_scenery_new.html', context)
    return render(request, 'album.html', context)


def album_scenery_hot(request):
    # filter out all scenery photos (category = 1) and order by time
    hottest_scenery_photos_list = Photo.objects.filter(category=1).order_by('-thumbs_up_number')
    # 9 photos per page
    paginator = Paginator(hottest_scenery_photos_list, 9)
    page = request.GET.get('page')
    try:
        hottest_scenery_photos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        hottest_scenery_photos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        hottest_scenery_photos = paginator.page(paginator.num_pages)
    photos_list = hottest_scenery_photos
    context = {'hottest_scenery_photos': hottest_scenery_photos, 'photos_list': photos_list}
    #return render(request, 'album_scenery_hot.html', context)
    return render(request, 'album.html', context)


def album_people_new(request):
    # filter out all scenery photos (category = 1) and order by time
    newest_people_photos_list = Photo.objects.filter(category=2).order_by('-time')
    # 9 photos per page
    paginator = Paginator(newest_people_photos_list, 9)
    page = request.GET.get('page')
    try:
        newest_people_photos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        newest_people_photos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        newest_people_photos = paginator.page(paginator.num_pages)
    photos_list = newest_people_photos
    context = {'newest_people_photos': newest_people_photos, 'photos_list': photos_list}
    #return render(request, 'album_people_new.html', context)
    return render(request, 'album.html', context)


def album_people_hot(request):
    # filter out all scenery photos (category = 1) and order by time
    hottest_people_photos_list = Photo.objects.filter(category=2).order_by('-thumbs_up_number')
    # 9 photos per page
    paginator = Paginator(hottest_people_photos_list, 9)
    page = request.GET.get('page')
    try:
        hottest_people_photos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        hottest_people_photos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        hottest_people_photos = paginator.page(paginator.num_pages)
    photos_list = hottest_people_photos
    context = {'hottest_people_photos': hottest_people_photos, 'photos_list': photos_list}
    #return render(request, 'album_people_hot.html', context)
    return render(request, 'album.html', context)


def album_photo(request, photo_id):
    photo=Photo.objects.filter(id=int(photo_id))
    this_photo=photo[0]
    image_path = this_photo.image_path
    photo_name = this_photo.photo_name
    photographer_remark = this_photo.photographer_remark
    category = this_photo.category
    thumbs_up_number = this_photo.thumbs_up_number
    photocomment_set=PhotoComment.objects.filter( photo_id = photo_id)

    # some algorithm to get image_path from photo_id
    if request.method == 'POST':
        form = photocommentForm(request.POST)
        #return HttpResponse('successful!')
        if form.is_valid():
            content=form.cleaned_data['content']
            s=PhotoComment()
            s.content=content
            s.photo_id = photo_id
            s.save()
            #return HttpResponse('successful!')
        else:
            return HttpResponse('fail!')

    else:
        form = photocommentForm()
    context = {
        'photo_id': photo_id,
        'PhotoComment': photocomment_set.all().order_by('-time'),
        'form': form,
        'image_path': image_path,
        'thumbs_up_number': thumbs_up_number,
        'photo_name': photo_name,
        'photographer_remark': photographer_remark,
        'category': category,
    }

    return render(request, 'album_photo.html', context)


# upload photo
def album_upload_image(request):
    if request.method == 'POST':
        form = photoForm(request.POST, request.FILES)
        if form.is_valid():
            if 'docfile' in request.FILES:
                image = request.FILES["docfile"]
                image.name = str(timezone.now()) + '.jpg'
                category = form.cleaned_data['category']
                photo_name = form.cleaned_data['photo_name']
                photographer_name = form.cleaned_data['photographer_name']
                photographer_remark = form.cleaned_data['photographer_remark']
                s = Photo(image_path=image, thumbs_up_number=0)
                s.category = category
                s.photo_name = photo_name
                s.photographer_name = photographer_name
                s.photographer_remark = photographer_remark
                s.save()
                #return HttpResponse('successful!')
                return redirect('/ShutterWeb/album/photo/'+ str(s.id))
            else:
                return HttpResponse('fail 123')
        else:
            image_path = None
            return HttpResponse('fail')
    else:
        form = photoForm()
        return render(request, 'album_upload_image.html', {'form': form})


def thumbs_up(request, photo_id):
    photo = Photo.objects.filter(id=photo_id)
    this_photo = photo[0]
    this_photo.increase_thumbs_up()
    return redirect('/ShutterWeb/album/photo/' + str(this_photo.id))

def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username","")
        pass_word = request.POST.get("password","")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request,user)
            return render(request, "album_people_new.html")
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

