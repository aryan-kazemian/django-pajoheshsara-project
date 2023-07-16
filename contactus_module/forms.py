from django import forms

class ContactUsForm(forms.Form):
    name = forms.CharField(label='نام', max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'نام'
    }))
    subject = forms.CharField(label='نام خانوادگی', max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'موضوع'
    }))
    text = forms.CharField(label="درباره ی من", widget=forms.Textarea(attrs={
        'placeholder': "پیام"
    }))
