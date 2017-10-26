from django import forms
from .models import Topiccomment,Topic, Photo, PhotoComment, Message
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.db import models


class CommentForm(forms.ModelForm):
    # content=forms.CharField(label='comment_content',max_length=500)
    class Meta:
        model= Topiccomment
        fields = ['content', ]



class TopicForm(forms.ModelForm):
    class Meta:
        model= Topic
        fields = ['title', 'content']

    # register related

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = ("username", "email")


class photoForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Photo
        fields = ['category', 'photo_name', 'photographer_name', 'photographer_remark', 'image_path']

class photocommentForm(forms.ModelForm):
    class Meta:
        model = PhotoComment
        fields = ['content']

class messageSendForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']
