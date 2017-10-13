from django.db import models
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20, null=True)
    gender = models.CharField(max_length=1, null=True, default='U')
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=20, null=True)
    authorization = models.CharField(max_length=10, null=True, blank=True)
    pquestion1 = models.CharField(max_length=200, null=True, blank=True)
    panswer1 = models.CharField(max_length=200, null=True, blank=True)
    pquestion2 = models.CharField(max_length=200, null=True, blank=True)
    panswer2 = models.CharField(max_length=200, null=True, blank=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return (self.name)


class Message(models.Model):
    author = models.ForeignKey('User', related_name='Message_Author', on_delete=models.CASCADE)
    receiver = models.ForeignKey('User', related_name='Message_Receiver', on_delete=models.CASCADE)
    content = models.CharField(max_length=500, null=True, blank=True)
    time = models.DateTimeField(default=timezone.now)
    remarks = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return ('from %s to %s at %s:%s %s/%s/%s'
                % (self.author, self.receiver, self.time.hour, self.time.minute, self.time.day, self.time.month,
                   self.time.year))


class Topic(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.CharField(max_length=500, null=True, blank=True)
    time = models.DateTimeField(default=timezone.now)
    # author = models.ForeignKey('User', related_name='Topic_Author', on_delete=models.CASCADE)
    remarks = models.IntegerField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.content


    def recent_topic(self):
        return self.time >= timezone.now()-timedelta(minutes=3)

class Topiccomment(models.Model):
    topic = models.ForeignKey('Topic',  on_delete=models.CASCADE, null=True,
                              blank=True)
    # comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True,
    #                             blank=True)
    content = models.CharField(max_length=500, null=True, blank=True)
    time = models.DateTimeField(default=timezone.now)
    # author = models.ForeignKey('User', related_name='TopicComment_Author', on_delete=models.CASCADE)
    # remarks = models.CharField(max_length=500, null=True, blank=True)


class News(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.CharField(max_length=500, null=True, blank=True)
    time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('User', related_name='News_Author', on_delete=models.CASCADE)
    remarks = models.CharField(max_length=500, null=True, blank=True)


class NewsComment(models.Model):
    topic = models.ForeignKey('News', related_name='NewsComment_Topic', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey('self', related_name='NewsComment_Comment', on_delete=models.CASCADE, null=True,
                                blank=True)
    content = models.CharField(max_length=500, null=True, blank=True)
    time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('User', related_name='NewsComment_Author', on_delete=models.CASCADE)
    remarks = models.CharField(max_length=500, null=True, blank=True)


class Photo(models.Model):
    author = models.ForeignKey('User', related_name='Photo_Author', on_delete=models.CASCADE)
    photo_path = models.FilePathField(null=True, blank=True)
    thumbs_up_number = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=20, null=True, blank=True)
    time = models.DateTimeField(default=timezone.now)
    remarks = models.CharField(max_length=500, null=True, blank=True)


class PhotoComment(models.Model):
    author = models.ForeignKey('User', related_name='PhotoComment_Author', on_delete=models.CASCADE)
    photo = models.ForeignKey('Photo', related_name='PhotoComment_Photo', on_delete=models.CASCADE, null=True,
                              blank=True)
    comment = models.ForeignKey('self', related_name='PhotoComment_Comment', on_delete=models.CASCADE, null=True,
                                blank=True)
    thumbs_up_number = models.IntegerField(null=True, blank=True)
    thumbs_down_number = models.IntegerField(null=True, blank=True)
    time = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=500, null=True, blank=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)
