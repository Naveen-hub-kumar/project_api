from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from .models import Teacher


# REGISTER FORM
class RegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:

        model = User

        fields = [

            'username',

            'email',

            'password1',

            'password2'

        ]


# TEACHER FORM
class TeacherForm(forms.ModelForm):

    class Meta:

        model = Teacher

        fields = [

            'phone',

            'subject'

        ]