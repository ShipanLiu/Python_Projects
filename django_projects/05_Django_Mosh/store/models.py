from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.contrib import admin

from uuid import uuid4


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    # '+' it instructs Django not to create a reverse relation from the related object back to the object with the ForeignKey.
    # 因为 Product class 已经有了 collection 这个key, so Collection class can't have a product key: deadloop
    # on_delete=models.SET_NULL: if the product is deleted, then the "featured_product" will be set to null
    # 因为null=True, 所以 在POST request 的时候， "featured_product" is not required.
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=255)
    # For example, a URL like /products/red-sports-car , "-"\'
    slug = models.SlugField()
    # null=True means it is optional，在POSt 的时候， This field is NOT required
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    # 存货清单
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    # optional, because FK
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name="products")
    # this field is also optional, because it is a many-to-many field
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    # "Customer" is a profile, and a profile should one-to-one map to a user
    # don't use "core.user"  , please use "settings.AUTH_USER_MODEL", so that the app will keep independent
    # if you delete a profile, then the user will also be deleted
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 这里相当于 "Customer" 有了 "first_name" 这个field
    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name

    def email(self):
        return self.user.email

    @admin.display(ordering="user__last_name")
    def last_name(self):
        return self.user.last_name

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


# this is the complete order, in this order there are a lot of items.
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        # this will be written into the table and add a tuple: "auth_permission"
        permissions = [
            ("cancel_order", "Can cancel order")
    ]


# this is a specific item in the order
# 1 OrderItem is a just a Product, and here field "product" is a FK, and it points to Product
# Product 是 1， OrderItem 是 多。
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="orderitems")
    # if the referenced Product is attempted to be deleted, then check
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="orderitems")
    quantity = models.PositiveSmallIntegerField()
    order_item_total_price = models.DecimalField(max_digits=6, decimal_places=2)

    # order_item_total_price need to be calculated before saving into the table
    def save(self, *args, **kwargs):
        # if the passed "order_item_total_price" has null value
        if not self.order_item_total_price:
            self.order_item_total_price = self.product.unit_price * self.quantity
        super().save(*args, **kwargs)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    # I don't want the hacker to know about my id, so I need to use GUID and redefine the PK
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    # this cartitem is actually which product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        # we don't want the user add the same product twice in a cart
        unique_together = [['cart', 'product']]




# >>>>>>>here is new defined Models>>>>>>>>>>>>>>>>>>>>>


# for example reviews from many customer of a product
class Review(models.Model):
    # if you delete a product, then all the reviews will be deleted
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    create_date = models.DateField(auto_now_add=True, null=True)
    update_date = models.DateField(auto_now=True, null=True)

    def __str__(self) -> str :
        return f"Review with id: {self.id} + name: {self.name}"

    # database name
    class Meta:
        db_table = "store_review"
        # Order by "create_date" in descending order
        ordering = ["-create_date"]

