###################for DAY 3##########################
from django.shortcuts import render


def test_static(request):
    return render(request, "07_test_static.html")
