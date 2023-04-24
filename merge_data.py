from moodle_scraper.moodle import Moodle
from google_calendar.g_calendar import GCalendar #create_HW, update_HW, get_exsisting_HW, get_credentials, get_calendar_id
from utils import Utils #checkDate, setReminder, findIndex, sameDescription

class MergeData:
    def __init__(self, google_token_file, userId, pwd):
        self.gCalendar = GCalendar(google_token_file)
        self.moodle = Moodle(userId, pwd)
        self.utils = Utils()
        self.calendar_id = ''
        self.creds = None
        self.moodle_data = None
        self.event_id = []
        self.gHW_names = []
        self.gHW_descriptions = []

    def getGoogleInfo(self):
        '''
        get google calendar id
        '''
        self.gCalendar.get_credentials()
        self.calendar_id, self.newEventList = self.gCalendar.get_calendar_id()


    def packData(self):
        '''
        get data from moodle
        '''
        # with open('data.json', 'r') as f:
        #     moodle_data = json.load(f)
        #     self.moodle_data = moodle_data
        moodle_data = self.moodle.get_data()
        moodle_data = self.moodle.data_process(moodle_data)
        self.moodle_data = moodle_data

        '''
        get data from google calendar
        '''
        self.gHW_names, self.gHW_descriptions, self.event_id = self.gCalendar.get_exsisting_HW(self.calendar_id)
        self.checkGHWname = [name.replace('✅', '') for name in self.gHW_names]

    def processingHW(self):
        for i in range(len(self.moodle_data['assessmentName'])):
            if self.moodle_data['assessmentDueDate'][i] == '':
                print(self.moodle_data['assessmentDueDate'][i], 'has no due date')
                continue
            hWname = self.moodle_data['assessmentName'][i]
            checkHWname = self.moodle_data['assessmentName'][i].replace('✅', '')

            reminder = self.utils.setReminder(hWname)

            if checkHWname not in self.checkGHWname:
                try:
                    self.gCalendar.synkHW(self.calendar_id, self.moodle_data, i, reminder)
                except Exception as e:
                    print(hWname + ' has an error : ', e)
                finally:
                    continue

            # if not self.newEventList and not self.utils.checkDate(self.moodle_data, i):
            #     continue
            index = self.utils.findIndex(checkHWname, self.checkGHWname)
            #TODO: check if the due date is different
            if self.utils.sameDescription(self.moodle_data, self.gHW_descriptions, i):
                print('executing update_HW')
                try:
                    self.gCalendar.synkHW(self.calendar_id, self.moodle_data, i, reminder, self.event_id[index])
                except Exception as e:
                    print(hWname + ' has an error : ', e)