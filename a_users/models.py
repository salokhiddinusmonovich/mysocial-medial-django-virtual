from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    realname = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    location = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('images/avatar_default.png')
        return avatar

    @property
    def name(self):
        if self.realname:
            name = self.realname
        else:
            name = self.user.username
        return name


class SupportMe(models.Model):
    author = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='support_me')
    message = models.CharField(max_length=150)
