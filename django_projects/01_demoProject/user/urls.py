from django.urls import path
from . import views


urlpatterns = [
    path("reg", views.handle_reg, name="reg"),
    path("login", views.handle_login, name="login"),
    path("logout", views.handle_logout, name="logout")
]
