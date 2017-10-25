from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
import os


# Create your models here.

class UserProfile(AbstractUser):
    gender = models.CharField(max_length=1, null=True, default='U',blank=True)
    email = models.EmailField(null=True, blank=True)
    authorization = models.CharField(max_length=10, null=True, blank=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return (self.name)


class Message(models.Model):
    author = models.ForeignKey('UserProfile', related_name='Message_Author', on_delete=models.CASCADE)
    receiver = models.ForeignKey('UserProfile', related_name='Message_Receiver', on_delete=models.CASCADE)
    content = models.CharField(max_length=500, null=True, blank=True)
    time = models.DateTimeField(default=timezone.now)
    readflag = models.CharField(max_length=6, default='UNREAD')
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
    remarks = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.content

    def increase_remarks(self):
        self.remarks += 1
        self.save(update_fields=['remarks'])


    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

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

    def __str__(self):
        return self.content

class News(models.Model):
        title = models.CharField(max_length=100, null=True, blank=True)
        content = models.CharField(max_length=10000, null=True, blank=True)
        time = models.DateTimeField(default=timezone.now)
        author = models.CharField(max_length=100, null=True, blank=True)
        description = models.CharField(max_length=100, null=True, blank=True)
        remarks = models.CharField(max_length=500, null=True, blank=True)

class NewsComment(models.Model):
        topic = models.ForeignKey('News', related_name='NewsComment_Topic', on_delete=models.CASCADE, null=True,
                                  blank=True)
        comment = models.ForeignKey('self', related_name='NewsComment_Comment', on_delete=models.CASCADE, null=True,
                                    blank=True)
        content = models.CharField(max_length=500, null=True, blank=True)
        time = models.DateTimeField(default=timezone.now)
        author = models.ForeignKey('UserProfile', related_name='NewsComment_Author', on_delete=models.CASCADE)
        remarks = models.CharField(max_length=500, null=True, blank=True)



class Photo(models.Model):
    photographer = models.ForeignKey('UserProfile', related_name='Photo_Author',on_delete=models.CASCADE,null=True,
                              blank=True)
    image_path = models.ImageField(upload_to='static/images/album/%m-%Y/',blank=True,null=True)
    thumbs_up_number = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=20, null=True, blank=True)
    time = models.DateTimeField(default=timezone.now)
    photo_name = models.CharField(max_length=500, null=True, blank=True)
    photographer_name = models.CharField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return'%s %s'%(self.owner,self.image)  


class PhotoComment(models.Model):
    author = models.ForeignKey('UserProfile', related_name='PhotoComment_Author', on_delete=models.CASCADE)
    photo = models.ForeignKey('Photo', related_name='PhotoComment_Photo', on_delete=models.CASCADE, null=True,
                              blank=True)
    comment = models.ForeignKey('self', related_name='PhotoComment_Comment', on_delete=models.CASCADE, null=True,
                                blank=True)
    thumbs_up_number = models.IntegerField(null=True, blank=True)
    thumbs_down_number = models.IntegerField(null=True, blank=True)
    time = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=500, null=True, blank=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)
