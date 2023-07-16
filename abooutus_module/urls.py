from django.urls import path
from . import views

urlpatterns = [
    path('', views.AboutUsTemplateView.as_view(), name='aboutus-page')
]