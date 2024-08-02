from django import forms
from .models import *

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','password']   

class LoginForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

class VideostoreForm(forms.ModelForm):

    class Meta:

        model=Videostore

        fields=['title','description','video']


class EditvideoForm(forms.ModelForm):

    class Meta:

           model=Videostore

           fields=['title','description','video']

 

class EditCustomUserForm(forms.ModelForm):

    class Meta:

        model=CustomUser

        fields=['username','bio','image']


class CommentForm(forms.ModelForm):

    class Meta:

        model=Comment
        fields=['comment']
        