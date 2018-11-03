from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False)
    last_name = forms.CharField(
        max_length=30, required=False)
    email = forms.EmailField(
        max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['password_mismatch'] = "رمزعبور و تکرار رمز عبور یکسان نیستند."

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', )
        error_messages = {
            'username':{
                'unique': "کاربری با نام کاربری وارد شده وجود دارد."
            }
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'کاربری با ایمیل وارد شده وجود دارد.')
        return email
