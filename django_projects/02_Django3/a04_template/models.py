from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    password = models.CharField(max_length=8)
    sex = models.CharField(max_length=5)
    salary = models.FloatField()
    create_time = models.DateTimeField("create time", auto_now_add=True)
    update_time = models.DateTimeField("update time", auto_now=True)

    def __str__(self):
        return f"name: {self.name}, age: {self.age}, sex: {self.sex}, salary: {self.salary}"
    class Meta:
        db_table = "a04_person"
