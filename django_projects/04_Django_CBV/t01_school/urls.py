from django.urls import path, include
import t01_classroom

app_name = "t01_school"

urlpatterns = [
    path('', include('t01_classroom.urls')),
]
