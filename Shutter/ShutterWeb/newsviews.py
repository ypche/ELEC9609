from django.shortcuts import render,get_object_or_404
from django.http import Http404
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import News, NewsComment



def news_list(request):
    all_news = News.objects.all()
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(all_news, 5, request=request)

    one_news = p.page(page)

    return render(request, 'news_list.html', {
        'all_news': one_news
    })

def news_content(request, news_id):
    news = News.objects.get(pk=news_id)
    context = {'news':news}
    return render(request,'news_content.html', context)
