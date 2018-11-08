from django.contrib.auth.models import AbstractUser
from django.db import models

from people.constants import GENDER_CHOICES


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Student(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name="student", )

    bio = models.TextField(max_length=500, blank=True, verbose_name="زندگی نامه")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="جنسیت")

    def __str__(self):
        return self.user.__str__()
