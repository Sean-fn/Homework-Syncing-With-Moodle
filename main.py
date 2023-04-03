from moodle_scraper.moodle import *
from google_calendar.g_calendar import *
from datetime import datetime
from datetime import date

def __main__():
    # moodle = Moodle(moodle_creds_file='moodle_scraper/moodle_creds_copy.json')
    # moodle_data = moodle.get_data()
    # moodle_data = moodle.data_process(moodle_data)
    with open('data.json', 'r') as f:
        moodle_data = json.load(f)

    creds = get_credentials()
    calendar_id = get_calendar_id(creds)
    gHW_names, gHW_descriptions, event_id = get_exsisting_HW(creds, calendar_id)

    for i in range(len(moodle_data['assessmentName'])):
        #checking if the HW has a due date
        hWname = moodle_data['assessmentName'][i]
        check_date_str = moodle_data['assessmentDueDate'][i]
        if check_date_str == '':
            print(hWname + ' has no due date/ skip this HW')
            continue

        #set reminder
        if hWname.startswith('✅'):reminder = False
        else:reminder = True

        #checking if the HW is already in the calendar
        if hWname not in gHW_names:
            create_HW(creds, calendar_id, moodle_data, i, reminder)
            continue

        #checking if the HW is past due
        today = date.today()
        check_date = datetime.strptime(check_date_str, '%Y-%m-%d').date()       #modual it
        if check_date >= today:
            #if the HW is past due
            #finding the index of the HW in the calendar
            for j in range(len(gHW_names)):
                if hWname == gHW_names[j]:
                    index = j
                    break
            print('index = ', index, type(index))

            #checking if the HW status is the same as the one in the calendar
            if moodle_data['assessmentDetail'][i] !=  gHW_descriptions[index]:
                print('executing update_HW')
                update_HW(creds, calendar_id, moodle_data, i, reminder, event_id[index])


if __name__ == '__main__':
    __main__()



            # def find_index(HW_name, n):
            #     if HW_name == gHW_names[n]:
            #         print(HW_name, gHW_names[n], n)
            #         return n
            #     else:
            #         print(n)
            #         find_index(HW_name, n+1)
            # index = find_index(moodle_data['assessmentName'][i], 0)