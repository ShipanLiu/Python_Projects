# convert a float to decimal
from decimal import Decimal
from django.db import transaction


from rest_framework import serializers
from .models import (Product, Collection,
                     Review, Cart, CartItem,
                     Order, OrderItem,
                     Customer, ProductImage)

# here we need to inport our signals:
from .signals import order_created_signal
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<use ModelSerilizer<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

class ProductImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        # the url: products/1(product_pk)/images/1(pk), here we use the product_id from the nedted router,
        # but still I will provide the product id here
        fields = ["id", "product_id", "image"]
    # this is read only, for uploading the images, we use the pro duct_id in the nested router
    product_id = serializers.IntegerField(read_only=True)

    # overwrite the "create()" method and get the product_id from the context:
    def create(self, validated_data):
        # get product_id from context
        product_id = self.context.get("product_id")
        # create image instance
        productImage = ProductImage.objects.create(product_id=product_id, **validated_data)
        # retuen
        return productImage



# 这比 上面的 ProductSerializer 更高级， 使用 Model Serilizer, 会使更改 “validate rules 更加容易”，
# 原理 就是直接使用 Model 的Field，不用再定义新的 fields, in this case, if you want to change the "validation rules"
# then you only need to change one place.
class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # "unit_price" 被 “price” 取代, because you have defined the "price" field
        fields = ["id", "title", "slug", "description", "unit_price", "inventory", "collection", "price_with_tax", "images"]
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_price_wit_tax", read_only=True)
    images = ProductImageModelSerializer(many=True, read_only=True)

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
        fields = ["id", "product_id", "product", "quantity", "cart_item_total_price"]

    # we want to get the ProductObj(简化版)
    product = SimpleProductModelSerializer(read_only=True)
    product_id = serializers.IntegerField()
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
    """
    validated_data:
    
    {
        "id": 1,
        "product_id": 20,
        "product": {
            "id": 20,
            "title": "Cheese - Parmesan Cubes",
            "unit_price": 32.94
        },
        "quantity": 6,
        "cart_item_total_price": 197.64
    }
    
    in Django REST Framework (DRF) bezieht sich validated_data auf die Daten,
     die bereits durch den Serializer validiert wurden und die in der Regel 
     aus dem Request-Body stammen.
    
    
    """
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
        fields = ["id", "items", "customer_id", "cart_total_price"]

    id = serializers.UUIDField(read_only=True)
    customer_id = serializers.IntegerField()
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
    order_item_total_price = serializers.SerializerMethodField(read_only=True)

    def get_order_item_total_price(self, orderitem: OrderItem):
        return orderitem.product.unit_price * orderitem.quantity



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


# if you create an Order, the only thing you need to do is to return an Cart, and
# here you don't need any fields from Order Table, but just you want a Cart id, so we don;t use ModelSerilizer, but normal Serilizer
"""
    {
        "id": 1,
        "product_id": 20,
        "product": {
            "id": 20,
            "title": "Cheese - Parmesan Cubes",
            "unit_price": 32.94
        },
        "quantity": 6,
        "cart_item_total_price": 197.64
    }
    
    in Django REST Framework (DRF) bezieht sich validated_data auf die Daten,
    die bereits durch den Serializer validiert wurden und die in der Regel 
    aus dem Request-Body stammen.


"""
class CreateOrderNormalSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    # I want to validate this "cart_id" , 注意命名规则
    def validate_cart_id(self, cart_id):
        # if the cart uuid is not valid/does not exist
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("no cart with the given id found")
        # if the cart items array is empty:
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError("cart can not be empty")
        return cart_id

    # do the DIY logic inside of saving
    def save(self, **kwargs):
        # use transaction:
        with transaction.atomic():
            # 前提在 request_body 你需要有 "cart_id"
            cart_id = self.validated_data.get("cart_id")
            user_id = self.context.get("user_id")

            # create an Order, we need "customer_id", this can be via "user" or via "cart", both of them contains customer
            # get customer_id from "cart"
            cart = Cart.objects.get(pk=cart_id)

            # you don't need to save any more, because create() will save to database
            order = Order.objects.create(customer_id=cart.customer_id)

            # now create order-items through cart-items
            # get query set
            cart_items_queryset = CartItem.objects.select_related("product").filter(cart_id=cart_id)
            # create OrderItem
            order_items = [
                OrderItem(
                    order_id = order.id,
                    product_id = item.product.id,
                    quantity = item.quantity
                ) for item in cart_items_queryset
            ]

            # save the orderitems into database
            OrderItem.objects.bulk_create(order_items)

            # and then you need to delete the Cart
            Cart.objects.filter(pk=cart_id).delete()

            # here we need to fire our signals:
            # pass the sender = self.__class__(this is the current instance class)
            # pass extra data "order"
            # the handler of this signal is in "core" app
            order_created_signal.send_robust(self.__class__, order=order)

            # return order Obj
            return order


class UpdateOrderModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["payment_status"]







