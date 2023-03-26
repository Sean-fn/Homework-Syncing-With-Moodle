from moodle_scraper.moodle import *
from google_calendar.g_calendar import *
from datetime import datetime
from datetime import date

def __main__():
    moodle = Moodle(moodle_creds_file='moodle_scraper/moodle_creds.json')
    moodle_data = moodle.get_data()
    moodle_data = moodle.data_process(moodle_data)

    creds = get_credentials()
    calendar_id = get_calendar_id(creds)
    exsisting = get_exsisting_HW(creds, calendar_id)

    today = date.today()
    for i in range(len(moodle_data['assessmentName'])):
        #checking if the HW is due today or later
        check_date_str = moodle_data['assessmentDueDate'][i]
        if check_date_str == None:
            print(moodle_data['assessmentName'][i] + ' has no due date')
            continue
        check_date = datetime.strptime(check_date_str, '%Y-%m-%d').date()       #make it function
        if check_date >= today:
            #checking if the HW is already in the calendar
            if moodle_data['assessmentName'][i] not in exsisting:
                create_HW(creds, moodle_data['assessmentName'][i], moodle_data['assessmentDueDate'][i], moodle_data['assessmentUrl'][i], calendar_id, moodle_data['assessmentDetail'][i])


if __name__ == '__main__':
    __main__()