from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.conf import settings
import os
import re
from django.test import TestCase
from django.urls import reverse

from rota.models import Request, UserProfile

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}RotaCare TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


def add_UserProfile(user, registration_id="0", first_name="Jane",
                    last_name="Doe", job_title="Nurse", phone_number="00000000000", ward="A2",
                    date_admission=datetime.now(), image=""):
    user.save()
    u, success = UserProfile.objects.get_or_create(user=user,
                                                   registration_id=registration_id,
                                                   first_name=first_name,
                                                   last_name=last_name,
                                                   job_title=job_title,
                                                   phone_number=phone_number,
                                                   ward=ward,
                                                   date_admission=date_admission,
                                                   image=image)
    u.save()
    return u
class ConfigTestCase(TestCase):

    def test_middleware_present(self):
        self.assertTrue('django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE)

    def test_session_app_present(self):
        self.assertTrue('django.contrib.sessions' in settings.INSTALLED_APPS)

    def test_app_present(self):
        self.assertTrue('rota' in settings.INSTALLED_APPS)


class ModelsTestCase(TestCase):
    def setUp(self):
        Request.objects.create(requested_by_staff="unknown", request_id="0",
                                      request_date="2001-01-01 00:01", )
        Request.objects.create(requested_by_staff="JaneDoe", request_id="1",
                                      request_date="2001-01-01 00:01")
        user1 = User.objects.create_user('jane',
                                         'doe' + '@nhs.com',
                                         'janepassword')
        user2 = User.objects.create_user('joe',
                                         'done@nhs.com',
                                         'joepassword')

        add_UserProfile(user1, registration_id="0", first_name="Jane",
                                          last_name="Doe", job_title="Charge Nurse",
                                          phone_number="00000000000", ward="A2",
                                          date_admission=datetime.now(), image="")
        add_UserProfile(user2, registration_id="1", first_name="Joe",
                                          last_name="Done", job_title="Healthcare Support Assistant",
                                          phone_number="00000000001", ward="A1",
                                          date_admission=datetime.now(), image="")

    def test_request_contents(self):
        self.assertEqual("JaneDoe", Request.objects.get(request_id="1").requested_by_staff)

    def test_userprofile_contents(self):
        self.assertNotEqual("Jane", UserProfile.objects.get(registration_id="1").first_name)
        self.assertEqual("Jane", UserProfile.objects.get(registration_id="0").first_name)
class ViewTests(TestCase):

    def test_index_view(self):
        response = self.client.get(reverse('rota:index'))
        content = response.content.decode()
        self.assertTrue(content)
