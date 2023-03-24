from moodle_scraper.moodle import *
from google_calendar.g_calendar import *

def __main__():
    moodle = Moodle(moodle_creds_file='moodle_scraper/moodle_creds.json')
    moodle_data = moodle.get_data()
    moodle_data = moodle.data_process(moodle_data)

    creds = get_credentials()
    calendar_id = get_calendar_id(creds)
    for i in range(len(moodle_data['assessmentName'])):
        create_HW(creds, moodle_data['assessmentName'][i], moodle_data['assessmentDueDate'][i], calendar_id, moodle_data['assessmentDetail'][i])

    items = get_exsisting_HW(creds, calendar_id)
    print(items)

if __name__ == '__main__':
    __main__()