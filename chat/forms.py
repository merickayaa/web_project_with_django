from django import forms
from .models import Thread,Message


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class':'w-100 form-control'}))

class MessageForm(forms.Form):
    message = forms.CharField(label='', max_length=1000, widget=forms.TextInput(attrs={'class':'form-control', 'style':'width: 100% !important;'}))