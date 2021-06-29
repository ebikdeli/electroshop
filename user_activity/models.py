from django.db import models
from profile.models import Profile
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# from tinymce.models import HTMLField
# from django_quill.fields import QuillField


class Comment(models.Model):
    profile = models.ForeignKey(Profile,
                                on_delete=models.SET_NULL,
                                related_name='profile_comments',
                                null=True)
    # comment = HTMLField()
    # comment = QuillField()
    comment = models.TextField(blank=True, max_length=1500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.profile.user.username}_comment_{self.id}'


class Like(models.Model):
    profile = models.ForeignKey(Profile,
                                on_delete=models.SET_NULL,
                                related_name='profile_likes',
                                null=True)
    like = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.profile.user.username}_like_{self.id}'
