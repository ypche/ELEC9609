from django import forms
from .models import Topiccomment

class CommentForm(forms.ModelForm):
    class Meta:
        model= Topiccomment
        fields = ['content', ]