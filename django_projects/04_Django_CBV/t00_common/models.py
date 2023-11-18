from django.db import models

'''
这个 app 是 放common 内容的， 这里的 models.py  也放 common 的内容 
'''


# Create your models here.
from django.db import models

# 创建一个
class BaseModel2(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract: True
        db_table = 'Shared_Model_BaseModel2'

