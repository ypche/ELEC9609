from django import forms
from .models import Topiccomment,Topic


class CommentForm(forms.ModelForm):
    # content=forms.CharField(label='comment_content',max_length=500)
    class Meta:
        model= Topiccomment
        fields = ['content', ]



class TopicForm(forms.ModelForm):
    class Meta:
        model= Topic
        fields = ['title', 'content']