from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from people.constants import GENDER_CHOICES


def get_picture_filename(instance, filename):
    return instance.username + "/" + filename


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    bio = MarkdownxField(max_length=500, blank=True, verbose_name="زندگی نامه", default="")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="جنسیت", blank=True)
    picture = models.ImageField(null=True, upload_to=get_picture_filename, verbose_name="عکس پروفایل", blank=True)

    @property
    def get_bio(self):
        return markdownify(self.bio)

    def profile_url(self):
        return reverse("people:profile", kwargs={"username": self.username})

    def __str__(self):
        return self.username

    def json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'profile_url': self.profile_url(),
        }


class Student(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name="student", )

    def __str__(self):
        return self.user.__str__()


class Teacher(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name="teacher", )

    def __str__(self):
        return self.user.__str__()


class TeacherFreeTimes(models.Model):
    teacher = models.ForeignKey(Teacher, null=False, blank=False, verbose_name="استاد")
    start = models.DateTimeField(null=False, blank=False, verbose_name="زمان شروع")
    end = models.TimeField(null=False, blank=False, verbose_name="ساعت پایان")
    student_capacity = models.PositiveIntegerField(null=False, blank=False, verbose_name="ظرفیت", )

    def __str__(self):
        return self.teacher.__str__() + " " + \
               self.start.__str__() + " " + \
               self.end.__str__() + " " + \
               self.student_capacity.__str__()

    class Meta:
        verbose_name_plural = "Teacher Free Times"
