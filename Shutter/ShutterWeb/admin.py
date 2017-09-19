from django.contrib import admin
from .models import User
from .models import Message

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User

admin.site.register(User, UserAdmin)

class MessageAdmin(admin.ModelAdmin):
    class Meta:
        model = Message

admin.site.register(Message, MessageAdmin)