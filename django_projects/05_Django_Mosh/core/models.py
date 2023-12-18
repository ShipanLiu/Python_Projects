from django.db import models
from django.contrib.auth.models import AbstractUser # we should use this one
# from django.contrib.auth.models import User


# we need to extend the AbstractUser class to modify some fields
# the name HAS TO BE "User"
class User(AbstractUser):
   email = models.EmailField(unique=True)
   # 这个自定义的 User 不能在 middle of the project  创建， 会有migrationProblem
   # 这里我定义了 但是 我错过了最好的时机， 即在 Project 开始的时候就要定义，否则只能drop databse
   # so I have droped my database at the end