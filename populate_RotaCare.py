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
        add_UserProfile(registration_id=i + 61, user=User.objects.create_user('jane' + str(i), 'doe' + users['registration_id'] + '@nhs.com',
         'janepassword'))  # for loop adds two
        # default jane doe users

        # users['registration_id'] = str(temp)

    add_Timetable()  # adds a default timetable object
    add_Request()  # adds a default request object


def add_UserProfile(registration_id, user):
    user.save()
    u, success = UserProfile.objects.get_or_create(user=user, registration_id=registration_id, first_name="Jane",
                                                   last_name="Doe", job_title="Nurse",
                                                   phone_number="00000000000", ward="A2",
                                                   date_admission=datetime.datetime.now(), image="Picture2.png")
    u.save()
    return u


def add_Request(requested_by_staff="unknown", request_id="0",
                request_date=datetime.datetime.now(), ):
    r, success = Request.objects.get_or_create(requested_by_staff=requested_by_staff,
                                               request_id=request_id,
                                               staff_job_title="Charge Nurse",
                                               request_date=request_date,
                                               shift_time="night_shift")
    r.save()
    return r


def add_Timetable():
    t, success = Timetable.objects.get_or_create(timetable_id="23", staff_name="Jane", registration_id="0", day="monday",
                                                 week_name="third",
                                                 month_name="March", date=datetime.datetime.now())
    t.save()
    return t


if __name__ == '__main__':
    print("populating rota database")
    populate()
