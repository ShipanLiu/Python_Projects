from django.db import models

# Create your models here.

class Student(models.Model):

    #在数据库中 保存 1， 2，但是在 admin 后台显示的是 男和女
    SEX_CHOICES = ((1, 'male'), (2, 'female'))

    name = models.CharField(verbose_name="name", max_length=20)
    #help_text:
    age = models.IntegerField(verbose_name="age", help_text="older than 18")

    #这是我迁移完之后 新增加的字段： 在不设置 default 的情况下 需要设置 null=True(照顾之前的老 records)
    sex = models.IntegerField("sex", choices=SEX_CHOICES, default=1)



    def __str__(self):
        sex = ""
        if self.sex == 1:
            sex = "male"
        else:
            sex = "female"
        return f"{self.name} -- {self.age} -- {sex}"
    class Meta:
        #更改在 数据库 里面的 table name
        db_table = 'a05_student'
        #更改在 admin 里面的 table name
        verbose_name_plural = verbose_name = 'a05_student(change in models.py)'



#<<<<<<<<<<<<<<<<<<<<现在开始探讨关系映射<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


#  一对多 和 一对一的 关系映射

class Place(models.Model):
    name = models.CharField("place_name", max_length=50) # 省略了 verbose_name=''
    address = models.CharField("address", max_length=80)

    def __str__(self):
        return f"{self.name} -- {self.address}"

    class Meta:
        verbose_name_plural = verbose_name = "a05_place" # 在 admin 显示
        db_table = "a05_place" # 在 db 显示

class Restaurant(models.Model):
    # mysql tale 里面会自动加上字段 "place_id"
    place = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=False, verbose_name="rest_addr")
    name = models.CharField("rest_name", max_length=50)
    # 加入我 insert 的时候，对serves_hot_dog 不做指示， 那么就会默认为false
    serves_hot_dog = models.BooleanField("serves_hot_dog", default=False)
    serves_pizza = models.BooleanField("serves_pizza", default=False)

    def __str__(self):
        return f"{self.pk}--{self.name}--{self.place.name}--{self.serves_hot_dog}--{self.serves_pizza}"
    class Meta:
        db_table = "a05_restaurant"
        verbose_name_plural = verbose_name = "a05_restaurant"

class Waiter(models.Model):
    # mysql tale 里面会自动加上字段 "restaurant_id"
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name="work_restaurant")
    name = models.CharField("waiter_name", max_length=40)
    def __str__(self):
        return f"{self.pk}-{self.name}--{self.restaurant.name}"
    class Meta:
        db_table = "a05_waiter"
        # 这是为了在admin 里面显示 这个table 的名字
        verbose_name_plural = verbose_name = "a05_waiter"


# 开始  多对多的 关系映射
class SchoolClass(models.Model):
    name = models.CharField(verbose_name="schoolclass_name", max_length=50)
    def __str__(self):
        return f"{self.name}"
    class Meta:
        db_table = "a05_schoolclass"
        verbose_name_plural = verbose_name = "a05_schoolclass"

class Teacher(models.Model):
    name = models.CharField("teacher_name", max_length=20)
    school_class = models.ManyToManyField(SchoolClass, verbose_name="school_class")

    def __str__(self):
        # 一个老师可能教授多个班级， 所以 这里不能用 self.school_class.name
        return f"{self.name} teaches {self.school_class.all()}"
    class Meta:
        db_table = "a05_teacher"
        verbose_name_plural = verbose_name = "a05_teacher"
