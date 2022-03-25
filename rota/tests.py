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


class ConfigTestCase(TestCase):

    def test_middleware_present(self):
        self.assertTrue('django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE)

    def test_session_app_present(self):
        self.assertTrue('django.contrib.sessions' in settings.INSTALLED_APPS)

    def test_app_present(self):
        self.assertTrue('rota' in settings.INSTALLED_APPS)


class ModelsTestCase(TestCase):
    def setUp(self):
        Request.objects.create(requested_by_staff="unknown", request_id="0", request_type="unknown",
                               request_date="2001-01-01 00:01",
                               date_requesting="2022-09-09 00:05", swap_staff="Jane Doe")
        Request.objects.create(requested_by_staff="JaneDoe", request_id="1", request_type="unknown",
                               request_date="2001-01-01 00:01",
                               date_requesting="2022-09-09 00:05", swap_staff="Jane Doe")

        user1 = User.objects.create_user('jane',
                                         'doe' + '@nhs.com',
                                         'janepassword')
        user2 = User.objects.create_user('joe',
                                         'done@nhs.com',
                                         'joepassword')
        UserProfile.objects.create(user1, registration_id="0", first_name="Jane",
                                   last_name="Doe", job_title="Charge Nurse",
                                   phone_number="00000000000", ward="A2",
                                   date_admission=datetime.datetime.now(), image="")
        UserProfile.objects.create(user2, registration_id="1", first_name="Joe",
                                   last_name="Done", job_title="Healthcare Support Assistant",
                                   phone_number="00000000001", ward="A1",
                                   date_admission=datetime.datetime.now(), image="")

    def test_requests_are_correct(self):
        Req1 = Request.objects.get(requested_by_staff="unknown")
        Req2 = Request.objects.get(requested_by_staff="JaneDoe")
        self.assertEqual(Req1.request_id, 0)
        self.assertEqual(Req2.request_id, 1)

    def test_UserProfiles_are_correct(self):
        Usr1 = UserProfile.objects.get(registration_id="0")
        Usr2 = UserProfile.objects.get(registration_id="1")
        self.assertEqual(Usr1.job_title, "Charge Nurse")
        self.assertEqual(Usr2.job_title, "Healthcare Support Assistant")


class ViewTests(TestCase):

    def test_index_view(self):
        response = self.client.get(reverse('rota:index'))
        content = response.content.decode()
        self.assertTrue(content)

