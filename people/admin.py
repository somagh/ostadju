from django.contrib import admin

from people.models import User, Student, Teacher, TeacherFreeTimes, ReservedFreeTimes, Notification


class ReservedFreeTimesInline(admin.StackedInline):
    model = ReservedFreeTimes
    extra = 1


class TeacherFreeTimesAdmin(admin.ModelAdmin):
    inlines = [ReservedFreeTimesInline]


admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(TeacherFreeTimes, TeacherFreeTimesAdmin)
admin.site.register(ReservedFreeTimes)
admin.site.register(Notification)
# Register your models here.
