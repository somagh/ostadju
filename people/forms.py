from django import forms
from django.contrib.admin.widgets import AdminIntegerFieldWidget, AdminTimeWidget, AdminDateWidget
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import SelectDateWidget

from people.models import User, Student, Teacher, TeacherFreeTimes


class SignUpForm(UserCreationForm):
    type = forms.ChoiceField(choices=[('student', 'دانشجو'), ('teacher', 'استاد')], widget=forms.RadioSelect,
                             required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
        error_messages = {
            'username': {
                'unique': "کاربری با نام کاربری وارد شده وجود دارد."
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "نام کاربری"
        self.fields['password1'].label = "گذرواژه"
        self.fields['password2'].label = "تکرار گذرواژه"
        self.fields['first_name'].label = "نام"
        self.fields['last_name'].label = "نام خانوادگی"
        self.fields['email'].label = "ایمیل"
        self.fields['type'].label = "نوع"

        self.error_messages['password_mismatch'] = "گذرواژه و تکرار گذرواژه یکسان نیستند."

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'کاربری با ایمیل وارد شده وجود دارد.')
        return email

    def save(self, commit=True):
        user = super().save(False)
        # user.is_student = True
        user.is_student = self.cleaned_data['type'] == 'student'
        user.is_teacher = self.cleaned_data['type'] == 'teacher'
        if commit:  # anyway we need to save this user
            user.save()
        if user.is_student:
            user.student = Student.objects.create(user=user)
        if user.is_teacher:
            user.teacher = Teacher.objects.create(user=user)

        return user


class ContactUsForm(forms.Form):
    title = forms.CharField(max_length=40, label='عنوان')
    email = forms.EmailField(label='ایمیل', required=False)
    text = forms.CharField(label='متن', widget=forms.Textarea, min_length=10, max_length=250)


class EditProfileUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'gender', 'picture']
        labels = {
            "first_name": "نام",
            "last_name": "نام خانوادگی"
        }


class TeacherFreeTimeForm(forms.ModelForm):
    # widget = forms.widgets.DateTimeInput(attrs={'type': 'date', 'class': 'datetimeshortcuts'})
    # start = forms.DateTimeField(widget=widget)
    # end = forms.DateTimeField(widget=widget)

    class Meta:
        model = TeacherFreeTimes
        fields = ['date', 'start', 'end', 'student_capacity', ]
        widgets = {
            'date': AdminDateWidget(),
            'start': AdminTimeWidget(),
            'end': AdminTimeWidget(),
            'student_capacity': AdminIntegerFieldWidget(),
        }
        error_messages = {
            'end': {
                'invalid': 'زمان پایان وارد شده معتبر نمی‌باشد'
            },
            'start': {
                'invalid': 'زمان شروع وارد شده معتبر نمی‌باشد'
            },
            'date': {
                'invalid': 'تاریخ وارد شده معتبر نمی‌باشد'
            },
        }


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(required=True, label="ایمیل", error_messages={'invalid': 'ایمیل وارد شده صحیح نمی‌باشد'})


class ResetPasswordForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "گذرواژه"
        self.fields['password2'].label = "تکرار گذرواژه"
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""
        self.error_messages['password_mismatch'] = "گذرواژه و تکرار گذرواژه یکسان نیستند."
