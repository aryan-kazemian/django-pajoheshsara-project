from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from user_module.models import User
from course_module.models import CoursesModel
from django.views import View
from .models import ChatModel
from django.utils.decorators import method_decorator
from .forms import ChatForm
import jalali_date



def teachers_list(request):
    teachers = User.objects.filter(groups=1).all()
    context = {
        'teachers': teachers
    }
    return render(request, 'teachers_module/teachers-list.html', context)

def teacher_profile(request, username):
    teacher = User.objects.get(username__iexact=username)
    courses = CoursesModel.objects.filter(teacher__username__iexact=username).all()
    context = {
        'teacher': teacher,
        'courses': courses,
        'courses_count': len(courses)
    }
    return render(request, 'teachers_module/teacher-profile.html', context)

# @method_decorator(login_required, 'dispatch')
# class ChatView(View):
#     def get(self, request, username):
#         chats = ChatModel.objects.filter(teacher=username, user_id=request.user.id).all()
#         teacher = User.objects.get(username__iexact=username)
#         form = ChatForm
#         context = {
#             'username': username,
#             'chats': chats,
#             'teacher': teacher,
#             'form': form
#         }
#         return render(request, 'teachers_module/chat-page.html', context)
#
#     def post(self, request, username):
#         form = ChatForm(request.POST)
#         if form.is_valid():
#             text = form.cleaned_data.get('text')
#             new_chat = ChatModel(teacher=username, user=request.user, sender='user', text=text)
#             new_chat.save()
#
#         teacher = User.objects.get(username__iexact=username)
#         chats = ChatModel.objects.filter(teacher=username, user_id=request.user.id).all()
#         form = ChatForm
#         context = {
#             'username': username,
#             'chats': chats,
#             'teacher': teacher,
#             'form': form
#         }
#         return render(request, 'teachers_module/chat-page.html', context)
