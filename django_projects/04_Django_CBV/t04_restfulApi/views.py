from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status # 比如404

from t03_store.models import Product
from .serializers import ProductSerializer

'''
理论上是 应该 使用 class based view 的， to keey the code DRY
但是 【code with mosh】 的教程是 functiona view， 所以暂且是用 functional view 来吧
'''



@api_view()
def product_list_view(request):
    #先把collection 查出来， 然后和 products join， 假如不这样的话，就会 每一个product 都会查一遍collection
    products_query_set = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(products_query_set, many=True) # tell ProductSerializer that there are more than 1 items
    return Response(serializer.data)

'''
访问： http://127.0.0.1:8000/t03/products/  得到的结果：

GET /t03/products/
HTTP 200 OK
Allow: GET, OPTIONS
Content-Type: application/json
Vary: Accept

"ok"

'''

@api_view(['GET'])
def product_detail_view(request, id):
    # try:
    #     product = Product.objects.get(pk=id)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)


    #上面的try except 可以用 “from django.shortcuts import get_object_or_404” 来代替
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)



