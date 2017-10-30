from django.shortcuts import render,get_object_or_404
from django.http import Http404
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import News, NewsComment
from .forms import NewsCommentForm




def news_list(request):
    all_news = News.objects.all().order_by("-time")
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
    try:
        news = News.objects.get(pk=news_id)
    except News.DoesNotExist:
        raise Http404("Topic does not exist")
    if request.method == 'GET':
        NewsCommentForm.author = request.user
        form = NewsCommentForm(request.POST)
    else:
        NewsCommentForm.author = request.user
        form = NewsCommentForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            clean_data['topic']= news
            news.author = request.user
            NewsComment.objects.create(**clean_data )
    context = {
        'news':news,
        'NewsComments':news.newscomment_set.all().order_by('-time'),
        'form': form
    }
    return render(request,'news_content.html', context)
