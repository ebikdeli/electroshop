from django.db import models
from profile.models import Profile
from tinymce.models import HTMLField


class Comment(models.Model):
    profile = models.OneToOneField(Profile,
                                   on_delete=models.SET_NULL,
                                   related_name='profile_comments',
                                   null=True)
    comment = HTMLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
