# convert a float to decimal
from decimal import Decimal

from rest_framework import serializers
from .models import (Product, Collection,
                     Review, Cart, CartItem,
                     Order, OrderItem,
                     Customer)
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<use ModelSerilizer<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<



# 这比 上面的 ProductSerializer 更高级， 使用 Model Serilizer, 会使更改 “validate rules 更加容易”，
# 原理 就是直接使用 Model 的Field，不用再定义新的 fields, in this case, if you want to change the "validation rules"
# then you only need to change one place.
class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # "unit_price" 被 “price” 取代, because you have defined the "price" field
        fields = ["id", "title", "slug", "description", "unit_price", "inventory", "collection", "price_with_tax"]
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_price_wit_tax", read_only=True)


    # serialized_product is the product(model) that is serialized
    def calculate_price_wit_tax(self, serialized_product: Product):
        # attention: "Decimal,小数" can NOT multiply "float number，浮点数"
        result = serialized_product.unit_price * Decimal(1.1)
        # result是 Decimal格式，rounded to 2 decimal places
        return round(result, 2)


class CollectionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ["id", "title", "featured_product", "products_count"]
    products_count = serializers.IntegerField(read_only=True)



# >>>>here is serializer class for review>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class ReviewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "name", "description", "create_date", "update_date"]
    def create(self, validated_data):
        # create a new instance
        product_id = self.context.get("product_id")
        # 写法2
        new_review = Review.objects.create(product_id=product_id, **validated_data)
        # return instance
        return new_review



class SimpleProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]


# >>>>> CartItemModelSerializer
# 可以应对 get, put/patch, delete
class CartItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model =  CartItem
        fields = ["id", "product", "quantity", "cart_item_total_price"]

    # we want to get the ProductObj(简化版)
    product = SimpleProductModelSerializer(read_only=True)
    cart_item_total_price = serializers.SerializerMethodField(read_only=True)

    def get_cart_item_total_price(self, single_cart_item:CartItem):
        return single_cart_item.product.unit_price * single_cart_item.quantity

    # for GET, PUT, PATCH, DELETE, you don;t need to do anything additional


# 之所以单独创建这个Serilizer 是因为要应对 create 要在post body 里面写  product_id,  而不是写product object
class CreateCartItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        # fields = ["id", "product", "quantity"]
        fields = ["id", "product_id", "quantity"] #假如你非要写成product_id 的话，then you need to redefine it.
    product_id = serializers.IntegerField()

    # create a CartItem in "http://127.0.0.1:8000/store/carts/d0c9caf5714e4c1ea3ee65363a160672/items/1/"  ==> you need use the "cart_id" in the context passed from views.py
    #def create(self, validated_data):
        # get cart_id
        # cart_id = self.context.get("cart_id")
        # create a new CartItem using CartItem.objects.create(), you can not create this way, 如果body里你给的 product id 不存在呢？
        # new_cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)

    # validate the product_id, 注意命名规则。
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"no product with id {value} exist ")
        return value


    #  the default create() and update() method form ModelSerializer will call save() at the end
    # so it's better to controll the save() method so that we won't rewrite 2 methods "create()" + "update()"
    # here we don't want the same item be saved twice
    def save(self, **kwargs):
        # get cart_id
        cart_id = self.context.get("cart_id")
        # get product_id
        product_id = self.validated_data.get("product_id")
        # get quantity
        quantity = self.validated_data.get("quantity")

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            # now update an existing item
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # now create an item
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance


# we only want to update the quantity using "PATCH"
class UpdateCartItemModelSerializer(serializers.ModelSerializer):
    # update is not like create, we don't need the "cart_id" or "product_id"
    class Meta:
        model = CartItem
        fields = ["quantity"]



# >>>>> CartModelSerializer
class CartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        # fields = ["id", "created_at"]
        fields = ["id", "items", "cart_total_price"]

    id = serializers.UUIDField(read_only=True)
    # list the CartItemObj
    items= CartItemModelSerializer(many=True, read_only=True)

    cart_total_price = serializers.SerializerMethodField()

    def get_cart_total_price(self, cart:Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])



# Customized SLizer for Customer
class CustomerModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        # fields = ["id", "user", "phone", "birth_date", "membership"]
        fields = ["id", "user_id", "username", "phone", "birth_date", "membership"]

    # if you want to use field "user_id", then you need really to create this filed on fly
    user_id = serializers.IntegerField()

    # show the username eachtime
    username = serializers.SerializerMethodField(read_only=True)

    def get_username(self, customer: Customer):
        return customer.user.username


class PutCustomerModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        # fields = ["id", "user", "phone", "birth_date", "membership"]
        fields = ["id", "user_id", "phone", "birth_date", "membership"]

    # if you want to use field "user_id", then you need really to create this filed on fly
    user_id = serializers.IntegerField(read_only=True)




# OrderItem Serializer
class OrderItemModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product_id", "product", "quantity", "order_item_total_price"]
        read_only_fields = ["order_item_total_price"]
    product_id = serializers.IntegerField()
    product = SimpleProductModelSerializer(read_only=True)



# Order Serializer
class OrderModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "customer_id", "customer_username", "placed_at", "payment_status", "orderitems"]


    customer_id = serializers.IntegerField()
    customer_username = serializers.SerializerMethodField(read_only=True)
    orderitems = OrderItemModalSerializer(many=True, read_only=True)

    def get_customer_username(self, order:Order):
        return order.customer.user.username

