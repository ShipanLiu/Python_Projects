from django.db import models

from django.db import models
from t00_common.models import BaseModel2

class School(BaseModel2):
    school_name = models.CharField(max_length=50)

    class Meta:
        db_table = 't01_school'
    def __str__(self):
        return f'school name: {self.school_name}'


