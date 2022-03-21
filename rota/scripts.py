from datetime import datetime, timedelta

import pytz

from google.oauth2 import service_account

from googleapiclient.discovery import build
from models import Request

service_account_email = "rotacaretester@rotacare.iam.gserviceaccount.com"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

credentials = service_account.Credentials.from_service_account_file("{% static 'rotacare-caa0fcb3d409.json' %} ")
scoped_credentials = credentials.with_scopes(SCOPES)


def build_service():
    service = build("calendar", "v3", credentials=scoped_credentials)
    return service


def create_event():
    service = build_service()

    start_datetime = datetime.now(tz=pytz.utc)

    event = (
        service.events().insert(
            calendarId="primary",
            body={
                "summary": "Foo 2",
                "description": "Bar",
                "start": {"dateTime": start_datetime.isoformat()},
                "end": {
                    "dateTime": (start_datetime + timedelta(minutes=15)).isoformat()
                },
            },
        ).execute()
    )

    print(event)


def export_events():
    service = build_service()
    shifts = Request.objects.getall()
    start_datetime = datetime.now(tz=pytz.utc)
    for shift in shifts:
        event = (
            service.events().insert(
                calendarId="primary",
                body={
                    "summary": shift.requested_by_staff,
                    "description": shift.request_type,
                    "start": {"dateTime": shift.request_date},
                    "end": {
                        "dateTime": (shift.request_date + timedelta(minutes=15)).isoformat()
                    },
                },
            ).execute()
        )
        print(event)


# def list_events():


export_events()
