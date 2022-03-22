from django.test import TestCase

# Create your tests here.
from django.conf import settings
import os
import re
from django.test import TestCase
from rota.models import Request

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class RequestTestCase(TestCase):
    def setUp(self):
        Request.objects.create(requested_by_staff="unknown", request_id="0", request_type="unknown",
                               request_date="2001-01-01 00:01",
                               date_requesting="2022-09-09 00:05", swap_staff="Jane Doe")
        Request.objects.create(requested_by_staff="JaneDoe", request_id="1", request_type="unknown",
                               request_date="2001-01-01 00:01",
                               date_requesting="2022-09-09 00:05", swap_staff="Jane Doe")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        Req1 = Request.objects.get(requested_by_staff="unknown")
        Req2 = Request.objects.get(requested_by_staff="JaneDoe")
        self.assertEqual(Req1.request_id, 0)
        self.assertEqual(Req2.request_id, 1)
