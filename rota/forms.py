from django import forms
from django.forms import ModelForm, DateInput
from django.contrib.auth.models import User
from rota.models import UserProfile, Request


# Form to create a user.
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password",)


# Form used to create a user profile.
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name", "job_title", "phone_number", "ward", "image",)


# Form used to update the user profile.
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name", "phone_number", "ward", "image",)
        exclude = ('user', "job_title")


# Form used to create a shift.
class ShiftForm(ModelForm):
    class Meta:
        model = Request
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ShiftForm, self).__init__(*args, **kwargs)
