from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from people.decorators import is_student_check
from people.forms import SignUpForm, ContactUsForm, EditProfileStudentForm, EditProfileUserForm


# Create your views here.


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
def profile(request):
    return render(request, 'people/profile.html', {'user': request.user})


@login_required
@user_passes_test(test_func=is_student_check)
def edit_profile(request):
    if request.method == 'POST':

        form1 = EditProfileUserForm(instance=request.user, data=request.POST)
        form2 = EditProfileStudentForm(instance=request.user.student, data=request.POST)

        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            message = 'درخواست شما با موفقیت انجام شد'
        else:
            message = 'اطلاعات وارد شده معتبر نمی‌باشد'
    else:
        message = ""
        form1 = EditProfileUserForm(instance=request.user)
        form2 = EditProfileStudentForm(instance=request.user.student)

    return render(request, 'people/edit_profile.html', {'form1': form1,
                                                        'form2': form2,
                                                        'message': message})
