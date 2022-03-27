from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    registration_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=40, default="FirstName")
    last_name = models.CharField(max_length=40, default="LastName")
    job_title = models.CharField(max_length=40, default="Staff Nurse")
    phone_number = models.CharField(max_length=15, default="12345678910")
    ward = models.CharField(max_length=40, default="Default")
    date_admission = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        super().save()

        if self.image != "":
            img = Image.open(self.image.path)

            # resize image
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Request(models.Model):
    requested_by_staff = models.CharField(max_length=80)
    request_id = models.AutoField(primary_key=True)
    staff_job_title = models.CharField(max_length=40)
    request_date = models.DateTimeField(max_length=10)
    shift_time = models.CharField(max_length=20)

    def __str__(self):
        return str(self.request_id)

    @property
    def get_html_url(self):
        url = reverse('rota:shift_edit', args=(self.request_id,))
        return f'<a href="{url}"> {self.requested_by_staff} </a>'

    @property
    def get_staff_name(self):
        return self.requested_by_staff

    @property
    def get_job_title(self):
        return self.staff_job_title

    @property
    def get_shift_time(self):
        return self.shift_time


class Timetable(models.Model):
    timetable_id = models.AutoField(primary_key=True)
    staff_name = models.CharField(max_length=80)
    registration_id = models.CharField(max_length=10)
    day = models.CharField(max_length=2)
    week_name = models.CharField(max_length=30)
    month_name = models.CharField(max_length=30)
    date = models.DateTimeField(max_length=10)

    def __str__(self):
        return str(self.timetable_id)
