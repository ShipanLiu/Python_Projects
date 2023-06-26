from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField("person_name", max_length=20)
    age = models.IntegerField("person_age", help_text=">18")

    def __str__(self):
        return f"{self.pk}--{self.name}--{self.age}"
    class Meta:
        db_table = "a06_perosn"
        verbose_name_plural = verbose_name = "a06_perosn"

class Worker(models.Model):
    name = models.CharField("worker_name", max_length=20, null=True, blank=True) # 对数据库 和 ORM 你都以为可空
    age = models.IntegerField("worker_age", help_text=">18")

    def __str__(self):
        return f"{self.pk}--{self.name}--{self.age}"
    class Meta:
        db_table = "a06_worker"
        verbose_name_plural = verbose_name = "a06_worker"

