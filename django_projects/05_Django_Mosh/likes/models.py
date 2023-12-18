from django.db import models
from django.contrib.auth.models import User
# from core.models import MyUser # 不要这样引用， 否则 “likes” 这个app 就会不独立
from django.conf import settings # use "settings.AUTH_USER_MODEL"
# we use the modified user model
# from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class LikedItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
