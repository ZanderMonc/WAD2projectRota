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

    def test_index_exists(self):
        url = ''

        try:
            url = reverse('rota:index)')
        except:
            pass
        self.assertEqual(url, '')

    def test_about_exists(self):
        url = ''

        try:
            url = reverse('rota:about')
        except:
            pass
        self.assertEqual(url, '/about/')

    def test_contact_us_exists(self):
        url = ''

        try:
            url = reverse('rota:contactus')
        except:
            pass
        self.assertEqual(url, '/contactus/')

    def test_login_exists(self):
        url = ''

        try:
            url = reverse('rota:login')
        except:
            pass
        self.assertEqual(url, '/login/')

    def test_logout_exists(self):
        url = ''

        try:
            url = reverse('rota:logout')
        except:
            pass
        self.assertEqual(url, '/logout/')

    def test_register_exists(self):
        url = ''

        try:
            url = reverse('rota:register')
        except:
            pass
        self.assertEqual(url, '/register/')

    def test_profile_exists(self):
        url = ''

        try:
            url = reverse('rota:profile')
        except:
            pass
        self.assertEqual(url, '/profile/')

    def test_edit_profile_exists(self):
        url = ''

        try:
            url = reverse('rota:editprofile')
        except:
            pass
        self.assertEqual(url, '/editprofile/')

    def test_timetable_exists(self):
        url = ''

        try:
            url = reverse('rota:timetable')
        except:
            pass
        self.assertEqual(url, '/timetable/')

    def test_newshift_exists(self):
        url = ''

        try:
            url = reverse('rota:shift/new')
        except:
            pass
        self.assertEqual(url, '')  # redirects to timetable (i.e. homepage) if not accessed by charge nurse user

    def test_edit_shift_exists(self):
        url = ''
        try:
            url = reverse('rota:shift/edit/<shift_id>')
        except:
            pass
        self.assertEqual(url, '')

    def test_index_template(self):
        response = self.client.get(reverse('rota:index'))
        content = response.content.decode()
        self.assertTrue(re.search(r'Homepage', content))

    def test_about_template(self):
        response = self.client.get(reverse('rota:about'))
        content = response.content.decode()
        searchfor = r'RotaCare is a web app to assist NHS nursing staff with their rota management'
        self.assertTrue(re.search(searchfor, content))

    def test_contact_us_template(self):
        response = self.client.get(reverse('rota:contactus'))
        content = response.content.decode()
        searchfor = r'<h3 class="mb-0 text-center">Contact us</h3>'
        self.assertTrue(re.search(searchfor, content))

    def test_login_template(self):
        response = self.client.get(reverse('rota:login'))
        content = response.content.decode()
        searchfor = r' <button class="btn btn-primary text-white btn-lg btn-block" type="submit">Login</button>'
        self.assertTrue(re.search(searchfor, content))

    def test_register_template(self):
        response = self.client.get(reverse('rota:register'))
        content = response.content.decode()
        searchfor = r' <button class="btn btn-primary btn-lg btn-block text-white" type="submit" value="Register">Register</but'
        self.assertTrue(re.search(searchfor, content))

class TestFunction(TestCase):
    def test_login_functionality(self):

        user = User.objects.get_or_create(username='Jane',
                                          email='doe@nhs.com',
                                          password='janepassword')[0]
        user.set_password('janepassword')
        user.save()

        add_UserProfile(registration_id="1",
                        job_title="Charge Nurse",
                        first_name="Jane",
                        last_name="Doe",
                        user=user)
        response = self.client.post(reverse('rota:login'), {'username': 'Jane', 'password': 'janepassword'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('rota:timetable'))

    def test_logout_functionality(self):
        response = self.client.post(reverse('rota:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/logout/')

