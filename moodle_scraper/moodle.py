from moodle_scraper.config import *
from moodle_scraper.scraper import *

class Moodle():
    def __init__(self, moodle_creds_file):
        self.moodle = MoodleInit(moodle_creds_file)      #login to moodle
        self.scraper = MoodleScraper(self.moodle.driver)     #scrape data from moodle

    def get_data(self):
        data = {
            'assessmentName': [],
            'assessmentDueDate': [],
            'assessmentDueTime': [],
            'assessmentDetail': []
        }

        for courrse_index in range(15):
            course_name = self.scraper.get_course_name(courrse_index)
            if  not self.scraper.navigate_to_course(courrse_index):
                print('No course found')
                continue

            #course page
            assessment_links = self.moodle.driver.find_elements(By.CLASS_NAME, "instancename")
            for assessment_index in range(len(assessment_links)):
                if not self.scraper.navigate_to_assessment(assessment_index, assessment_type = [' 作業', ' 測驗卷']):
                    #data['assessmentName'].append(course_name + ' | ' + 'No assessment found')
                    print('No assessment found!!!!!!!!!')
                    continue

                #assessment page
                print('已進入作業')
                assessmentName = self.scraper.get_assessment_name()
                print('assessmentName: ', assessmentName)
                assessmentDeadline = self.scraper.get_assessment_deadline()
                print('assessmentDeadline: ', assessmentDeadline)
                assesmentDetail = self.scraper.get_assessment_detail()
                print('assesmentDetail: ', assesmentDetail)
                #storing data
                data['assessmentName'].append(course_name + ' | ' + assessmentName)
                data['assessmentDueDate'].append(assessmentDeadline)
                data['assessmentDueTime'].append('')
                data['assessmentDetail'].append(assesmentDetail)
                self.moodle.driver.back()
                print('上一頁')
            self.moodle.driver.back()
        self.moodle.logout()
        print(data)
        return data

    def data_process(self, data):
        #data['assessmentDeadline'] = [date.replace('年', '-').replace('月', '-').replace('日', '') for date in data['assessmentDeadline']]
        for i, date in enumerate(data['assessmentDueDate']):
            try:
                data['assessmentDueDate'][i] = self.scraper.split_date(date)
                data['assessmentDueTime'][i] = self.scraper.split_time(date)
            except:
                print('cannot split date and time: row data = ', date)
                data['assessmentDueDate'][i] = None
                data['assessmentDueTime'][i] = None

        return data



def __main__():
    moodle = Moodle(moodle_creds_file='moodle_scraper/moodle_creds.json')
    data = moodle.get_data()
    data = moodle.data_process(data)
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    pass
    #__main__()