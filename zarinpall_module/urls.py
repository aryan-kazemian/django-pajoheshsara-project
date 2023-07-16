from django.urls import path
from . import views

urlpatterns = [
    path('<course_name>', views.zarin_pall, name='zarin-pall-page')
]
