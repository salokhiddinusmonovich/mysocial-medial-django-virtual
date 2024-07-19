from django.forms import ModelForm
from .models import *
from crispy_forms.helper import FormHelper
from django import forms
from crispy_forms.layout import Layout, Button, Submit


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]
        labels = {
            'realname': 'Name'
        }
        widgets = {
            'image': forms.FileInput(),
            'bio': forms.Textarea(attrs={'rows': 3})
        }


class SupportMeForm(forms.ModelForm):
    class Meta:
        model = SupportMe
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'author',
            'message',
            Submit('submit', 'Buy', css_class='mt-1')
        )