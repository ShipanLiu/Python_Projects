from django.urls import path
from .views import H01_HomeView, H02_ThankyouView

app_name="t01_classroom"

urlpatterns = [
    path('', H01_HomeView.as_view(), name='index'),
    path('thank_you/', H02_ThankyouView.as_view(), name='thank_you')
]
