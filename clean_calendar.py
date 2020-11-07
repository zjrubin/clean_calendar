from __future__ import print_function
from datetime import datetime, timedelta
import pickle
import os.path
from googleapiclient.discovery import build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from typing import List, Dict

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # TODO: delete reminders
    creds = handle_authentication()

    service = build("calendar", "v3", credentials=creds)

    # now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time

    # Call the Calendar API
    events = get_old_events(service=service)

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event.get("summary"))
        service.events().delete(calendarId="primary", eventId=event["id"]).execute()

    if not events:
        print("No old events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event.get("summary"))


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


def get_old_events(service: Resource) -> List[Dict]:
    one_month_ago = get_time_n_days_ago(30).isoformat() + "Z"  # 'Z' indicates UTC time

    events = []
    request = service.events().list(
        calendarId="primary",
        timeMax=one_month_ago,
        singleEvents=True,
        orderBy="startTime",
    )

    while request is not None:
        events_result = request.execute()
        events.extend(events_result.get("items", []))
        request = service.events().list_next(request, events_result)

    return events


def get_time_n_days_ago(n: int) -> datetime:
    return datetime.now() - timedelta(days=n)


if __name__ == "__main__":
    main()
