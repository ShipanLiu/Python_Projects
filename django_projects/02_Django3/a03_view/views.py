from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.views import View

# Create your views here.

class t01_CBV_class_base_views(View):
    def get(self, request):
        return HttpResponse("response to GET via CBV class")
    def post(self, request):
        return HttpResponse("response to POST via CBV class")

# 错误处理
def t02_handle(request, errorNr):
    if errorNr > 30:
        return HttpResponseNotFound(f"page not found errorNr: {errorNr}")
    # 浏览器 可以识别
    elif errorNr > 20:
        # return HttpResponse(f"page not found errorNr: {errorNr}", status=404)
        raise Http404(f"page not found errorNr: {errorNr}")
