import os
import random
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RotaCare.settings')

import django

django.setup()

from django.contrib.auth.models import User
from rota.models import UserProfile, Request, Timetable


def populate():
    users = {'user': 'Jane Doe', 'registration_id': '100',
             'first_name': 'Jane', 'last_name': 'Doe',
             'job_title': 'Nurse',
             'phone_number': '00000000000', 'ward': 'A2'}
    for i in range(10):
        # code to create random id, still chance of violating unique username:
        # temp = int(users['registration_id']) + random.randint(0,10000)
        users['registration_id'] = str(i)  # str(temp)
        if i < 2:
            job_title = "Charge Nurse"
        elif 2 < i < 5:
            job_title = "Staff Nurse"
        elif i > 5:
            job_title = "Healthcare Support Worker"

        add_UserProfile(registration_id=i,
                        job_title=job_title,
                        user=User.objects.create_user('jane' + str(i),
                                                      'doe' + users['registration_id'] + '@nhs.com',
                                                      'janepassword'))
        # for loop adds ten default jane doe users

    add_Timetable()  # adds the default timetable object

    # making shift requests below
    for i in range(100):
        user_num = random.randint(0, 9)  # for one of the base users;
        user = UserProfile.objects.filter(registration_id=str(user_num));
        day = random.randint(-60, 60)  # shifts appearing randomly between two months ago and two months ahead
        if day < 0:
            date_req = datetime.datetime.now() - datetime.timedelta(days=day)
        else:
            date_req = datetime.datetime.now() + datetime.timedelta(days=day)
        if day % 2 != 0:
            shift_time = "Night Shift"
        else:
            shift_time = "Day Shift"
        add_Request(requested_by_staff=str(user.first_name + user.last_name), request_id=str(i), request_date=date_req,
                    shift_time=shift_time, staff_job_title=user.job_title)
        # adds 30 default request objects once daily from the present day.


def add_UserProfile(user, registration_id="0",first_name="Jane",
                    last_name="Doe",job_title="Nurse", phone_number="00000000000", ward="A2",
                    date_admission=datetime.datetime.now(), image="Picture2.png"):
    user.save()
    u, success = UserProfile.objects.get_or_create(user=user, registration_id=registration_id, first_name=first_name,
                                                   last_name=last_name, job_title=job_title,
                                                   phone_number=phone_number, ward=ward,
                                                   date_admission=date_admission, image=image)
    u.save()
    return u


def add_Request(requested_by_staff="unknown", request_id="0",
                request_date=datetime.datetime.now(), staff_job_title="Staff Nurse", shift_time="night_shift"):
    r, success = Request.objects.get_or_create(requested_by_staff=requested_by_staff,
                                               request_id=request_id,
                                               staff_job_title=staff_job_title,
                                               request_date=request_date,
                                               shift_time=shift_time)
    r.save()
    return r


def add_Timetable(timetable_id="1", staff_name="admin", registration_id="0",
                  day="monday",
                  week_name="third",
                  month_name="March", date=datetime.datetime.now()):
    t, success = Timetable.objects.get_or_create(timetable_id=timetable_id, staff_name=staff_name,
                                                 registration_id=registration_id,
                                                 day=day,
                                                 week_name=week_name,
                                                 month_name=month_name, date=date)
    t.save()
    return t


if __name__ == '__main__':
    print("populating rota database")
    populate()
