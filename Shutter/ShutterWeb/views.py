from django.shortcuts import render
from django.http import Http404

from .models import Topic

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
    return render(request, 'topic.html', {'topic':topic})
