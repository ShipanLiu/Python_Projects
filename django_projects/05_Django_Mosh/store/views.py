# 为了节省时间， 我们使用 django.shortcuts 里面的函数
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view  # decorators
from rest_framework.response import Response # this is response from rest framework, not from "django"
from rest_framework import status # status.HTTP_404_NOT_FOUND 等价于 404,  return Response(status=status.HTTP_404_NOT_FOUND)
# 当前文件下的 ,models.py import a class
from .models import Product
from .serializers import ProductSerializer


# Create your views here.

def say_hallo(request):
    return HttpResponse("hallo")

@api_view() # so "request" as a parameter will no longer belong to “django” but to "django_restframework"
def product_list(request):
    queryset = Product.objects.all();
    # serializer 可以接受单个Product，也可以接受
    return Response("ok")


@api_view()
def product_detail(request, id):
    # get the targeted product
    product = get_object_or_404(Product, pk=id)
    # create a serilizer and pass the "product" into it
    slizer = ProductSerializer(product)
    # now get the created "dictionary" from slizer
    dict = slizer.data
    # the djangorestfamework will create automatically convert the "dict" into JSON format and this is under the hood
    return Response(dict)