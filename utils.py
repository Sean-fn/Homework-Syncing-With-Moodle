from datetime import datetime, date

def checkDate(moodle_data, idx):
    check_date_str = moodle_data['assessmentDueDate'][idx]
    today = date.today()
    check_date = datetime.strptime(check_date_str, '%Y-%m-%d').date()
    if check_date >= today:return True
    else:return False

def setReminder(hWname):
    if hWname.startswith('✅'):return False
    else:return True

def findIndex(hW_name, gHW_names):
    for i in range(len(gHW_names)):
        if hW_name == gHW_names[i]:
            index = i
            print('index = ', index, type(index))
            break
    return index

def sameDescription(moodle_data, gHW_descriptions, i, index):
    if moodle_data['assessmentDetail'][i] !=  gHW_descriptions[index]:
        return True
    else:
        return False