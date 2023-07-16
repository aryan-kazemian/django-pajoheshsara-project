from django import forms

class RegisterCourseForm(forms.Form):
    father_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': "نام پدر"
    }))
    email = forms.CharField(max_length=300, widget=forms.EmailInput(attrs={
        'placeholder': "ایمیل"
    }))
    kod_meli = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'placeholder': "کد ملی"
    }))

