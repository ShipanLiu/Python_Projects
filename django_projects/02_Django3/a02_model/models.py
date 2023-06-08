from django.db import models

# Create your models here.

class Question(models.Model):
    # 这是 最开始 创建的 字段， 不用 写 default
    question_text = models.CharField(max_length=200)
    create_time = models.DateTimeField("create time", auto_now_add=True)
    update_time = models.DateTimeField("update time", auto_now=True)
    # 这是新增的attribute： 为照顾老attribute， 需要设置 default
    question_title = models.CharField(max_length=50, default="")


    class Meta:
        db_table = 'a02_question'


##############一对多#################
class Manufacture(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return "manufacture: %s"%(self.name)

    class Meta:
        db_table = 'a02_manufacture'



class Car(models.Model):
    name = models.CharField(max_length=20)
    #mysql 字段名自动为： manufacture.id
    manufacture = models.ForeignKey(Manufacture, on_delete=models.CASCADE)

    def __str__(self):
        return "car: %s, manufacture: %s"%(self.name, self.manufacture)

    class Meta:
        db_table = 'a02_car'

# 针对一对多 ： 因为FK 在 多的一方， 所以 先添加 一的一方， 再添加 多的一方
# >>> honda = Manufacture.objects.create(name="honda")
# >>> honda
# <Manufacture: Manufacture object (2)>
# >>> man = Manufacture.objects.get(name="honda")
# >>> honda_jazz = Car.objects.create(name="honda jazz", manufacture=man)
# >>> honda_jazz
# <Car: Car object (1)>

# a02_manufacture
  # 1,toyota
  # 2,honda

# a02_car:
  # 1,honda jazz,2




##############一对一#################
# 一个 Place 有  一个  Restaurant   ， 有多个   Waiter

class Place(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return "place: %s"%(self.name)
    class Meta:
        db_table = 'a02_place'

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    # 会在mysql 中生成  place_id
    place = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=True)

    serves_hot_dog = models.BooleanField(default=True)
    serves_pizza = models.BooleanField(default=True)

    def __str__(self):
        return "resuaurant: %s"%(self.name)
    class Meta:
        db_table = 'a02_restaurant'

class Waiter(models.Model):
    name = models.CharField(max_length=50)
    # 会在 mysql 中生成 restaurant_id
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return "waiter: %s at %s"%(self.name, self.restaurant)
    class Meta:
        db_table = 'a02_waiter'


#如何 插入值？
# step1: create place
# step2: 用 Place.objects.get() 查出 Place， 之后   create restaurant
# step3: 用 Restaurant.objects.get() 查出 Restaurant， 之后   create waiter

##############多对多#################

#  自己关联自己
# 创建 "a02_student" table
# 会创建 "a02_student_friends" table里面有attributes： “from_student_id”, "to_student_id"
class Student(models.Model):
    name = models.CharField(max_length=20)
    # 注意 “self” 有 “”
    friends = models.ManyToManyField("self")

    def __str__(self):
        return "student name: %s"%(self.name)
    class Meta:
        db_table = 'a02_student'


# 不是 自关联， 而是 normal fall
# 1 "Teacher" has many "Class",  1 "Class" has many "teachers"
# 会生成三张表 ： "a02_teacher",  "a02_school_class", "a02_teacher_school_class"

class SchoolClass(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return "school class name: %s"%(self.name)
    class Meta:
        db_table = 'a02_school_class'

class Teacher(models.Model):
    name = models.CharField(max_length=50)
    school_class = models.ManyToManyField(SchoolClass)

    def __str__(self):
        return "teacher name: %s"%(self.name)
    class Meta:
        db_table = 'a02_teacher'





# 多对多， 自定义中间表的 情况

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # 因为timestamp 是后加的， 所以 需要指定 default 值
    create_time = models.DateTimeField("create time", auto_now_add=True, null=True, blank=True)
    update_time = models.DateTimeField("update time", auto_now=True, null=True, blank=True)

    def __str__(self):
        return "persion fullname: %s - %s"%(self.first_name, self.last_name)

    class Meta:
        db_table = "a02_person"

class Group(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(
        Person,
        through="Membership",
        through_fields=("person", "group")
    )
    create_time = models.DateTimeField("create time", auto_now_add=True, null=True, blank=True)
    update_time = models.DateTimeField("update time", auto_now=True, null=True, blank=True)

    def __str__(self):
        return "group name: %s"%(self.name)

    class Meta:
        db_table = "a02_group"


class Membership(models.Model):
    person = models.ForeignKey(Group, on_delete=models.CASCADE)
    group = models.ForeignKey(Person, on_delete=models.CASCADE)
    # 自定义： 表示 membership 的 等级
    level = models.IntegerField(default=1)
    create_time = models.DateTimeField("create time", auto_now_add=True, null=True, blank=True)
    update_time = models.DateTimeField("update time", auto_now=True, null=True, blank=True)

    def __str__(self):
        return "Membership: persion: %s, group: %s"%(self.person,  self.group)

    class Meta:
        db_table = "a02_membership"

# 添加 Person
# >>> from a02_model.models import *
# >>> p2 = Person.objects.create(first_name="Jier", last_name="Liu")
# >>> p2
# <Person: persion fullname: Jier - Liu>



#添加 Group（不用考虑关联， 最简单的 创建即可）
# >>> g1 = Group.objects.create(name="group1")
# >>> g2 = Group.objects.create(name="group2")
# >>> p
# <Person: persion fullname: Ted - Liu>


#关联 Person 和 Group
# 给Group 里的members 来 赋值。
# >>> g1.members.set([1,2])


# 查看 a02_membership
# 1(id),1(level),1(group_id),1(person_id),2023-06-08 18:37:52.122945(create_time),2023-06-08 18:37:52.122945(update_time)
# 2,1,2,1,2023-06-08 18:37:52.122945,2023-06-08 18:37:52.122945







