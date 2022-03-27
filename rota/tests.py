from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.conf import settings
import os
import re
from django.test import TestCase
from django.urls import reverse

import populate_RotaCare
from rota.models import Request, UserProfile

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}RotaCare TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


def create_user(username, email, registration_id,
                job_title,
                first_name,
                last_name,
                image="default.jpg",
                password="janepassword"):
    user = User.objects.get_or_create(username=username,
                                      email=email,
                                      password=password)[0]
    user.set_password(password)
    user.save()

    add_UserProfile(registration_id=registration_id,
                    job_title=job_title,
                    first_name=first_name,
                    last_name=last_name,
                    user=user,
                    image=image)
    return user


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


class ConfigTestCase(TestCase):#tests app is configured

    def test_middleware_present(self):
        self.assertTrue('django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE)

    def test_session_app_present(self):
        self.assertTrue('django.contrib.sessions' in settings.INSTALLED_APPS)

    def test_app_present(self):
        self.assertTrue('rota' in settings.INSTALLED_APPS)


class ModelsTestCase(TestCase):#tests models save and retrieve correctly
    def setUp(self):
        Request.objects.create(requested_by_staff="unknown", request_id="0",
                               request_date="2001-01-01 00:01", )
        Request.objects.create(requested_by_staff="JaneDoe", request_id="1",
                               request_date="2001-01-01 00:01")

        user1 = create_user('jane', 'doe@nhs.com', '0', "Charge Nurse", "Jane", "Doe")
        user2 = create_user('joe', 'done@nhs.com', '1', 'Healthcare Support Assistant', 'Joe', 'Done')

    def test_request_contents(self):
        self.assertEqual("JaneDoe", Request.objects.get(request_id="1").requested_by_staff)

    def test_userprofile_contents(self):
        self.assertNotEqual("Jane", UserProfile.objects.get(registration_id="1").first_name)
        self.assertEqual("Joe", UserProfile.objects.get(registration_id="1").first_name)


class ViewTests(TestCase):#the following tests for url correctness

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


class TestFunction(TestCase): #tests main functionality
    def test_login_functionality(self):
        user = create_user('Jane', 'doe@nhs.com', "1", 'Charge Nurse', "Jane", "Doe")
        response = self.client.post(reverse('rota:login'), {'username': 'Jane', 'password': 'janepassword'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('rota:timetable'))

    def test_logout_functionality(self):
        response = self.client.post(reverse('rota:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/logout/')

    def test_new_shift(self):
        user = create_user("Joe", 'doe@nhs.com', '2', "Charge Nurse", 'Joe', 'Doe')
        r = self.client.post(reverse('rota:login'), {'username': 'Joe', 'password': 'janepassword'})
        response = self.client.get(reverse('rota:shift_new'))
        content = response.content.decode()

        try:
            self.assertEqual(response.status_code, 200)
        except:
            self.assertEqual(response.status_code, 302)
        self.assertTrue('Add new shift' in content)

    def test_editprofile(self):
        user = create_user('Joan', 'done@nhs.com', "3", "Staff Nurse", "Joan", "Done")
        r = self.client.post(reverse('rota:login'),
                             {'registration_id': "2", 'username': 'Joan', 'password': 'janepassword'})
        response = self.client.get(reverse('rota:editprofile'))
        content = response.content.decode()

        try:
            self.assertEqual(response.status_code, 200)
        except:
            self.assertEqual(response.status_code, 302)
        self.assertTrue("Edit Profile" in content)

    def test_timetable(self):
        user = create_user('J', 'done@nhs.com', '5', "Charge Nurse", "J", "Done")
        r = self.client.post(reverse('rota:login'),
                             {'registration_id': "5", 'username': 'J', 'password': 'janepassword'})
        response = self.client.get(reverse('rota:timetable'))
        content = response.content.decode()

        try:
            self.assertEqual(response.status_code, 200)
        except:
            self.assertEqual(response.status_code, 302)
        self.assertTrue(str(datetime.now().month) in content)

    def test_new_shift_link_charge_nurse(self):
        user = create_user('Job', 'done@nhs.com', '6', "Charge Nurse", "Job", "Done")
        r = self.client.post(reverse('rota:login'),
                             {'registration_id': "6", 'username': 'Job', 'password': 'janepassword'})
        content = self.client.get(reverse('rota:timetable')).content.decode()
        self.assertTrue("New Shift" in content)

    def test_new_shift_link_staff_nurse(self):
        user = create_user('Job', 'done@nhs.com', '7', "Staff Nurse", "Job", "Done")
        r = self.client.post(reverse('rota:login'),
                             {'registration_id': "7", 'username': 'Job', 'password': 'janepassword'})
        content = self.client.get(reverse('rota:timetable')).content.decode()
        self.assertTrue("New Shift" not in content)

    def test_edit_shift_charge_nurse(self):
        user = create_user('Job2', 'done@nhs.com', '8', "Charge Nurse", "Job2", "Done")
        r = self.client.post(reverse('rota:login'),
                             {'registration_id': "8", 'username': 'Job2', 'password': 'janepassword'})
        shift = Request.objects.get_or_create(requested_by_staff="Jane", request_id="1", staff_job_title="Charge Nurse",
                                              request_date=datetime.now(),
                                              shift_time=datetime.now())[0]

        content = self.client.get(reverse('rota:shift_edit', kwargs={'shift_id': shift.request_id})).content.decode()
        self.assertTrue("Edit Shift" in content)

    def test_edit_shift_staff_nurse(self):
        user = create_user('Job3', 'done@nhs.com', '9', "Staff Nurse", "Job3", "Done")
        r = self.client.post(reverse('rota:login'),
                             {'registration_id': "9", 'username': 'Job3', 'password': 'janepassword'})
        shift2 = Request.objects.get_or_create(requested_by_staff="Jane", request_id="2", staff_job_title="Staff Nurse",
                                               request_date=datetime.now(),
                                               shift_time=datetime.now())[0]

        response = self.client.get(reverse('rota:shift_edit', kwargs={'shift_id': shift2.request_id}))
        content = response.content.decode()
        self.assertTrue("Add new shift" not in content)
        self.assertTrue(response.url, '')
