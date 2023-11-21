from django.shortcuts import render

# Create your views here.

def handle_index(request):
    return render(request, "index/index.html")
    pass

