from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from people.forms import SignUpForm, ContactUsForm


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
