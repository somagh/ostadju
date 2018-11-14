from django.contrib import admin

from people.models import User, Student, Teacher

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)

# Register your models here.
