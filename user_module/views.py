from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import User
from .forms import RegisterForm, EnterSecurityCod, LoginForm, EnterUsername, ChangePasswordForm
from django.utils.crypto import get_random_string
from functions.functions import compare_date_time
from django.contrib import messages
import random
import datetime


class RegisterView(View):
    def get(self, request):
        form = RegisterForm
        context = {
            'form': form
        }
        return render(request, 'account_module/register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        is_username_error = 0
        if form.is_valid():
            messages.success(request, 'Success')
            username = form.cleaned_data.get('username')
            user: bool = User.objects.filter(username__iexact=username).exists()
            if user is False:
                form_phone_number = form.cleaned_data.get('phone_number')
                home_phone_number = form.cleaned_data.get('home_phone_number')
                grade = form.cleaned_data.get('grade')
                name = form.cleaned_data.get('name')
                family = form.cleaned_data.get('family')
                day_birthday = form.cleaned_data.get('day_birthday')
                month_birthday = form.cleaned_data.get('month_birthday')
                year_birthday = form.cleaned_data.get('year_birthday')
                kode_meli = form.cleaned_data.get('kode_meli')
                school = form.cleaned_data.get('school')
                birthday = str(year_birthday) + "-" + str(month_birthday) + "-" + str(day_birthday)
                new_user = User(
                        first_name=name,
                        last_name=family,
                        username=username,
                        phone_number=form_phone_number,
                        home_phone_number=home_phone_number,
                        user_random_cod=random.randint(1000, 9999),
                        is_active=False,
                        user_random_string=get_random_string(72),
                        grade=grade,
                        kode_meli=kode_meli,
                        birthday=birthday,
                        school=school,
                    )
                password = form.cleaned_data.get('password')
                confirm_password = form.cleaned_data.get('confirm_password')
                if password == confirm_password:
                    new_user.set_password(password)
                    new_user.save()
                    return redirect('security-cod-page', str(username))
                else:
                    form.add_error(confirm_password, 'رمز های عبور با هم تطابق ندارند !!!')
            else:
                is_username_error += 1

            if is_username_error == 1:
                context = {
                    'form': form,
                    'dose_it_has_username_error': True
                }
                return render(request, 'account_module/register.html', context)

        else:
            messages.error(request, 'Wrong Captcha !')
            context = {
                'form': form
            }
            return render(request, 'account_module/register.html', context)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'account_module/login.html', context)

    def post(self, request):
        form_information = LoginForm(request.POST)
        is_error = 0
        if form_information.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user: User = User.objects.filter(username__iexact=username).first()
            if user is not None:
                if user.is_active is True:
                    check_password = user.check_password(password)
                    if check_password:
                        login(request, user)
                        return redirect(reverse('profile-page'))
                    else:
                        is_error += 1
                else:
                    return redirect('security-cod-page', username=username)
            if not user:
                is_error += 1
        if is_error > 0:
            context = {
                'form': form_information,
                'error': 'کاربری با این مشخصات وجود ندارد !!!'
            }
            return render(request, 'account_module/login.html', context)
        else:
            return redirect('index-page')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login-page'))


