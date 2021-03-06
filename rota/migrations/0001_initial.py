# Generated by Django 2.2.26 on 2022-03-22 02:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('requested_by_staff', models.CharField(max_length=80)),
                ('request_id', models.AutoField(primary_key=True, serialize=False)),
                ('staff_job_title', models.CharField(max_length=40)),
                ('request_date', models.DateTimeField(max_length=10)),
                ('shift_time', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('timetable_id', models.AutoField(primary_key=True, serialize=False)),
                ('staff_name', models.CharField(max_length=80)),
                ('registration_id', models.CharField(max_length=10)),
                ('day', models.CharField(max_length=2)),
                ('week_name', models.CharField(max_length=30)),
                ('month_name', models.CharField(max_length=30)),
                ('date', models.DateTimeField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('registration_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('job_title', models.CharField(max_length=40)),
                ('job_id', models.CharField(max_length=1)),
                ('phone_number', models.CharField(max_length=15)),
                ('ward', models.CharField(max_length=40)),
                ('date_admission', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
