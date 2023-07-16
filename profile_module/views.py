from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from user_module.models import User
from profile_module.forms import EditProfileModelForm, ChangePasswordForm, ChangeAvatarForm, ChangeBackgroundImageForm
from course_module.models import CoursesModel
from django.utils.decorators import method_decorator

@method_decorator(login_required, 'dispatch')
class ProfileView(View):
    def get(self, request):
        user = User.objects.filter(id=request.user.id).first()
        avatar = user.avatar
        background_image = user.background_image
        form = EditProfileModelForm(initial={
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'about_user': user.about_user,
                    'avatar': avatar,
                    'background_image': background_image
                })
        context = {
                'form': form,
                'user': user,
        }
        return render(request, 'profile_module/profile-page.html', context)

    def post(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            name = edit_form.cleaned_data.get('name')
            family = edit_form.cleaned_data.get('family')
            avatar = edit_form.cleaned_data.get('avatar')
            print(avatar)
            background_image = edit_form.cleaned_data.get('background_image')
            about_user = edit_form.cleaned_data.get('about_user')
            if name is not None:
                current_user.first_name = name
            if family is not None:
                current_user.last_name = family
            if avatar is not None:
                current_user.avatar = avatar
            if background_image is not None:
                current_user.background_image = background_image
            if about_user is not None:
                current_user.about_user = about_user
            current_user.save()
            return redirect('profile-page')

        context = {
            'form': edit_form,
            'user': current_user
        }
        return render(request, 'profile_module/profile-page.html', context)

@method_decorator(login_required, 'dispatch')
class ChangePasswordView(View):
    def get(self, request):
        form = ChangePasswordForm
        user = User.objects.filter(id=request.user.id).first()
        context = {
            'form': form,
            'user': user
        }
        return render(request, 'profile_module/profile-chanage-password.html', context)

    def post(self, request):
        user = User.objects.filter(id=request.user.id).first()
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data.get('current_password')
            if user.check_password(current_password):
                new_password = form.cleaned_data.get('password')
                user.set_password(new_password)
                user.save()
                logout(request)
                return redirect(reverse('login-page'))
            else:
                form.add_error('current_password', 'رمز عبور وارد شده اشتباه است !!!')

        context = {
            'form': form,
            'user': user
        }
        return render(request, 'profile_module/profile-chanage-password.html', context)

@login_required
def purchased_courses(request):
    courses = CoursesModel.objects.filter(ownedcoursesuser__user_id=request.user.id)
    context = {
        'courses': courses
    }
    return render(request, 'profile_module/purchased_courses.html', context)


@login_required
def profile_header_component(request):
    context = {

    }
    return render(request, 'profile_module/component/profile-header.html', context)
