from django.urls import path
from . import views
urlpatterns = [
    path('<page>', views.news_list, name='news-list-page'),
    path('news/<news>', views.news_detail, name='news-detail-page')
]
