from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.

#a Product can have a lot of Promotions
#a Promotion can be applied to different Product
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)


    class Meta:
        db_table = "t03_store_promotion"

# a collection(分类) can have many products
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+') # + tells django not to create reverse relationship(collection 中有 product， product 中有 relation？)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "t03_store_collection"

    def __str__(self) -> str:
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=255)
    # the slug field is using Django's SlugField, which is a field for storing slugs
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        default=0,
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    #库存
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    # if you delete a collection: you don;t delete
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name="products")
    promotions = models.ManyToManyField(Promotion, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "t03_store_product"
        ordering = ['title']

    def __str__(self) -> str:
        return f"product name: {self.title}"


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        # MEMBERSHIP_BRONZE 是为了数据库， 其值是 ‘B’， ‘Bronze’ 是 human readable name
        # 问题： 既然 你都有 MEMBERSHIP_GOLD = 'G' 了， 为什么还需要 (MEMBERSHIP_GOLD, 'Gold')？
        # 那是因为 之后会有一个 下拉框， 下拉框里面 会显示 'Gold'
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True) # this field can be null
    # choices 是 possiable values of the field
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "t03_store_customer"


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # 一个 customer 可以有很多 addresses
    # on_delete=models.CASCADE ==> if we delete a customer, the all addresses will be deleted
    # on_delete=models.SETNULL ==> if the parent(customer) got deleted, then the addresses related will be set null
    #       the problem is: this attribute doesnot set "null=True", so we can't use "on_delete=models.SETNULL" here
    # on_delete=models.PROTECT ==> if a customer has addresses set, then this customer can't be deleted(child 限制 parent)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = "t03_store_address"

# 这是 一个大的Order， 里面有很多 products， 即 orderItems(Foreignkey 定义到 OrderItem 里面)
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    # 一个customer 对多个 orders， 所以 foreign key 定义在多的一方
    # a customer can have a lot of orders
    # 原则：orders can never be deleted(可以set 成 true 或 false)，because of this, you can't delete a customer with orders exist
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = "t03_store_order"


class OrderItem(models.Model):
    # an Order can have multiple OrderItems
    # if one Order has at least 1 OrderItem, then it can't be deleted.
    order = models.ForeignKey(Order, on_delete=models.PROTECT)


    '''
    Product: "The Great Gatsby" is a single product in the bookstore's catalog.
    OrderItem #1: Customer A places an order for 2(quantity) copies of "The Great Gatsby."
    OrderItem #2: Customer B places an order for 3(quantity) copies of "The Great Gatsby."
    OrderItem #3: Customer C places an order for 1(quantity) copy of "The Great Gatsby."
    Here, we have three different OrderItem objects, all referring to the same Product ("The Great Gatsby"). This creates a many-to-one relationship between OrderItem and Product.
    
    '''
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    # to prevent from saving negativ numbers
    quantity = models.PositiveSmallIntegerField()



    # the price of product can be changed all the time, so we have to save
    # the price of product at the time it is orderd. (用户下单的时候是 200 元， 不能过了一天变成400元了)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "t03_store_orderitem"



# there are a lot of cart that belong to a lot of customers,
# you only need a cart id(this will be automatically created)
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = "t03_store_cart"


class CartItem(models.Model):
    # 1 Cart can have a lot of Car  tItems
    # if you delete a Cart, then you delete all the CartItems
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    #如果你下架了一个product, 那么这个 product 就应该删除所有的对应的 CartItem
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "t03_store_cartitem"
