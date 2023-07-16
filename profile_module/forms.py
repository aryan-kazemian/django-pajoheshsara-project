from django import forms
from django.core.exceptions import ValidationError

from user_module.models import User


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'about_user', 'avatar', 'background_image']
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'about_user': forms.Textarea(),
            'avatar': forms.ClearableFileInput(),
            'background_image': forms.ClearableFileInput()
                }

        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'about_user': 'درباره شخص',
        }

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label='رمز عبور فعلی', error_messages={
        'required': 'این فیلد اجباری است !!!'
    }, widget=forms.PasswordInput(attrs={
        'placeholder': 'لطفا رمز عبور فعلی خود را وارد کنید .'
    }))
    password = forms.CharField(label='رمز عبور جدید', error_messages={
        'required': 'این فیلد اجباری است !!!'
    }, widget=forms.PasswordInput(attrs={
        'placeholder': 'لطفا رمز عبور جدید خود را وارد کنید .'
    }))
    confirm_password = forms.CharField(label='تکرار رمز عبور جدید', error_messages={
        'required': 'این فیلد اجباری است !!!'
    }, widget=forms.PasswordInput(attrs={
        'placeholder': 'لطفا رمز عبور جدید خود را تکرار کنید . '
    }))

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return password
        else:
            raise ValidationError('رمز های عبور باید با هم برابر باشند .')

class ChangeAvatarForm(forms.Form):
    profile_main_image = forms.ImageField()

class ChangeBackgroundImageForm(forms.Form):
    profile_background_image = forms.ImageField()