class GetSecurityCodView(View):
    def get(self, request, username):
        # todo: send active cod to phone number
        user = User.objects.get(username__iexact=username)
        miss_cod_time = user.missed_cod_time
        if miss_cod_time is not None:
            current_time = str(datetime.datetime.now())
            compared_time = compare_date_time(current_time, miss_cod_time)
            if compared_time == miss_cod_time:
                return redirect('security-cod-after-4-missed-cod-page', username, miss_cod_time)
            else:
                form = EnterSecurityCod
                context = {
                    'form': form,
                    'username': username,
                }
                return render(request, 'account_module/security-cod.html', context)
        else:
            form = EnterSecurityCod
            context = {
                'form': form,
                'username': username,
            }
            return render(request, 'account_module/security-cod.html', context)

    def post(self, request, username):
        user = User.objects.get(username__iexact=username)
        user_random_cod_on_database = user.user_random_cod
        form = EnterSecurityCod(request.POST)
        if form.is_valid():
            entered_cod = form.cleaned_data.get('security_cod')
            if entered_cod == user_random_cod_on_database:
                user.is_active = True
                user.user_random_cod = random.randint(1000, 9999)
                user.save()
                return redirect('login-page-alert', 'check-number')

            else:
                user.missed_cod += 1
                user.save()
                if user.missed_cod > 4:
                    current_date_time = datetime.datetime.now()
                    hour = int(str(current_date_time)[11:13]) + 1
                    next_hour = str(current_date_time)[0:11] + str(hour) + str(current_date_time)[13:]
                    user.missed_cod_time = str(next_hour)
                    user.save()
                    return redirect('security-cod-after-4-missed-cod-page', username, next_hour)

                error_text = 'کد وارد شده نادرست می باشد !!!'
                context = {
                    'error_text': error_text,
                    'dose_it_has_error': True,
                    'form': EnterSecurityCod,
                    'username': username
                    }
                return render(request, 'account_module/security-cod.html', context)


class GetSecurityCodAfterMissedCodsView(View):
    def get(self, request, username, time):
        full_time = User.objects.get(username__iexact=username).missed_cod_time
        time = time[10:19]
        current_time = str(datetime.datetime.now())
        context = {
            'time':  time,
            'username': username,
            'full_time': full_time,
            'current_time': current_time,
        }
        return render(request, 'account_module/check-phone-number-missed.html', context)

    def post(self, request, username, time):
        current_time = str(datetime.datetime.now())
        user = User.objects.get(username__iexact=username)
        time = user.missed_cod_time
        compare_time = compare_date_time(current_time, time)
        if compare_time == current_time:
            user = User.objects.get(username__iexact=username)
            user.missed_cod = 0
            user.user_random_cod = random.randint(1000, 9999)
            user.save()
            return redirect('security-cod-page', username)
        else:
            full_time = time
            time = time[10:19]
            context = {
                'time':  time,
                'username': username,
                'full_time': full_time
            }
            return render(request, 'account_module/check-phone-number-missed.html', context)


class GetUsernameView(View):
    def get(self, request):
        form = EnterUsername
        context = {
            'form': form
        }
        return render(request, 'account_module/get-username-before-get-cod-forgot-password.html', context)

    def post(self, request):
        form = EnterUsername(request.POST)
        if form.is_valid():
            user = User.objects.filter(username=form.cleaned_data.get('username')).first()
            if not user:
                form.add_error('username', 'کاربری با این نام کاربری پیدا نشد !!!')
                context = {
                    'form': form
                }
                return render(request, 'account_module/get-username-before-get-cod-forgot-password.html', context)
            else:
                username = form.cleaned_data.get('username')
                return redirect('forgot-password-page', username=username)
        context = {
            'form': form
        }
        return render(request, 'account_module/get-username-before-get-cod-forgot-password.html', context)


