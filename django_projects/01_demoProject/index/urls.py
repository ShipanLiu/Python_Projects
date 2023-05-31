from django.urls import path
from . import views


urlpatterns = [
    #http://127.0.0.1:8000/index
    path("", views.handle_index)

]
