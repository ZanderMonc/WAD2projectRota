from django import forms
from django.forms import ModelForm, DateInput
from django.contrib.auth.models import User
from rota.models import UserProfile, Request


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password",)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name", "job_title", "job_id", "phone_number", "ward",)

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name", "job_title", "phone_number", "ward",)
        exclude = ('user',)

class ShiftForm(ModelForm):
    class Meta:
        model = Request
        # format to make date time show on fields because datetime-local HTML5 input type
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ShiftForm, self).__init__(*args, **kwargs)
        # parse HTML5 datetime-local input to datetime field
        #self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        #self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
