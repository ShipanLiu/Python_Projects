from django.urls import path
from . import views

urlpatterns = [
    path("posts", views.post_list_handle, name="posts"),
    path("create_post", views.create_post_handle, name="create_post"),
    path("create_comment/<int:post_id>", views.create_comment_handle, name="create_comment"),
    #demo/blog/create_reply/9/1
    path("create_reply/<int:post_id>/<int:comment_id>", views.create_comment_reply_handle, name="create_reply"),
]
