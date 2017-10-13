from django.shortcuts import render, redirect
from django.http import Http404


from .models import Topic, Topiccomment
from .forms import CommentForm

def forum(request):
    latest_topic_list=Topic.objects.order_by('-time')[:3]
    context = {'latest_topic_list': latest_topic_list}
    return render(request, 'forum.html', context)

def hot_topic(request):
    latest_topic_list=Topic.objects.order_by('-remarks')[:3]
    context = {'latest_topic_list': latest_topic_list}
    return render(request, 'hot_topic.html', context)

def topic(request, topic_id):
    try:
        topic = Topic.objects.get(pk=topic_id)
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
    context = {
        'topic': topic,
        'TopicComments':topic.topiccomment_set.all().order_by('-time'),
        'form': form
    }
    return render(request,'topic.html', context)




