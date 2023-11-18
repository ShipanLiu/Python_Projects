from django.shortcuts import render
# 从 generic 引入 ， 方便我们的生活,
from django.views.generic import TemplateView

# Create your views here.

class H01_HomeView(TemplateView):
    template_name = 't01_classroom/01_index.html'

class H02_ThankyouView(TemplateView):
    template_name = 't01_classroom/02_thankyou.html'


