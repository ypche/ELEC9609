from django import forms
from .models import Topiccomment,Topic
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


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

class photoForm(forms.Form):
    image = forms.ImageField(required=False)

