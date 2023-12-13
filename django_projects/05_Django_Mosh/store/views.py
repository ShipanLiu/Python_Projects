# aggregate function: count
from django.db.models.aggregates import Count
# 为了节省时间， 我们使用 django.shortcuts 里面的函数
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view  # decorators
from rest_framework.response import Response # this is response from rest framework, not from "django", 比 django的更加强大。
from rest_framework import status  # status.HTTP_404_NOT_FOUND 等价于 404,  return Response(status=status.HTTP_404_NOT_FOUND)
# 当前文件下的 models.py import a class
from .models import Product, Collection, OrderItem, Review
from .serializers import ProductSerializer, CollectionSerializer, ProductModelSerializer, CollectionModelSerializer, ReviewModelSerializer

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


# >>>>>>>>>>>>>>>Class Based View>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# 这个更牛逼，combine "ProductList" and "ProductDetail", "GET", "POST", "PUT", "DELETE" 都结合在一起了。
# ModelViewSet contains all minxins and APIView
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ["collection_id"]
    filterset_class = ProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]
    # you can set the global pagination in settings.py
    pagination_class = DefaultPagination # you don't need to in  "settings.py" and set the PAGE_SIZE, because DefaultPagination has included the page_size


    # the filtering logic could be replaced by "DjangoFil"
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get("collection_id") # the get() method may give back a None
    #     if collection_id is not None:
    #         queryset = Product.objects.filter(collection_id=collection_id)
    #     return queryset

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




# class ProductList(ListCreateAPIView):
#     # a more easy way to replace the "get_queryset()" and "get_serializer_class()" method
#     queryset = Product.objects.all()
#     serializer_class = ProductModelSerializer
#
#     # if you use generics "ListCreateAPIView", the only thing you need to overwrite 2 methods and provide "queryset" and "serilizer"
#     # def get_queryset(self):
#     #     return Product.objects.select_related("collection").all() # return the target queryset
#     # def get_serializer_class(self):
#     #     return ProductModelSerializer # return the target serilizer
#     # the serilizer need context
#     def get_serializer_context(self):
#         return {"request": self.request}
#
#
#
#     # def get(self, request):
#     #     queryset = Product.objects.select_related("collection").all()
#     #     slizer = ProductModelSerializer(queryset, many=True, context={"request": request})
#     #     dict = slizer.data
#     #     return Response(dict)
#     #
#     # def post(self, request):
#     #     dSlizer = ProductModelSerializer(data=request.data, context={"request": request})
#     #     dSlizer.is_valid(raise_exception=True)
#     #     print(dSlizer.validated_data)
#     #     dSlizer.save()
#     #     return Response(dSlizer.data, status=status.HTTP_201_CREATED)
#
# # support GET, PUT, DELETE, ==> http://127.0.0.1:8000/store/products/2
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     # here you provide the base queryset(all products, but not filter)
#     queryset = Product.objects.all()
#     serializer_class = ProductModelSerializer
#
#     # GET 和 PUT are all exected automaticlly
#     # you need to overwrite the delete()" in "RetrieveUpdateDestroyAPIView" to realize customized logic
#
#
#
#     # def get(self, request, id):
#     #     target_product = get_object_or_404(Product, pk=id)
#     #     slizer = ProductModelSerializer(target_product, many=False, context={"request": request})
#     #     dict = slizer.data
#     #     return Response(dict)
#     #
#     # def put(self, request, id):
#     #     target_product = get_object_or_404(Product, pk=id)
#     #     slizer = ProductModelSerializer(target_product, data=request.data, context={"request": request})
#     #     slizer.is_valid(raise_exception=True)
#     #     slizer.save()
#     #     return Response(slizer.data)
#
#     def delete(self, request, pk):
#         target_product = get_object_or_404(Product, pk=pk)
#         if target_product.orderitems.count() > 0:
#             return Response({"error": "this product exist in an order, can not be deleted"},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         target_product.delete()
#         return Response({"message": f"delete product with id: {id} in success"}, status=status.HTTP_204_NO_CONTENT)




class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionModelSerializer

    # pass the "request" to the sLizer, because: when you need to access the request object inside your serializer for various purposes,
    # such as generating hyperlinks or accessing user information.
    # Regarding the request attribute, Django's class-based views are designed to handle web requests.

    # request 是哪里来的？ When a request comes in, Django creates an instance of the view class and sets various attributes on it,
    # including the request object. This request object contains all the information about the current HTTP request -
    # -such as GET and POST data, headers, the authenticated user (if any), and so on.
    def get_serializer_context(self):
        return {"request": self.request}


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionModelSerializer

    # overwrite the "delete()" method in "RetrieveUpdateDestroyAPIView"
    def delete(self, request, pk):
        target_collection = get_object_or_404(Collection, pk=pk)
        if target_collection.products.count() > 0:
            return Response({"error": "collection contains some products, can not be deleted"})
        target_collection.delete()
        return Response({"message": f"target collection with id:{pk} and title:{target_collection.title} is deleted"})





# >>>>>>>>>>>>>>>>>>>>>>>>>>function based view(we won;t use because too many if and else)>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>




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
        dSlizer = ProductModelSerializer(data=request.data, context={"request": request})
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
        # return the data, so that you can see.(you can also return somethingelse)
        return Response(dSlizer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])# PATCH, sometimes, one can only update a subset of data, so Patch is mostly used.
