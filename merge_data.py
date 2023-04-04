from moodle_scraper.moodle import Moodle
from google_calendar.g_calendar import GCalendar #create_HW, update_HW, get_exsisting_HW, get_credentials, get_calendar_id
from utils import Utils #checkDate, setReminder, findIndex, sameDescription
import json

class MergeData:
    def __init__(self):
        self.creds = None
        self.calendar_id = ''
        self.gHW_names = []
        self.gHW_descriptions = []
        self.event_id = []
        self.moodle_data = None
        # self.moodle = Moodle(moodle_creds_file='moodle_scraper/moodle_creds.json')
        self.gCalendar = GCalendar()
        self.utils = Utils()

    def getGoogleInfo(self):
        self.gCalendar.get_credentials()
        self.calendar_id = self.gCalendar.get_calendar_id()


    def packData(self):
        # moodle_data = self.moodle.get_data()
        # moodle_data = self.moodle.data_process(moodle_data)
        # self.moodle_data = moodle_data
        with open('data.json', 'r') as f:
            moodle_data = json.load(f)
            self.moodle_data = moodle_data

        self.gHW_names, self.gHW_descriptions, self.event_id = self.gCalendar.get_exsisting_HW(self.calendar_id)


    def processingHW(self):
        for i in range(len(self.moodle_data['assessmentName'])):
            hWname = self.moodle_data['assessmentName'][i]
            reminder = self.utils.setReminder(hWname)

            if hWname not in self.gHW_names:
                try:
                    self.gCalendar.create_HW(self.creds, self.calendar_id, self.moodle_data, i, reminder)
                except:
                    print(hWname + ' has no due date/ skip this HW')
                continue

            if  not self.utils.checkDate(self.moodle_data, i):
                continue
            index = self.utils.findIndex(hWname, self.gHW_names)
            if self.utils.sameDescription(self.moodle_data, self.gHW_descriptions, i):
                print('executing update_HW')
                self.gCalendar.update_HW(self.creds, self.calendar_id, self.moodle_data, i, reminder, self.event_id[index])