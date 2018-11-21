import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
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
    activation_code = models.UUIDField(null=False, default=uuid.uuid1)

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
    teacher = models.ForeignKey(Teacher, null=False, blank=False, verbose_name="استاد", on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False, verbose_name="تاریخ")
    start = models.TimeField(null=False, blank=False, verbose_name="ساعت شروع")
    end = models.TimeField(null=False, blank=False, verbose_name="ساعت پایان")
    student_capacity = models.PositiveIntegerField(null=False, blank=False, verbose_name="ظرفیت")
    reserved = models.ManyToManyField(Student, blank=True, default=[], through="ReservedFreeTimes")

    def free_capacity(self):
        return self.student_capacity - self.reserved.count()

    def __str__(self):
        return self.teacher.__str__() + " " + \
               self.date.__str__() + " " + \
               self.start.__str__() + " " + \
               self.end.__str__() + " " + \
               self.student_capacity.__str__()

    class Meta:
        verbose_name_plural = "Meetings"

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self.id is not None and self.free_capacity() < 0:
            raise ValidationError("ظرفیت جدید کمتر از تعداد رزروها است")
        if 'start' not in exclude:
            if 'end' not in exclude:
                self.clean_end()
                self.clean_start()

    def clean_end(self):
        if self.start >= self.end:
            raise ValidationError("زمان شروع باید قبل از زمان پایان فرصت باشد")

    def clean_start(self):
        have_intersect_error = "بازه زمانی انتخاب شده با فرصت های قبلی شما اشتراک دارد"
        q = TeacherFreeTimes.objects.filter(teacher=self.teacher, date=self.date)
        if self.id:
            q = q.filter(~Q(id=self.id))
        for x in q:
            if not ((x.end < self.start) or (self.end < x.start)):
                raise ValidationError(have_intersect_error)


class ReservedFreeTimes(models.Model):
    free_time = models.ForeignKey(TeacherFreeTimes, on_delete=models.CASCADE, null=False, blank=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Reserved Meetings'

    def __str__(self):
        return self.student.__str__() + " " + self.free_time.__str__()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name="notifications")
    text = models.TextField(null=False, blank=True)

    def __str__(self):
        return self.user.__str__() + " " + self.text
