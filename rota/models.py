from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    registration_id = models.AutoField(primary_key = True)
    first_name = models.CharField(max_length = 40)
    last_name = models.CharField(max_length = 40)
    job_title = models.CharField(max_length = 40)
    job_id = models.CharField(max_length = 1)
    phone_number = models.CharField(max_length = 15)
    ward = models.CharField(max_length=40)
    date_admission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Request(models.Model):
    requested_by_staff = models.CharField(max_length = 80)
    request_id = models.AutoField(primary_key = True)
    request_type = models.CharField(max_length=40)
    request_date = models.DateTimeField(max_length = 10)
    date_requesting = models.DateTimeField(max_length = 10)
    swap_staff = models.CharField(max_length = 80)

    def __str__(self):
        return self.request_id

class Timetable(models.Model):
    timetable_id = models.AutoField(primary_key = True)
    staff_name = models.CharField(max_length = 80)
    registration_id = models.CharField(max_length=10)
    day = models.CharField(max_length=2)
    week_name = models.CharField(max_length=30)
    month_name = models.CharField(max_length=30)

    def __str__(self):
        return self.timetable_id
