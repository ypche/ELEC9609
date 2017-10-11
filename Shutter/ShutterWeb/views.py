from django.shortcuts import render

from .models import Topic

def forum(request):
    latest_topic_list=Topic.objects.order_by('-time')[:3]
    context = {'latest_topic_list': latest_topic_list}
    return render(request, 'forum.html', context)

