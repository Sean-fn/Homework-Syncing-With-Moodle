from datetime import datetime, date

class Utils:
    def __init__(self):
        self.gIndex = 0

    def checkDate(self, moodle_data, idx):
        check_date_str = moodle_data['assessmentDueDate'][idx]
        today = date.today()
        check_date = datetime.strptime(check_date_str, '%Y-%m-%d').date()
        if check_date >= today:return True
        else:return False

    def setReminder(self, hWname):
        if hWname.startswith('✅'):return False
        else:return True

    def findIndex(self, hW_name, gHW_names):
        for j in range(len(gHW_names)):
            if hW_name == gHW_names[j]:
                self.gIndex = j
                print('index = ', self.gIndex, type(self.gIndex))
                break
        return self.gIndex

    def sameDescription(self, moodle_data, gHW_descriptions, i):
        if moodle_data['assessmentDetail'][i] !=  gHW_descriptions[self.gIndex]:
            return True
        else:
            return False