class ForgotPasswordView(View):
    def get(self, request, username):
        # todo: send active cod to phone number
        user = User.objects.get(username__iexact=username)
        miss_cod_time = user.missed_cod_time
        if miss_cod_time is not None:
            current_time = str(datetime.datetime.now())
            compared_time = compare_date_time(current_time, miss_cod_time)
            if compared_time == miss_cod_time:
                return redirect('forgot-password-missed-cods-page', username, miss_cod_time)
            else:
                form = EnterSecurityCod
                context = {
                    'form': form,
                    'username': username,
                }
                return render(request, 'account_module/get-random-cod-before-change-password.html', context)
        else:
            form = EnterSecurityCod
            context = {
                'form': form,
                'username': username,
            }
            return render(request, 'account_module/get-random-cod-before-change-password.html', context)

    def post(self, request, username):
        form = EnterSecurityCod(request.POST)
        user = User.objects.get(username__iexact=username)
        user_random_cod_on_database = user.user_random_cod
        if form.is_valid():
            entered_cod = form.cleaned_data.get('security_cod')
            if entered_cod == user_random_cod_on_database:
                user.is_active = True
                user.user_random_cod = random.randint(1000, 9999)
                user.save()
                return redirect('change-password-page', user.user_random_string)
            else:
                user.missed_cod += 1
                user.save()
                if user.missed_cod > 4:
                    print('----------------------------------------- false')
                    current_date_time = datetime.datetime.now()
                    hour = int(str(current_date_time)[11:13]) + 1
                    next_hour = str(current_date_time)[0:11] + str(hour) + str(current_date_time)[13:]
                    user.missed_cod_time = str(next_hour)
                    user.save()
                    return redirect('forgot-password-missed-cods-page', username, next_hour)

                error_text = 'کد وارد شده نادرست می باشد !!!'
                context = {
                    'error_text': error_text,
                    'dose_it_has_error': True,
                    'form': EnterSecurityCod,
                    'username': username
                    }
                return render(request, 'account_module/get-random-cod-before-change-password.html', context)


class ForgotPasswordAfterMissedCodsView(View):
    def get(self, request, username, time):
        full_time = User.objects.get(username__iexact=username).missed_cod_time
        time = time[10:19]
        current_time = str(datetime.datetime.now())
        context = {
            'time':  time,
            'username': username,
            'full_time': full_time,
            'current_time': current_time,
        }
        return render(request, 'account_module/check-phone-number-missed-password.html', context)

    def post(self, request, username, time):
        current_time = str(datetime.datetime.now())
        user = User.objects.get(username__iexact=username)
        time = user.missed_cod_time
        compare_time = compare_date_time(current_time, time)
        if compare_time == current_time:
            user = User.objects.get(username__iexact=username)
            user.missed_cod = 0
            user.user_random_cod = random.randint(1000, 9999)
            user.save()
            return redirect('forgot-password-page', username)
        else:
            full_time = time
            time = time[10:19]
            context = {
                'time':  time,
                'username': username,
                'full_time': full_time
            }
            return render(request, 'account_module/check-phone-number-missed-password.html', context)


class ChangePassword(View):
    def get(self, request, string):
        form = ChangePasswordForm
        context = {
            'form': form,
            'string': string
        }
        return render(request, 'account_module/change-password.html', context)

    def post(self, request, string):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            if not password == confirm_password:
                form.add_error('password', 'رمز های عبور باید با هم یکسان باشند')
                context = {
                    'form': form,
                    'string': string
                }
                return render(request, 'account_module/change-password.html', context)
            else:
                user = User.objects.filter(user_random_string__iexact=string).first()
                user.set_password(password)
                user.user_random_string = get_random_string(72)
                user.save()
                return redirect('login-page')

        context = {
            'form': form,
            'string': string
        }
        return render(request, 'account_module/change-password.html', context)


class LoginAlertView(View):
    def get(self, request, alert):
        check_number = None
        if alert == 'check-number':
            check_number = True
        form = LoginForm()
        context = {
            'form': form,
            'check_number': check_number
        }
        return render(request, 'account_module/login.html', context)

    def post(self, request):
        form_information = LoginForm(request.POST)
        is_error = 0
        if form_information.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user: User = User.objects.filter(username__iexact=username).first()
            if user is not None:
                check_password = user.check_password(password)
                if check_password:
                    login(request, user)
                    return redirect(reverse('index-page'))
                else:
                    is_error += 1
            if not user:
                is_error += 1
        if is_error > 0:
            context = {
                'form': form_information,
                'error': 'کاربری با این مشخصات وجود ندارد !!!'
            }
            return render(request, 'account_module/login.html', context)
        else:
            return redirect('index-page')