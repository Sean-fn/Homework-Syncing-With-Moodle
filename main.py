from moodle_scraper.moodle import *
from google_calendar.g_calendar import *
from utils import checkDate, setReminder, findIndex, sameDescription


def main():
    # moodle = Moodle(moodle_creds_file='moodle_scraper/moodle_creds_copy.json')
    # moodle_data = moodle.get_data()
    # moodle_data = moodle.data_process(moodle_data)
    with open('data.json', 'r') as f:
        moodle_data = json.load(f)

    creds = get_credentials()
    calendar_id = get_calendar_id(creds)
    gHW_names, gHW_descriptions, event_id = get_exsisting_HW(creds, calendar_id)

    for i in range(len(moodle_data['assessmentName'])):
        hWname = moodle_data['assessmentName'][i]
        reminder = setReminder(hWname)

        if hWname not in gHW_names:
            '''
            create new HW if it is not in the google calendar
            '''
            try:
                create_HW(creds, calendar_id, moodle_data, i, reminder)
            except:
                print(hWname + ' has no due date/ skip this HW')
            continue

        if  not checkDate(moodle_data, i):
            '''
            ignore the HW if it is past due
            '''
            continue
        index = findIndex(hWname, gHW_names)
        if sameDescription(moodle_data, gHW_descriptions, i, index):
            print('executing update_HW')
            update_HW(creds, calendar_id, moodle_data, i, reminder, event_id[index])


if __name__ == '__main__':
    main()