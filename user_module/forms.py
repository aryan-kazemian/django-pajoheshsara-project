from user_module.models import User
from django import forms
from django.db import models
from django.core.exceptions import ValidationError

class GradeChoices(models.TextChoices):
    Preschool = ("Preschool", "پیش دبستانی")
    first_grade = ("first_grade", "اول")
    second_grade = ("second_grade", "دوم")
    third_grade = ("third_grade", "سوم")
    fourth_grade = ("fourth_grade", "چهارم")
    fifth_grade = ("fifth_grade", "پنجم")
    sixth_grade = ("sixth_grade", "ششم")
    seventh_grade = ("seventh_grade", "هفتم")
    eighth_grade = ("eighth_grade", "هشتم")
    ninth_grade = ("ninth_grade", "نهم")
    tenth_grade = ("tenth_grade", "دهم")
    eleventh_grade = ("eleventh_grade", "یازدهم")
    twelfth_grade = ("twelfth_grade", "دوازدهم")

class RegisterForm(forms.Form):
    name = forms.CharField(label='نام', min_length=3, error_messages={
        'required': 'این فیلد اجباری است !'
    }, widget=forms.TextInput())
    family = forms.CharField(label=' نام خانوادگی', min_length=3,  error_messages={
        'required': 'این فیلد اجباری است !'
    }, widget=forms.TextInput())
    phone_number = forms.CharField(label='شماره تماس', error_messages={
        'required': 'این فیلد اجباری است !'
    }, widget=forms.TextInput())
    username = forms.CharField(label='نام کاربری', min_length=3, error_messages={
        'required': 'این فیلد اجباری است !!!'
    }, widget=forms.TextInput())
    home_phone_number = forms.CharField(label='تلفن خانه', min_length=7, error_messages={
        'required': 'این فیلد اجباری است !!!'
    }, widget=forms.TextInput())
    school = forms.CharField(label='مدرسه', min_length=3, error_messages={
        'required': 'این فیلد اجباری است !!!'
    }, widget=forms.TextInput())
    kode_meli = forms.CharField(label='کد ملی', error_messages={
        'required': 'این فیلد اجباری است !!!'
    }, widget=forms.TextInput())
    grade = forms.ChoiceField(choices=GradeChoices.choices, label='پایه تحصیلی')
    day_birthday = forms.IntegerField(max_value=31, min_value=1, widget=forms.NumberInput(), label='روز تولد')
    month_birthday = forms.IntegerField(max_value=12, min_value=1, widget=forms.NumberInput(), label='ماه تولد')
    year_birthday = forms.IntegerField(widget=forms.NumberInput(), label='سال تولد')
    password = forms.CharField(label='رمز عبور ', min_length=10, error_messages={
        'required': 'این فیلد اجباری است !!!'
    }, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='تکرار رمز', min_length=10, error_messages={
        'required': 'این فیلد اجباری است !!!'
    }, widget=forms.PasswordInput())

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return password
        else:
            raise ValidationError('رمز های عبور باید با هم برابر باشند .')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'نام کاربری'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'رمز عبور'
    }))


class EnterSecurityCod(forms.Form):
    security_cod = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        'placeholder': "کد 4 رقمی"
    }))


class EnterUsername(forms.Form):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'placeholder': "نام کاربری "
    }))


class ChangePasswordForm(forms.Form):
    password = forms.CharField(label='رمز عبور ', error_messages={
        'required': 'این فیلد اجباری است !!!'
    }, widget=forms.PasswordInput(attrs={
        'placeholder': 'رمز عبور'
    }), min_length=10)
    confirm_password = forms.CharField(label='تکرار رمز عبور', error_messages={
        'required': 'این فیلد اجباری است !!!'
    }, widget=forms.PasswordInput(attrs={
        'placeholder': 'تکرار رمز عبور '
    }), min_length=10)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return password
        else:
            raise ValidationError('رمز های عبور باید با هم برابر باشند .')