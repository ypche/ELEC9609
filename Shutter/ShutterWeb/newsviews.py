from django.shortcuts import render, redirect
from django.http import Http404
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import News, NewsComment


def news_list(request):
    all_news = News.objects.all()
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    # 对所有新闻进行分页
    p = Paginator(all_news, 5, request=request)

    one_news = p.page(page)

    return render(request, 'news_list.html', {
        'all_news': one_news
    })