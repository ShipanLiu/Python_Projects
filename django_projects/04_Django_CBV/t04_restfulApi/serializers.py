from decimal import Decimal
from t03_store.models import Product, Collection
#serializers 是 把model 变成 dict 的
from rest_framework import serializers

#number -> decimal
from decimal import Decimal

''' 第一代写法  '''

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    collection_name = serializers.CharField(max_length=255, source='title')

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    # 告诉django ‘product_name’ 对应的就是 models.py 里的  ‘title’
    product_name = serializers.CharField(max_length=255,source='title')
    #告诉django ‘product_price’ 对应的就是 models.py 里的  ‘unit_price’
    product_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    # 这个字段 是 model.py 里面的 Product 表 里面没有的， 属于 APIModel 自己加的
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_pricewithtax') # we define a method, which returns value for thsis field

    #种类1: 返回id  开始学习 foreign key 查询了。
    collection_id = serializers.PrimaryKeyRelatedField(
         queryset=Collection.objects.all()
    )

    #种类2: 返回name  这是利用了 Collection 里面的 def __str__(self) 方法
    collection_name = serializers.StringRelatedField(source='collection')

    #种类3: 返回 以子自己定义的 serializer(相当于 dict)     或者自己定义一个 CollectionSerializer， 显示一个 dict 回去
    collection_dict = CollectionSerializer(source='collection')

    # 自己定义的 类颞部的函数 ==》 服务于 class
    def calculate_pricewithtax(self, product: Product):
        return product.unit_price * Decimal(1.1)
                                                                        #     "id": 2,
                                                                        #     "product_name": "Iphone15",
                                                                        #     "product_price": 1000.0,
                                                                        #     "price_with_tax": 1100.0,
                                                                        #     "collection_id": 1,
                                                                        #     "collection_name": "handy",
                                                                        #     "collection_dict": {
                                                                        #         "id": 1,
                                                                        #         "collection_name": "handy"
                                                                        #     }
                                                                        # },















'''
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
'''
