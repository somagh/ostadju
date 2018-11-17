from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import ListView

from people.decorators import is_teacher_check
from people.forms import SignUpForm, ContactUsForm, EditProfileUserForm, TeacherFreeTimeForm
from people.models import User, Teacher, TeacherFreeTimes


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
def profile(request, username=""):
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'base.html', {'message': 'کاربری با این نام کاربری وجود ندارد'})
    else:
        user = request.user
    return render(request, 'people/profile.html', {'user': user})


@login_required
def edit_profile(request):
    if request.method == 'POST':

        form = EditProfileUserForm(instance=request.user, data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            return redirect('people:profile')
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
        form = TeacherFreeTimeForm(data=request.POST)
        if form.is_valid():
            instance = form.save(False)
            instance.teacher = request.user.teacher
            instance.save()
            return redirect('home')
    else:
        form = TeacherFreeTimeForm()
    return render(request, 'people/new_teacher_free_time.html', {"form": form})


@login_required()
@user_passes_test(test_func=is_teacher_check)
def teacher_free_times(request):
    free_times = TeacherFreeTimes.objects.filter(teacher=request.user.teacher)
    return render(request, 'people/teacher_free_times.html', {'free_times': free_times})


def delete_teacher_free_time(request, free_time_id):
    try:
        teacher_free_time = TeacherFreeTimes.objects.get(id=free_time_id)
        teacher_free_time.delete()
        message = 'فرصت مورد نظر حذف شد'
    except TeacherFreeTimes.DoesNotExist:
        message = 'فرصتی با شماره داده شده وجود ندارد'
    return render(request, 'base.html', {'message': message})
