from django import forms
from .models import Topiccomment,Topic


class CommentForm(forms.ModelForm):
    class Meta:
        model= Topiccomment
        fields = ['content', ]



class TopicForm(forms.ModelForm):
    class Meta:
        model= Topic
        fields = ['title', 'content']