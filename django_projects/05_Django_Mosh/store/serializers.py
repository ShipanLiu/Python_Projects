# convert a float to decimal
from decimal import Decimal

from rest_framework import serializers
from .models import Product, Collection, Review


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
    collection_name = serializers.StringRelatedField(source="collection", read_only=True)

    # here the collection_obj will be an Obj {}
    collection_obj = CollectionSerializer(source="collection", read_only=True)

    # we create a hyperlink for the collection
    # view_name="collection-detail" is the url name in urls.py ==>  path("collections/<int:id>", views.collection_detail, name="collection-detail")
    # in view you need to add: context={"request": request} to the serilizer
    collection_link = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name="collection-detail",
        source="collection",
    )


    # serialized_product is the product(model) that is serialized
    def calculate_price_wit_tax(self, serialized_product: Product):
        # attention: "Decimal" can NOT multiply "float number"
        return serialized_product.unit_price * Decimal(1.1)






#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<use ModelSerilizer<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<







# 这比 上面的 ProductSerializer 更高级， 使用 Model Serilizer, 会使更改 “validate rules 更加容易”，
# 原理 就是直接使用 Model 的Field，不用再定义新的 fields, in this case, if you want to change the "validation rules"
# then you only need to change one place.
class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # "unit_price" 被 “price” 取代, because you have defined the "price" field
        fields = ["id", "title", "slug", "description", "unit_price", "inventory", "collection", "price_with_tax"]
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source="unit_price") # 1234.56
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_price_wit_tax", read_only=True)
    # collection_obj = CollectionSerializer(required=False, source="collection", read_only=True)
    # collection_link = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name = "collection-detail",
    #     required=False,
    #     source = "collection",
    # )


    # serialized_product is the product(model) that is serialized
    def calculate_price_wit_tax(self, serialized_product: Product):
        # attention: "Decimal,小数" can NOT multiply "float number，浮点数"
        result = serialized_product.unit_price * Decimal(1.1)
        # result是 Decimal格式，rounded to 2 decimal places
        return round(result, 2)

    # here override the create method, for creating a new tuple in th edatabase, it is responsible for creating new instances of a model based on the validated data
    # create() is called after calling save() in the views.py
    # def create(self, validated_data):
    #     #create a new Object, take the validated_data dictionairy, the **validated_data syntax unpacks the dictionary, passing the key-value pairs as arguments to the Product model constructor
    #     newProduct = Product(**validated_data)
    #     # set a special field, useful for setting default values or adding data that is not provided by the API user but is required by the application's logic.
    #     newProduct.other = 1
    #     newProduct.save()
    #     return newProduct


    # updaing a product, override the basic method in serilizer:
    # def update(self, instance, validated_data):
    #     # for example if you want to update "unit_price"
    #     instance.unit_price = validated_data.get("unit_price")
    #     instance.save()
    #     return instance




    # define data validate rules(here override the validate method from serializers)
    # def validate(self, data):
    #     # pwd consistency
    #     if data["password"] != data["confirm_password"]:
    #         return serializers.ValidationError("password and confirm_password do not match")
    #     # if all right, then return the data
    #     return data


# 这样 POST request 可以为：-> http://127.0.0.1:8000/store/collections/
# {
#     "title": "test collection",
#     "featured_product": 200
# }
# 注意： featured_product 只用给 integer（primary key）就行了，这是默认的.

class CollectionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        # in model "Collection", the field "featured_product" is a FK and can be NULL, so when doing a post request, it is not required.
        fields = ["id", "title", "featured_product", "products_count"]

    # use ProductModelSerializer, show Product Object only when “GET” method
    # source="featured_product"，以featured_product 为 source， 来生成featured_product_obj。
    # featured_product_obj = ProductModelSerializer(read_only=True, source="featured_product") # we only need the collection id

    # the Collection model does not have "products_count", so I need to define here.
    # read_only  ==>  只用于从 database 里 rausholen, so you don't need to set "required=False"
    products_count = serializers.IntegerField(read_only=True)



# >>>>here is serializer class for review>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class ReviewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "name", "description", "create_date", "update_date"]

    # 一般POST 请求 create 一个 Review 的时候， the body will be like:
    #     {"name": "customer 1",
    #     "description": "this is a test review"
    #     "product":1 }
    # the post url will be http://127.0.0.1:8000/store/products/1/reviews/
    # the post url will be store/products/<int:product_pk>/reviews/<int:pk>/
    # but in the url, the product id is already included, so the new request body could be(without product):
    #     {
    #     "name": "customer 1",
    #     "description": "this is a test review"
    #     }
    # and we can get the product_pk from the url
    # now overwrite the create() method, the create method is for DIY logic before saving to database
    def create(self, validated_data):
        # create a new instance
        product_id = self.context.get("product_id")

        # 写法1
        # new_review = Review(product_id=product_id, **validated_data)
        # new_review.save()

        # 写法2
        new_review = Review.objects.create(product_id=product_id, **validated_data)

        # return instance
        return new_review



