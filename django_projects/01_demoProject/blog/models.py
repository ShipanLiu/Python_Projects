from django.db import models
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the sys.path
sys.path.insert(0, parent_dir)
from user.models import User

class Post(models.Model):
    title = models.CharField(verbose_name="post title", max_length=255)
    content = models.TextField("post content")
    created_time = models.DateTimeField("create time", auto_now_add=True)
    updated_time = models.DateTimeField("update time", auto_now=True)
    user = models.CharField("related uid", max_length=10)
    class Meta:
        db_table = 'demo_post'

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField("comment content")
    created_time = models.DateTimeField("create time", auto_now_add=True)
    updated_time = models.DateTimeField("update time", auto_now=True)
    user = models.CharField("related uid", max_length=10)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        db_table = 'demo_comment'

    def __str__(self):
        return self.content
