from django.contrib import admin
from .models import User
from .models import Message
from .models import Topic
from .models import TopicComment
from .models import News
from .models import NewsComment
from .models import Photo
from .models import PhotoComment


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User


admin.site.register(User, UserAdmin)


class MessageAdmin(admin.ModelAdmin):
    class Meta:
        model = Message


admin.site.register(Message, MessageAdmin)

admin.site.register(Topic)

admin.site.register(TopicComment)

admin.site.register(News)

admin.site.register(NewsComment)

admin.site.register(Photo)

admin.site.register(PhotoComment)
