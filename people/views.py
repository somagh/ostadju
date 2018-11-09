from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from people.forms import SignUpForm, ContactUsForm, EditProfileUserForm
from people.models import User


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

        form = EditProfileUserForm(instance=request.user, data=request.POST)

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
