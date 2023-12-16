# aggregate function: count
from django.db.models.aggregates import Count
# 为了节省时间， 我们使用 django.shortcuts 里面的函数
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view  # decorators
from rest_framework.response import Response # this is response from rest framework, not from "django", 比 django的更加强大。
from rest_framework import status  # status.HTTP_404_NOT_FOUND 等价于 404,  return Response(status=status.HTTP_404_NOT_FOUND)
# 当前文件下的 models.py import a class
from .models import Product, Collection, OrderItem, Review, Cart, CartItem, Order, OrderItem
from .serializers import (ProductModelSerializer, CollectionModelSerializer,
                          ReviewModelSerializer, CartModelSerializer,
                          CartItemModelSerializer, CreateCartItemModelSerializer,
                          UpdateCartItemModelSerializer)

# for class based view, APIView is the base class for all CBVs(class based views)
from rest_framework.views import APIView
# for example in "GET" method, we always write the same code so here mixin comes
from rest_framework.mixins import ListModelMixin, CreateModelMixin
# we won't use mixins directly but we use generics:
# ListCreateAPIView has get() for listing  and post() for creating
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# for "ProductList" and "ProductDetail" we have the same "queryset" and "serializer_class", so here we need to apply Viewset
from rest_framework.viewsets import ModelViewSet # ModelViewSet combines listview(GET + POST) and detailview(GET+POST+DELETE)

# if you want to flter the products with any parameters, then you need a generic filter,and here you need "django-filter"
# DjangoFilterBackend gives us generic filtering
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
# now it is about searching ==> searching by some fields
from rest_framework.filters import SearchFilter, OrderingFilter # 'SearchFilter' is for filtering,  'OrderingFilter' is for ordering
# now about pagination
from rest_framework.pagination import PageNumberPagination

# DIY paginationclass
from .pagination import DefaultPagination

# if you don't want to use "ModelViewSet", you can create your own "MyViewSet"
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet



# >>>>>>>>>>>>>>>Class Based View>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# 这个更牛逼，combine "ProductList" and "ProductDetail", "GET", "POST", "PUT", "DELETE" 都结合在一起了。
# ModelViewSet contains all minxins and APIView
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # 这里的filter的意思是，根据filter， 列出list
    # filterset_fields = ["collection_id"]
    filterset_class = ProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]
    # you can set the global pagination in settings.py
    pagination_class = DefaultPagination # you don't need to in  "settings.py" and set the PAGE_SIZE, because DefaultPagination has included the page_size

    serializer_class = ProductModelSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    # overwrite the "destroy" method in "ModelViewSet.DestroyModelMixin"
    # because in original "destroy()" the target_object(here target product) is collected
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs.get("pk")).count() > 0:
            return Response({"error": "this product exist in an order, can not be deleted"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionModelSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        # I want del a collection, if the collection contains any products, then can not
        if Product.objects.filter(collection=kwargs.get("pk")).count() > 0:
            return Response({"error": "collection contains some products, can not be deleted"})
        return super().destroy(request, *args, **kwargs)


# ViewSet for Review=> this support GET, POST, PUT and DELETE
class ReviewViewSet(ModelViewSet):
    # get queryset(show all the reviews belongs to this product, here we need to have access to "self", so we overwrite the get_queryset method)
    # queryset = Review.objects.all()
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get("product_pk"))
    # sLizer class
    serializer_class = ReviewModelSerializer
    # context parameter,给 ReviewModelSerializer 传点东西。
    def get_serializer_context(self):
        return {
            "request": self.request,
            # http://127.0.0.1:8000/store/products/1/reviews/1/,  "product_pk" is the first '1', the pk is the second '1'
            # product_pk 对应 urls.py 里的 lookup="product", 会自动给你加上 '_pk'
            # store/products/<int:product_pk>/reviews/<int:pk>/
            # kwargs will be like: {
            #     'product_pk': 1,
            #     'pk': 1
            # }
            "product_id": self.kwargs.get("product_pk")
        }
    # overwrite method for customed methods


# >>> I don't want to use "ModelViewSet", "ModelViewSet" 有太多功能(我不想用"UpdateModelMixin" 和 “ListModelMixin”)
class MyBaseCartModelSet(RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    pass


# >>> CartViewSet -> handle "GET", "POST", "PUT", "PATCH", "DELETE"
# here be attention, we don't want to support "list all carts", and there is no "update a cart operation"
# GET : http://127.0.0.1:8000/store/carts/d0c9caf5714e4c1ea3ee65363a160672/  支持
# GET : http://127.0.0.1:8000/store/carts/  不应该支持
class CartViewSet(MyBaseCartModelSet):
    # queryset
    def get_queryset(self):
        # prefetch_related: use it when a cart man have multiple items, use "prefetch_related"
        # select_related: for foreignkeys where we have a single related object, use "select_related"
        # the "items" is related_name
        return Cart.objects.prefetch_related("items__product").all()  # '__product' means we also wat to preload the "product" in "items"
    # serilizer class
    serializer_class = CartModelSerializer
    # pass context
    def get_serializer_context(self):
        return {
            "request": self.request
        }


    # diy logic



# >>> CartItemViewSet
class CartItemViewSet(ModelViewSet):
    # how can you prevent the "PUT" mmethod?
    # if you use "PUT" method, then u need to update the whole Project.
    # the http-method here should be lower-case
    http_method_names = ["get", "post", "patch", "delete"]


    # queryset
    def get_queryset(self):
        # Foreignkey 的时候，就用 select_related
        return (CartItem.objects
                .filter(cart_id=self.kwargs.get("cart_pk"))
                .select_related("product"))
    # sLizer class
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateCartItemModelSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemModelSerializer
        return CartItemModelSerializer
    # pass context
    def get_serializer_context(self):
        return {
            "request": self.request,
            "cart_id": self.kwargs.get("cart_pk")
        }
