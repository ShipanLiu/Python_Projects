from django.shortcuts import render
from django.http import  HttpResponse, HttpResponseRedirect

# Create your views here.


# path("index", views.index_view)
def index_view(request):
    return render(request, "news/index.html")

