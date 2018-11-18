from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from people.decorators import is_teacher_check, is_student_check
from people.forms import SignUpForm, ContactUsForm, EditProfileUserForm, TeacherFreeTimeForm
from people.models import User, Teacher, TeacherFreeTimes, Notification, ReservedFreeTimes


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'people/signup.html', {'form': form})


def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(form.cleaned_data['title'],
                      "فرم تماس با ما با اطلاعات زیر پر شده است\n ایمیل:‌{} \n متن:{}".format(
                          form.cleaned_data['email'], form.cleaned_data['text']), from_email=form.cleaned_data['email'],
                      recipient_list=["ostadju@fastmail.com"],
                      fail_silently=True)
            return render(request, 'people/contact_us_success.html')
    else:
        form = ContactUsForm()
    return render(request, 'people/contact_us.html', {'form': form})


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'base.html', {'message': 'کاربری با این نام کاربری وجود ندارد'})
    free_times = ""
    if user.is_teacher:
        free_times = TeacherFreeTimes.objects.filter(teacher=user.teacher)
    elif user.is_student:
        query_set = ReservedFreeTimes.objects.filter(student=request.user.student)
        free_times = []
        for query in query_set:
            free_times.append(query.free_time)
    return render(request, 'people/profile.html', {'user': user,
                                                   'free_times': free_times})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileUserForm(instance=request.user, data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            return redirect(request.user.profile_url())
        else:
            message = 'اطلاعات وارد شده معتبر نمی‌باشد'
    else:
        message = ""
        form = EditProfileUserForm(instance=request.user)

    return render(request, 'people/edit_profile.html', {'form': form,
                                                        'message': message})


class SearchProfiles(ListView):
    model = Teacher
    template_name = "people/search_profiles.html"
    context_object_name = "teachers"

    def get_queryset(self):
        text = self.request.GET.get("search", "")
        query_set = Teacher.objects.filter(user__first_name__contains=text)
        query_set |= Teacher.objects.filter(user__last_name__contains=text)
        query_set |= Teacher.objects.filter(user__username__contains=text)
        return query_set


@login_required()
@user_passes_test(test_func=is_teacher_check)
def new_teacher_free_time(request):
    if request.method == "POST":
        instance = TeacherFreeTimes(teacher=request.user.teacher)
        form = TeacherFreeTimeForm(data=request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return render(request, 'base.html', {'message': "درخواست شما با موفقیت ثبت شد"})
    else:
        form = TeacherFreeTimeForm()
    return render(request, 'people/teacher_free_time_form.html', {"form": form})


def delete_teacher_free_time(request, free_time_id):
    try:
        teacher_free_time = TeacherFreeTimes.objects.get(id=free_time_id)
        if teacher_free_time.teacher != request.user.teacher:
            message = "فرصت مورد نظر متعلق به شما نیست"
        else:
            for student in teacher_free_time.reserved.all():
                teacher_user = teacher_free_time.teacher.user
                text = "فرصتی که شما از استاد " \
                       "{last_name} {first_name} " \
                       "در تاریخ {self.date} از ساعت {self.start} تا ساعت" \
                       " {self.end} گرفته بودید حذف گردید".format(self=teacher_free_time,
                                                                  first_name=teacher_user.first_name,
                                                                  last_name=teacher_user.last_name)
                notification = Notification(user=student.user, text=text)
                notification.save()
            teacher_free_time.delete()
            return redirect('home')
    except TeacherFreeTimes.DoesNotExist:
        message = 'فرصتی با شماره داده شده وجود ندارد'
    return render(request, 'base.html', {'message': message})


def search_teachers_api_view(request):
    query = request.GET.get('query', '')
    query_set = Teacher.objects.filter(user__first_name__contains=query)
    query_set |= Teacher.objects.filter(user__last_name__contains=query)
    query_set |= Teacher.objects.filter(user__username__contains=query)

    result = []
    for teacher in query_set:
        result.append(teacher.user.json())
    return JsonResponse(result, safe=False)


@login_required()
@user_passes_test(test_func=is_teacher_check)
def update_teacher_free_time(request, free_time_id):
    free_time = TeacherFreeTimes.objects.get(id=free_time_id)
    message = ""
    if free_time.teacher != request.user.teacher:
        message = "فرصت مورد نظر متعلق به شما نیست"
    if request.method == "POST":
        form = TeacherFreeTimeForm(data=request.POST, instance=free_time)
        if form.is_valid():
            form.save()
            return render(request, 'base.html', {'message': "درخواست شما با موفقیت ثبت شد"})
    else:
        form = TeacherFreeTimeForm(instance=free_time)
    return render(request, 'people/teacher_free_time_form.html', {"form": form, 'message': message})


@login_required()
def seen_notification(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        if notification.user != request.user:
            return render(request, 'home.html', {'message': 'اطلاعیه مورد نظر متعلق به شما نیست'})
        else:
            notification.delete()
            return redirect('home')
    except Notification.DoesNotExist:
        return render(request, 'home.html', {'message': 'اطلاعیه ای با شماره داده شده وجود ندارد'})


@login_required()
@user_passes_test(test_func=is_student_check)
def reserve_free_time(request, free_time_id):
    try:
        teacher_free_time = TeacherFreeTimes.objects.get(id=free_time_id)
    except TeacherFreeTimes.DoesNotExist:
        return render(request, 'home.html', {'message': 'فرصتی با شماره داده شده وجود ندارد'})
    if teacher_free_time.free_capacity() <= 0:
        return render(request, 'home.html', {'message': 'فرصت مورد نظر ظرفیت خالی ندارد'})
    x = ReservedFreeTimes(free_time=teacher_free_time,
                          student=request.user.student)
    x.save()
    return render(request, 'home.html', {'message': 'فرصت مورد نظر با موفقیت رزرو شد'})
