from moodle_scraper import MoodleInit
from moodle_scraper.scraper import MoodleScraper
from selenium.webdriver.common.by import By
import json
from tqdm import tqdm

class Moodle():
    def __init__(self, userId, pwd):
        self.moodle = MoodleInit(userId, pwd)      #login to moodle
        self.scraper = MoodleScraper(self.moodle.driver)     #scrape data from moodle

    def get_data(self):
        data = {
            'assessmentName': [],
            'assessmentDueDate': [],
            'assessmentDueTime': [],
            'assessmentDetail': [], 
            'assessmentUrl': []
            }

        '''go though 15 courses'''
        for courrse_index in tqdm(range(15)):
            '''
            go though all courses
            '''
            course_name = self.scraper.get_course_name(courrse_index)
            if  not self.scraper.navigate_to_course(courrse_index):
                # print('No course found')
                continue
            course_url = self.scraper.get_url()

            '''
            go though all assessments in a course
            '''
            aa = self.moodle.driver.find_elements(By.CLASS_NAME, "activityinstance")
            assessment_links = []
            for a in aa:
                assessment_links.append(a.find_element(By.TAG_NAME, "a"))

            for assessment_index in range(len(assessment_links)):
                if not self.scraper.navigate_to_assessment(assessment_index):
                    continue
                #assessment page
                # print('已進入作業')
                assessmentName = self.scraper.get_assessment_name()
                # print('assessmentName: ', assessmentName)
                if assessmentName in ['公佈欄', '']:
                    if course_url != self.scraper.get_url():
                        self.moodle.driver.back()
                    # print('assessmentName is empty and QUIT')
                    continue
                assessmentName = course_name + ' | ' + assessmentName
                assessmentDeadline = self.scraper.get_assessment_deadline()
                # print('assessmentDeadline: ', assessmentDeadline)
                assessmentName, assesmentDetail = self.scraper.get_assessment_detail(assessmentName)
                # print('assesmentDetail: ', assesmentDetail)
                assesmentUrl = self.scraper.get_url()
                # print('assesmentUrl: ', assesmentUrl)
                
                '''
                save data
                '''
                data['assessmentName'].append(assessmentName)
                data['assessmentDueDate'].append(assessmentDeadline)
                data['assessmentDueTime'].append('')
                data['assessmentDetail'].append(assesmentDetail)
                data['assessmentUrl'].append(assesmentUrl)
                self.moodle.driver.back()
                # print('上一頁')

            self.moodle.driver.back()

        self.moodle.logout()
        return data


    def data_process(self, data):
        #data['assessmentDeadline'] = [date.replace('年', '-').replace('月', '-').replace('日', '') for date in data['assessmentDeadline']]
        for i, date in enumerate(data['assessmentDueDate']):
            try:
                data['assessmentDueDate'][i] = self.scraper.split_date(date)
                # print('date splited: ', data['assessmentDueDate'][i])
            except:
                # print('cannot split date and time: row data = ', date)
                data['assessmentDueDate'][i] = ''
                data['assessmentDueTime'][i] = ''
            else:
                data['assessmentDueTime'][i] = self.scraper.split_time(date)
                # print('time splited: ', data['assessmentDueTime'][i])
        return data


def __main__():
    moodle = Moodle(moodle_creds_file='moodle_scraper/creds/moodle_creds.json')
    # data = moodle.get_data()
    with open('dataSean.json', 'r') as f:
        data = json.load(f)
    data = moodle.data_process(data)
    with open('dataSean.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    __main__()