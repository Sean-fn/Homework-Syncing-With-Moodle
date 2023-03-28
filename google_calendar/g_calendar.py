from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials(token_file='google_calendar/g_calendar_token.json'):
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google_calendar/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    return creds


def create_HW(creds, title, date, url, calendar_id, description=''):
    try:
        service = build('calendar', 'v3', credentials=creds)
        event = {
        'summary': title,
        'description': description,
        'location': url, 
        'start': {
            'date': date,
            'timeZone': 'UTC+8',
        },
        'end': {
            'date': date,
            'timeZone': 'UTC+8',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'popup', 'minutes': 24 * 60 * 2 + 120},
            ],
        },  
        }

        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print('An error occurred: %s' % error)


def update_HW(creds, calendar_id, event_id='', description=''):
    try:
        service = build('calendar', 'v3', credentials=creds)
        event = {
        'description': description,
        }

        event = service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
        print('Event updated: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print('An error occurred: %s' % error)


def create_summary(creds):
    service = build('calendar', 'v3', credentials=creds)
    calendar = {
    'summary': 'HW',
    'timeZone': 'UTC+8', 
    
}
    created_calendar = service.calendars().insert(body=calendar).execute()
    print ('the created calendar ID is = ', created_calendar['id'])


def get_calendar_id(creds):
    service = build('calendar', 'v3', credentials=creds)
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for i, calendar_list_entry in enumerate(calendar_list['items']):
            print ('calendar_list_entry = ', calendar_list_entry['summary'])
            if calendar_list_entry['summary'] == 'HW':
                return calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            create_summary(creds)


def get_event_id(creds, calendar_id):
    service = build('calendar', 'v3', credentials=creds)
    events_result = service.events().list(calendarId=calendar_id, maxResults=2500, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    for event in events:
        print(event['id'])
        print(event['description'])


def split_descriptions(descriptions):
    for i in range(len(descriptions)):
        descriptions[i] = descriptions[i].split('\n', 1)[0]


def get_exsisting_HW(creds, calendar_id):
    try:
        service = build('calendar', 'v3', credentials=creds)

        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 100 events')
        events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                              maxResults=100, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return '', '', ''
        summary = []
        descriptions = []
        event_id = []
        for event in events:
            #print(event['summary'])
            summary.append(event['summary'])
            descriptions.append(event['description'])
            event_id.append(event['id'])
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'], '\n', event['description'])
        return summary, descriptions, event_id

    except HttpError as error:
        print('An error occurred: %s' % error)




creds = get_credentials()
calendar_id = get_calendar_id(creds)
# create_HW(creds, '國文小考測驗', '2023-04-01', calendar_id, 'Test')
items = get_exsisting_HW(creds, calendar_id)                        #can't use one line for loop