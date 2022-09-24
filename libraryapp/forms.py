from django import forms
from libraryapp.models import Category, Usermember
from django.contrib.auth.models import User
from . import models


class userform(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']

class categoryform(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'