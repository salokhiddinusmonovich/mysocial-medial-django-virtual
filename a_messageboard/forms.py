from django.forms import ModelForm
from django import forms
from .models import *


class MessageCreateForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Post a message ...', 'class': 'p-4 text-black', 'maxlength': '2000'})
        }