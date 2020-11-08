from __future__ import print_function
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from typing import List, Dict
import os.path
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = handle_authentication()

    service = build("calendar", "v3", credentials=creds)

    calendars = get_calendars(service)

    for calendar in calendars:
        events = get_old_events(service=service, calendar_id=calendar["id"])

        delete_events(service=service, calendar=calendar, events=events)


def handle_authentication() -> Credentials:
    creds: Credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds


def get_calendars(service: Resource) -> List[Dict]:
    calendars = []
    request = service.calendarList().list(minAccessRole="writer", showHidden=True)

    while request is not None:
        calendars_result = request.execute()
        calendars.extend(calendars_result.get("items", []))
        request = service.calendarList().list_next(request, calendars_result)

    return calendars


def get_old_events(service: Resource, calendar_id: str) -> List[Dict]:
    one_month_ago = get_time_n_days_ago(30).isoformat() + "Z"  # 'Z' indicates UTC time

    events = []
    request = service.events().list(
        calendarId=calendar_id,
        timeMax=one_month_ago,
        singleEvents=True,
        orderBy="startTime",
    )

    while request is not None:
        events_result = request.execute()
        events.extend(events_result.get("items", []))
        request = service.events().list_next(request, events_result)

    return events


def delete_events(service: Resource, calendar: List[Dict], events: List[Dict]) -> None:
    print(f"Deleting events in calendar: {calendar['summary']}")
    for event in events:
        service.events().delete(
            calendarId=calendar["id"], eventId=event["id"]
        ).execute()

        start = event["start"].get("dateTime", event["start"].get("date"))
        print(f"Deleted: ({start}) - {event.get('summary')}")
    print(f"Finished deleting events in calendar: {calendar['summary']}\n")


def get_time_n_days_ago(n: int) -> datetime:
    # now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    return datetime.now() - timedelta(days=n)


if __name__ == "__main__":
    main()
