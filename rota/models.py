from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    registration_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    job_title = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=15)
    ward = models.CharField(max_length=40)
    date_admission = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        super().save()
        if self.image != "":
            img = Image.open(self.image.path)  # Open image

            # resize image
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)  # Resize image
                img.save(self.image.path)  # Save it again and override the larger image


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
        return f'<a href="{url}"> {self.requested_by_staff + " - " + self.get_job_title} </a>'

    @property
    def get_job_title(self):
        return self.staff_job_title


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
