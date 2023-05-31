from django.urls import path
from . import views

urlpatterns = [

    path("posts", views.post_list_handle, name="posts"),
    path("create_post", views.create_post_handle, name="create_post"),

]
