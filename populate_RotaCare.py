import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RotaCare.settings')

import django

django.setup()

from django.contrib.auth.models import User
from rota.models import UserProfile, Request, Timetable


def populate():
    users = {'user': 'Jane Doe', 'registration_id': '100',
             'first_name': 'Jane', 'last_name': 'Doe',
             'job_title': 'Nurse', 'job_id': '0',
             'phone_number': '00000000000', 'ward': 'A2'}
    for i in range(10):
        #code to create random id, still chace of violating unique username: temp = int(users['registration_id']) + random.randint(0,10000)
        users['registration_id'] = str(i) #str(temp)
        add_UserProfile(registration_id=i, user=User.objects.create_user('jane-doe' + users['registration_id'], 'doe@nhs.com',
                                                                            'janepassword'))  # for loop adds two default jane doe users

        # users['registration_id'] = str(temp)

        add_Timetable()  # adds a default timetable object
        add_Request()  # adds a default request object


def add_UserProfile(registration_id, user,
                    first_name="Jane", last_name="Doe", job_title="Nurse",
                    job_id="0", phone_number="00000000000", ward="A2",
                    date_admission="2001-01-01 00:01"):
    user.save()
    u = UserProfile.objects.get_or_create(user=user, registration_id=registration_id, first_name=first_name,
                                          last_name=last_name, job_title=job_title, job_id=job_id,
                                          phone_number=phone_number, ward=ward, date_admission=date_admission)[0]
    u.save()
    return u


def add_Request(requested_by_staff="unknown", request_id="0", request_type="unknown", request_date="2001-01-01 00:01",
                date_requesting="2001-02-01 00:01", swap_staff="Jane Doe"):
    R = Request.objects.get_or_create(requested_by_staff=requested_by_staff,
                                      request_id=request_id,
                                      request_type=request_type,
                                      request_date=request_date,
                                      date_requesting=date_requesting,
                                      swap_staff=swap_staff)[0]
    R.save()
    return R


def add_Timetable(timetable_id="0", staff_name="Jane", registration_id="0", day="monday", week_name="third",
                  month_name="March"):
    T = Timetable.objects.get_or_create(timetable_id=timetable_id, staff_name=staff_name,
                                        registration_id=registration_id, day=day,
                                        week_name=week_name, month_name=month_name)[0]
    T.save()
    return T


if __name__ == '__main__':
    print("populating rota database")
    populate()
