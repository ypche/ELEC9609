
from django.shortcuts import render, redirect
from django.http import Http404
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.db.models import Q
from .models import Topic, Topiccomment, Message, Photo, PhotoComment, UserProfile
from .forms import CommentForm, TopicForm, RegisterForm, photoForm, photocommentForm, messageSendForm,UserInfoForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.utils import timezone
from . import filters
from django.contrib.auth.decorators import login_required
from django.shortcuts import render



from django.core.exceptions import ObjectDoesNotExist


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

@login_required(login_url='/ShutterWeb/login')
def inbox(request):
    if 'messageSortByDate' in request.POST:
        message_list = Message.objects.filter(Q(author=request.user)|Q(receiver=request.user)).order_by('-time')
    elif 'messageSortByUnread' in request.POST:
        message_list = Message.objects.filter((Q(author=request.user)|Q(receiver=request.user))&Q(readflag='UNREAD'))
        message_list = message_list.order_by('-time')
    elif 'messageSortByFT' in request.POST:
        message_list = Message.objects.filter(Q(author=request.user)|Q(receiver=request.user)).order_by('author')
    elif 'messageSend' in request.POST:
        # print(request.POST)
        form = messageSendForm(request.POST)
        if form.is_valid():
            try:
                receiver = UserProfile.objects.get(username=request.POST['receiver'])
                message = Message()
                message.author = request.user
                message.receiver = receiver
                message.content = form.cleaned_data['content']
                message.save()
            except ObjectDoesNotExist:
                print('no user admin')
            # form.author = request.user
            # form.save()
        message_list = Message.objects.filter(Q(author=request.user)|Q(receiver=request.user)).order_by('-time')
    else:
        message_list = Message.objects.filter(Q(author=request.user)|Q(receiver=request.user)).order_by('-time')
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

@login_required(login_url='/ShutterWeb/login')
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

@login_required(login_url='/ShutterWeb/login')
def album_photo(request, photo_id):
    photo=Photo.objects.filter(id=int(photo_id))
    this_photo=photo[0]
    image_path = this_photo.image_path
    photo_name = this_photo.photo_name
    photographer_name = this_photo.photographer_name
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
        'photographer_name': photographer_name,
        'photographer_remark': photographer_remark,
        'category': category,
    }

    return render(request, 'album_photo.html', context)


# upload photo
@login_required(login_url='/ShutterWeb/login')
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


def delete_photo(request, photo_id):
    this_photo=Photo.objects.get(id = photo_id)
    this_photo.delete()
    return render(request,'delete_photo.html',{})



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
            return render(request, "album.html")
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


def Userinfo(request):
    return  render(request, 'user_profile.html',{})

def editprofile(request):
    user_info_form = UserInfoForm(request.POST, instance=request.user)
    if user_info_form.is_valid():
        user_info_form.save()
        return HttpResponseRedirect("/ShutterWeb/info")
    else:
        user_info_form = UserInfoForm()
    return render(request, 'edit_profile.html', context={'user_info_form': user_info_form})




