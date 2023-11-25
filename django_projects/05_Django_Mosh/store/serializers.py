# convert a float to decimal
from decimal import Decimal

from rest_framework import serializers
from .models import Product, Collection


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)




# serializer: convert "model instance" into "dictionary"
class ProductSerializer(serializers.Serializer):
    # you have to define, which attributes from tuple you want to serialize, 这样做的原因是
    # 不会 expose your sensitive data to the outside world
    # so here you have to define exactly like defining n model
    # 因为之后， serializer 还要接受 frontend 传来的products，这里定义max_length=255 也为了得到valid Serializer
    # the name of the attrivbutes here d't have to be the same as defined in Models
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    # here you don't have to use "unit_price" but you can just use "price",
    # but using the same name as in models is good.
    # if you use "price", you need to tell django which field in model to match
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source="unit_price") # 1234.56
    # 这是自定一个的一个 key，
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_price_wit_tax")
    # return the collection number: (这里的 collection field 是一个 foreign key)
    # using the "PrimaryKeyRelatedField", the result will be a PK, a number
    collection_nr = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all(),
        source="collection"
    )
    # this will use the " def __str__(self) -> str: return self.title" in Collection Model class
    collection_name = serializers.StringRelatedField(source="collection")

    # here the collection_obj will be an Obj {}
    collection_obj = CollectionSerializer(source="collection")

    # we create a hyperlink for the collection
    # view_name="collection-detail" is the url name in urls.py ==>  path("collections/<int:id>", views.collection_detail, name="collection-detail")
    # in view you need to add: context={"request": request} to the serilizer
    collection_link = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name="collection-detail",
        source="collection"
    )


    # serialized_product is the product(model) that is serialized
    def calculate_price_wit_tax(self, serialized_product: Product):
        # attention: "Decimal" can NOT multiply "float number"
        return serialized_product.unit_price * Decimal(1.1)






#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<use ModelSerilizer<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<







# 这比 上面的 ProductSerializer 更高级， 使用 Model Serilizer, 会使更改 “validate rules 更加容易”，
# 原理 就是直接使用 Model 的Field，不用再定义新的 fields
class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # "unit_price" 被 “price” 取代, because you have defined the "price" field
        fields = ["id", "title", "price", "price_with_tax", "collection_id", "collection_obj", "collection_link"]
        extra_kwargs = {
            "price_with_tax": {"required": False},
            "collection_obj": {"required": False},
            "collection_link": {"required": False},
        }
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source="unit_price") # 1234.56
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_price_wit_tax")
    collection_id = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all(),
        source="collection"
    )
    collection_obj = CollectionSerializer(source="collection")
    collection_link = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name = "collection-detail",
        source = "collection"
    )


    # serialized_product is the product(model) that is serialized
    def calculate_price_wit_tax(self, serialized_product: Product):
        # attention: "Decimal" can NOT multiply "float number"
        result = serialized_product.unit_price * Decimal(1.1)
        # result是 Decimal格式，rounded to 2 decimal places
        return round(result, 2)


class CollectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]
