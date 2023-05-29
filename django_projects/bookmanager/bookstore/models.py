from django.db import models

# Create your models here.

# 建立一个实体（也就是 一个table）
# 这个实体 extends 于 models.Model
class Book(models.Model):
    # verbose_name="the name" does not matter in mysql attributes, but will be first showed in the admin后台
    title = models.CharField(verbose_name="the name", max_length=50, default="", unique=True)
    # 默认 都是 非空的
    pub = models.CharField("publication", max_length=100, default="")
    # 两位小数
    price = models.DecimalField("the price", max_digits=7, decimal_places=2, default=0.0)
    # 增加一个字段
    info = models.CharField("the info", max_length=300, default="this is the default info about this book")
    market_price = models.DecimalField("the market price", max_digits=7, decimal_places=2, default=0.0)
    #标记是否删除
    is_active = models.BooleanField("is deleted", default=True)

    class Meta:
        db_table = 'book'  # table name will be no more "bookstore_book" , but "book"

    # 相当于 toString
    def __str__(self):
        return "%s_%s_%s_%s_%s_"%(self.title, self.pub, self.price, self.info, self.market_price)


class Author(models.Model):
    name = models.CharField("the name", max_length=20)
    age = models.IntegerField("the age", default=1)
    email = models.EmailField("the email",null=True)
    class Meta:
        db_table = 'author'



