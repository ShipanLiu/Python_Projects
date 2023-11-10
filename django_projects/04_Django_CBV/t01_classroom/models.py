from django.db import models

# Create your models here.
# 你也想用 BaseModel 类， 就需要 import
from t00_common.models import BaseModel2

class Classroom(BaseModel2):
    class_nr = models.IntegerField(verbose_name="class nr")

    class Meta:
        db_table = 't01_classroom'

    def __str__(self):
        return f'classroomId: {self.id}, classroomNr: {self.class_nr}'

class Teacher(BaseModel2):
    first_name = models.CharField(verbose_name='first name', max_length=20)
    last_name = models.CharField(verbose_name='last name', max_length=20)
    # related_name='teacher' 是 服务于 Subject 的。
    subjects = models.ManyToManyField('Subject', related_name='teacher')  # Corrected field type

    class Meta:
        db_table = "t01_teacher"

    def __str__(self):
        # 打印出老师 所有的 课：
        subjectArr = []
        for subject in self.subjects.all():
            subjectArr.append(subject.subject_name)
        # join method in Python is used to concatenate the elements of an iterable (such as a list or tuple)
        # into a single string, using a specified separator. 格式： separator.join(iterable)
        subjectNameList = ', '.join(subjectArr)
        return f'teacher: {self.first_name} {self.last_name} teaches {self.subjectNameList}'

class Subject(BaseModel2):
    subject_name = models.CharField('subject name', max_length=30)

    class Meta:
        db_table = "t01_subject"

    def __str__(self):
        return f'subject: {self.subject_name}'  # Corrected string representation






