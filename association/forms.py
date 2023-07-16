from django import forms

class SearchBoxForm(forms.Form):
    search_box = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': "جست و جو"
    }))
