from django.contrib import admin

from people.models import User, Student, Teacher, TeacherFreeTimes

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(TeacherFreeTimes)

# Register your models here.
