from django.shortcuts import render
from .models import NewsModel
from functions.functions import *

# Create your views here.

paginate_by = 3

def news_list(request, page):
    news = NewsModel.objects.filter(is_active=True).all()
    index = int(int(page) - 1)
    all_news = make_grope(news, paginate_by)[index]
    has_other_pages = False
    current_page = int(page)
    page_count = int(len(news) / paginate_by + 1)
    page_range = range(1, page_count)
    if len(all_news) < len(news):
        has_other_pages = True
    has_previous = False
    has_next = True
    previous_page_number = int(page) - 1
    next_page_number = int(page) + 1
    if int(page) > 1:
        has_previous = True
    last_page = int(len(news)) / paginate_by
    if float(page) >= float(last_page):
        has_next = False
    context = {
        'news': all_news,
        'has_other_page': has_other_pages,
        'current_page': current_page,
        'page_range': page_range,
        'has_previous': has_previous,
        'previous_page_number': previous_page_number,
        'has_next': has_next,
        'next_page_number': next_page_number,
    }
    return render(request, 'news_module/news-list.html', context)

def news_detail(request, news):
    news = NewsModel.objects.get(url_title__iexact=news)
    context = {
        'news': news
    }
    return render(request, 'news_module/news-detail.html', context)
