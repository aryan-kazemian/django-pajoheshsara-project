from django.urls import path
from . import views

urlpatterns = [
    path('', views.teachers_list, name='teachers-list-page'),
    path('teacher-profile/<username>', views.teacher_profile, name='teacher-profile-page'),
    # path('teacher-profile/chat/<username>', views.ChatView.as_view(), name='chat-page')
]