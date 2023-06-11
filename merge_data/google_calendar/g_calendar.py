from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dotenv import load_dotenv
import os
import json

load_dotenv()

class GCalendar:
    def __init__(self, google_token):
        # If modifying these scopes, delete the file token.json.
        self.SCOPES = ['https://www.googleapis.com/auth/calendar'] 

        '''toss dic with refresh_token, client_id, client_secret'''
        self.token_str = google_token
        #TODO: remove this in init
        self.creds = self.get_credentials()
        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_json_credentials(self) -> str:
        '''convert credentials to string
        '''
        return json.loads(self.creds.to_json())

    def get_credentials(self):
        creds = None
        if self.token_str:
            creds = Credentials.from_authorized_user_info(info=self.token_str)
        if not creds or not creds.valid:
            if creds:
                creds.refresh(Request())
                print('refreshed')
            else:
                config = json.loads(os.environ['GOOGLE_CREDENTIALS'])
                flow = InstalledAppFlow.from_client_config(
                    config, self.SCOPES)
                creds = flow.run_local_server(port=0)
                print(creds.to_json())
                print('issued')
        print('returning creds')
        return creds

    def get_credentials_to_file(self):
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'google_calendar/creds/credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)

            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        return creds

    #TODO
    def synkHW(self, calendar_id, moodle_data, index, reminder, event_id=None):
        try:
            print('synkHW get into try')
            event = {
            'summary': moodle_data['assessmentName'][index],
            'description': moodle_data['assessmentDetail'][index],
            'location': moodle_data['assessmentUrl'][index], 
            'start': {
                'date': moodle_data['assessmentDueDate'][index],
                # 'dateTime': moodle_data['assessmentDueTime'][index],
                'timeZone': 'UTC+8',
            },
            'end': {
                'date': moodle_data['assessmentDueDate'][index],
                # 'dateTime': moodle_data['assessmentDueTime'][index],
                'timeZone': 'UTC+8',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'popup', 'minutes': 24 * 60 * 2 + 120},
                ],
            },  
            }
            if not reminder:
                event.pop('reminders')

            if not event_id:
                '''
                if event id in empty, create an event
                '''
                event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
                print('Event created: %s' % (event.get('htmlLink')))
            else:
                '''
                if event id, update an event
                '''
                event = self.service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
                print('Event updated: %s' % (event.get('htmlLink')))

        except HttpError as error:
            print('An error occurred: %s' % error)
            

    def create_HW(self, calendar_id, moodle_data, index, reminder=True):
        try:
            event = {
            'summary': moodle_data['assessmentName'][index],
            'description': moodle_data['assessmentDetail'][index],
            'location': moodle_data['assessmentUrl'][index], 
            'start': {
                'date': moodle_data['assessmentDueDate'][index],
                # 'dateTime': moodle_data['assessmentDueTime'][index],
                'timeZone': 'UTC+8',
            },
            'end': {
                'date': moodle_data['assessmentDueDate'][index],
                # 'dateTime': moodle_data['assessmentDueTime'][index],
                'timeZone': 'UTC+8',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'popup', 'minutes': 24 * 60 * 2 + 120},
                ],
            },  
            }
            if not reminder:
                event.pop('reminders')

            event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))

        except HttpError as error:
            print('An error occurred: %s' % error)


    def update_HW(self, calendar_id, moodle_data, index, reminder, event_id=''):
        try:
            event = {
            'summary': moodle_data['assessmentName'][index],
            'description': moodle_data['assessmentDetail'][index],
            'location': moodle_data['assessmentUrl'][index], 
            'start': {
                'date': moodle_data['assessmentDueDate'][index],
                # 'dateTime': moodle_data['assessmentDueTime'][index],
                'timeZone': 'UTC+8',
            },
            'end': {
                'date': moodle_data['assessmentDueDate'][index],
                # 'dateTime': moodle_data['assessmentDueTime'][index],
                'timeZone': 'UTC+8',
            },
            }
            if reminder:
                event['reminders'] = {
                'useDefault': False,
                'overrides': [
                {'method': 'popup', 'minutes': 24 * 60 * 2 + 120},
                ],
            }

            event = self.service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
            print('Event updated: %s' % (event.get('htmlLink')))

        except HttpError as error:
            print('An error occurred: %s' % error)


    def create_summary(self):
        calendar = {
        'summary': 'HW',
        'timeZone': 'UTC+8', 
        'colorId': 'Mango', 
        "description": 'This is a calendar synking all the homeworks on Moodle.\n it will be updated every 6 hours.' 
    }
        created_calendar = self.service.calendars().insert(body=calendar).execute()
        print ('the created calendar ID is = ', created_calendar['id'])
        return created_calendar['id'], True


    def get_calendar_id(self):
        page_token = None
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for i, calendar_list_entry in enumerate(calendar_list['items']):
                print ('calendar_list_entry = ', calendar_list_entry['summary'])
                if calendar_list_entry['summary'] == 'HW':
                    return calendar_list_entry['id'], False
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                calendarId, newEventList = self.create_summary()
                return calendarId, newEventList


    def get_exsisting_HW(self, calendar_id):
        try:
            '''
            TODO: the timeMin should be the start of the semester
            '''
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            curr_semester = datetime.datetime(2022, 2, 14).isoformat() + 'Z'
            print('Getting the upcoming 1000 events')
            events_result = self.service.events().list(calendarId=calendar_id, timeMin=curr_semester,
                                                maxResults=1000, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return '', '', ''
            
            '''
            store data
            '''
            summary = []
            descriptions = []
            event_id = []

            print('There are %d events in total' % len(events))
            for i, event in enumerate(events):
                print('event no.%d' % i)
                summary.append(event['summary'])
                print('summary = ', event['summary'])
                event_id.append(event['id'])
                print('event_id = ', event['id'])

                #ISSUE: the description is not always there
                if event['description'] == None:
                    descriptions.append('No description')
                else:
                    descriptions.append(event['description'])
                print('description = ', event['description'])
                
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'], '\n', event['description'])
            return summary, descriptions, event_id



        except HttpError as error:
            print('An error occurred: %s' % error)