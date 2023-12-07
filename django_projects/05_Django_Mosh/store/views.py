# 为了节省时间， 我们使用 django.shortcuts 里面的函数
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view  # decorators
from rest_framework.response import Response # this is response from rest framework, not from "django", 比 django的更加强大。
from rest_framework import status  # status.HTTP_404_NOT_FOUND 等价于 404,  return Response(status=status.HTTP_404_NOT_FOUND)
# 当前文件下的 models.py import a class
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer, ProductModelSerializer, CollectionModelSerializer


# Create your views here.
def say_hallo(request):
    return HttpResponse("hallo")

@api_view(["GET", "POST"]) # so "request" as a parameter will no longer belong to “django” but to "django_restframework"
def product_list(request):
    if request.method == "GET":
        # because in the API we also need to involve the "collection" with "products",
        # so we load the "collection" and "products" together
        # this is like a join operation, Product + left outer join + Collection, This is a method used to optimize database queries
        queryset = Product.objects.select_related("collection").all()
        # serializer 可以接受单个Product，也可以接受 一个 queryset
        # slizer = ProductSerializer(queryset, many=True, context={"request": request}) # 把 drf 的 request 传入 serializer
        slizer = ProductModelSerializer(queryset, many=True, context={"request": request})
        dict = slizer.data
        return Response(dict)
    elif request.method == "POST":
        # ProductModelSerializer will deserialize the data(the data here is from Frontend)
        dSlizer = ProductModelSerializer(data=request.data)
        # if dSlizer.is_valid():
        #     dSlizer.validated_data
        #     return Response("ok")
        # else:
        #     return Response(dSlizer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 更加简介的写法：if it is not valid, then give exception
        dSlizer.is_valid(raise_exception=True) # check the validate rules defined in ProductModelSerializer
        # you have to use ".is_valid" before using "validated_data"
        print(dSlizer.validated_data)
        # 自动存到数据库
        dSlizer.save()
        return Response("ok")


@api_view(["GET", "PUT", "PATCH"]) # PATCH, sometimes, one can only update a subset of data, so Patch is mostly used.
def product_detail(request, id):
    # get the targeted product，get_object_or_404() is same as "try()... catch()..."
    product = get_object_or_404(Product, pk=id)
    if request.method == "GET":
        # create a serilizer and pass the "product" into it
        slizer = ProductSerializer(product, many=False, context={"request": request})
        # now get the created "dictionary" from slizer
        dict = slizer.data
        # the drf will create automatically convert the "dict" into JSON format
        # happen under the hood the django will create a JSONRenderer Obj  ----> convert "dict" into "obj"
        return Response(dict)
    elif request.method == "PUT":
        # deserilize the data
        # validate the data
        # save to the database
        pass



@api_view()
def collection_detail(request, pk):
    target_collection = get_object_or_404(Collection, pk=pk)
    # slizer = CollectionSerializer(target_collection, many=False)
    slizer = CollectionModelSerializer(target_collection, many=False)
    return Response(slizer.data)
