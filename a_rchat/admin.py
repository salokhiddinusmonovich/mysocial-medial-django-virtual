from django.contrib import admin
from .models import GroupMessage, ChatGroup

admin.site.register(ChatGroup)
admin.site.register(GroupMessage)

