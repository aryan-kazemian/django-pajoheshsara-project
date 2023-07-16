from django import forms

class ChatForm(forms.Form):
    text = forms.CharField(max_length=500, widget=forms.TextInput(attrs={
        'placeholder': "متن",
        'class': "write_msg"
    }))