def product_detail(request, id):
    # get the targeted product，get_object_or_404() is same as "try()... catch()..."
    product = get_object_or_404(Product, pk=id)
    if request.method == "GET":
        # create a serilizer and pass the "product" into it
        slizer = ProductModelSerializer(product, many=False, context={"request": request})
        # now get the created "dictionary" from slizer
        dict = slizer.data
        # the drf will create automatically convert the "dict" into JSON format
        # happen under the hood the django will create a JSONRenderer Obj  ----> convert "dict" into "obj"
        return Response(dict)
    elif request.method == "PUT":
        # deserilize the data, this slizer will call the "update()" method in serialiers.py
        slizer = ProductModelSerializer(product, data=request.data, context={"request": request})
        # validate the data
        slizer.is_valid(raise_exception=True)
        # save to the database
        slizer.save()
        # return the data, so that you can see.(you can also return somethingelse)
        return Response(slizer.data)
    # http://127.0.0.1:8000/store/products/1004/  ==> I want to delete 1004, this "1004", you can write it into your body, or write in  the url
    elif request.method == "DELETE":
        # if the to be deleted products is also an orderitem
        # By default, the name of this reverse relation is the lowercase name of the related model followed by '_set'.
        # but here I have a DIY related_name : "orderitems" defined in OrderItem model
        if product.orderitems.count() > 0:
            return Response({"error": "this product exist in an order, can not be deleted"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        # this is the conventio of restful API, after deleting return a 204
        return Response({"message": f"delete product with id: {id} in success"}, status=status.HTTP_204_NO_CONTENT)


# >>>>>>>>>>>>>>Collection>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.



@api_view(["GET", "POST"])
def collection_list(request):
    if request.method == "GET":
        # get teh queryset from database
        # annotate(...): This method allows you to add extra fields to each model instance in the "QuerySet". These fields are not part of your model; instead, they are calculated on the fly.
        # Here, you are creating a new field products_count in the QuerySet. This field will contain the count of related Product instances for each Collection.
        # "products" should be the related name from the Collection model to the Product model.
        queryset = Collection.objects.annotate(products_count=Count("products")).all()
        # get slizer, of course you need to prepare a "products_count" field in your "CollectionModelSerializer"
        slizer = CollectionModelSerializer(queryset, many=True, context={'request': request})
        # don't need to validate the data, because this is GET
        # response
        return Response(slizer.data)
    elif request.method == "POST":
        # get data from request
        # get dSlizer
        dSlizer = CollectionModelSerializer(data=request.data, context={'request': request})
        # validate the data
        dSlizer.is_valid(raise_exception=True)
        # save to the database
        new_added_collection_item = dSlizer.save()
        #{'dSlizer.data': {'id': 23, 'title': 'iphone', 'featured_product': 40, 'featured_product_obj': OrderedDict([('id', 40), ('title', 'Bread - Hamburger Buns'), ('slug', '-'), ('description', 'vel nulla eget eros elementum pellentesque quisque porta volutpat erat quisque erat eros viverra eget congue eget'), ('unit_price', Decimal('51.39')), ('inventory', 8), ('collection', 5), ('price_with_tax', Decimal('56.53')), ('collection_obj', OrderedDict([('id', 5), ('title', 'Stationary')])), ('collection_link', 'http://127.0.0.1:8000/store/collections/5')])}}
        print({"dSlizer.data": dSlizer.data})
        # {'dSlizer.validated_data': OrderedDict([('title', 'iphone'), ('featured_product', <Product: Bread - Hamburger Buns>)])}
        print({"dSlizer.validated_data": dSlizer.validated_data})
        # {'new_added_collection_item': <Collection: iphone>}
        print({"new_added_collection_item": new_added_collection_item})
        # return response
        return Response({"message": "a new collection is created", "new_added_collection_item": dSlizer.data}, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def collection_detail(request, pk):
    # bacause in the "CollectionModelSerializer", there exist a field "products_count", so your target_collection has to contain a "products_count", you can only use annotate(add on fly)
    target_collection = get_object_or_404(Collection.objects.annotate(products_count=Count("products")), pk=pk)
    if request.method == "GET":
        # generate the sLizer, put the source into it.
        slizer = CollectionModelSerializer(target_collection, many=False)
        # you don't have to validate because this is get.
        return Response(slizer.data)
    elif request.method == "PUT":
        # get dSlizer
        dSlizer = CollectionModelSerializer(target_collection, data=request.data, context={'request': request})
        # validate data
        dSlizer.is_valid(raise_exception=True)
        # save to database
        dSlizer.save() # the save() method will call the update() method inside of "CollectionModelSerializer"
        return Response({"updated_collection": dSlizer.data})

    elif request.method == "DELETE":
        # if this collection has belonged products, then you can't delete
        # "products" is the related_name in model "Products"
        if target_collection.products.count() > 0:
            return Response({"error": "collection contains some products, can not be deleted"})
        target_collection.delete()
        return Response({"message": f"target collection with id:{pk} and title:{target_collection.title} is deleted"})

