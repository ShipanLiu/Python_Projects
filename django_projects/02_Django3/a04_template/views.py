from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from a04_template.models import *

# Create your views here.

def t01_template_engine_handle1(request, pk):
    target_person = get_object_or_404(Person, pk=pk)
    all_person = Person.objects.all()
    dict = {
        "bj": "北京",
        "sh": "上海"
    }
    list = [
        {
            "bj": "北京",
            "sh": "上海"
        },
        {
            "tj": "天津",
            "cq": "重庆"
        }
    ]
    return render(request, "a04_template/01_template.html", locals())
