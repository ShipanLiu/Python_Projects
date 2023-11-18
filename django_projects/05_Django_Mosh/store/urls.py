from django.urls import path, include
from . import views

#URLConf
urlpatterns = [
    path("hello/", views.say_hallo),
    path("products/", views.product_list),
    path("products/<int:id>/", views.product_detail),
]