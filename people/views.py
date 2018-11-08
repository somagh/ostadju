from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from people.forms import SignUpForm, ContactUsForm, EditProfileForm


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
            return render(request, 'people/contact_us_success.html')
    else:
        form = ContactUsForm()
    return render(request, 'people/contact_us.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'people/profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            form = EditProfileForm()
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            user.save()
            message = 'درخواست شما با موفقیت انجام شد'
        else:
            message = 'نام یا نام خانوادگی وارد شده معتبر نمی‌باشد'
    else:
        message = ""
        form = EditProfileForm()
    return render(request, 'people/edit_profile.html', {'form': form, 'message': message})
