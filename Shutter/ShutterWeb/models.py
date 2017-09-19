from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20, null=True)
    gender = models.CharField(max_length=1, null=True)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=20, null=True)
    authorization = models.CharField(max_length=10, null=True)
    pquestion1 = models.CharField(max_length=200, null=True)
    panswer1 = models.CharField(max_length=200, null=True)
    pquestion2 = models.CharField(max_length=200, null=True)
    panswer2 = models.CharField(max_length=200, null=True)
    remarks = models.CharField(max_length=500, null=True)

class Message(models.Model):
    author = models.ForeignKey('User', related_name='Message_Author', on_delete=models.CASCADE)
    receiver = models.ForeignKey('User', related_name='Message_Receiver', on_delete=models.CASCADE)
    content = models.CharField(max_length=500, null=True)
    time = models.DateTimeField(default=timezone.now)
    remarks = models.CharField(max_length=500, null=True)

class Topic(models.Model):
    title = models.CharField(max_length=100, null=True)
    content = models.CharField(max_length=500, null=True)
    time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('User', related_name='Topic_Author', on_delete=models.CASCADE)
    remarks = models.CharField(max_length=500, null=True)

class TopicComment(models.Model):
    topic = models.ForeignKey('Topic', related_name='TopicComment_Topic', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('self', related_name='TopicComment_Comment', on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=500, null=True)
    time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('User', related_name='TopicComment_Author', on_delete=models.CASCADE)
    remarks = models.CharField(max_length=500, null=True)

class News(models.Model):
    title = models.CharField(max_length=100, null=True)
    content = models.CharField(max_length=500, null=True)
    time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('User', related_name='News_Author', on_delete=models.CASCADE)
    remarks = models.CharField(max_length=500, null=True)

class NewsComment(models.Model):
    topic = models.ForeignKey('News', related_name='NewsComment_Topic', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('self', related_name='NewsComment_Comment', on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=500, null=True)
    time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('User', related_name='NewsComment_Author', on_delete=models.CASCADE)
    remarks = models.CharField(max_length=500, null=True)

class Photo(models.Model):
    author = models.ForeignKey('User', related_name='Photo_Author', on_delete=models.CASCADE)
    photo_path = models.FilePathField(null=True)
    thumbs_up_number = models.IntegerField(null=True)
    category = models.CharField(max_length=20, null=True)
    time = models.DateTimeField(default=timezone.now)
    remarks = models.CharField(max_length=500, null=True)

class PhotoComment(models.Model):
    author = models.ForeignKey('User', related_name='PhotoComment_Author', on_delete=models.CASCADE)
    photo = models.ForeignKey('Photo', related_name='PhotoComment_Photo', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('self', related_name='PhotoComment_Comment', on_delete=models.CASCADE, null=True)
    thumbs_up_number = models.IntegerField(null=True)
    thumbs_down_number = models.IntegerField(null=True)
    time = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=500, null=True)
    remarks = models.CharField(max_length=500, null=True)