from django.db import models

# Create your models here.

class Question(models.Model):
    # 这是 最开始 创建的 字段， 不用 写 default, 写上也无所谓
    question_title = models.CharField(max_length=50, default="default_title: question_text")
    question_text = models.CharField(max_length=200, default="default_value: question_text")
    create_time = models.DateTimeField("create time", auto_now_add=True)
    update_time = models.DateTimeField("update time", auto_now=True)
    class Meta:
        db_table = 'a03_question'


class Person(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    password = models.CharField(max_length=8)
    sex = models.CharField(max_length=5)
    salary = models.FloatField()

    def __str__(self):
        return f"name: {self.name}, age: {self.age}, sex: {self.sex}, salary: {self.salary}"
    class Meta:
        db_table = "a03_person"

