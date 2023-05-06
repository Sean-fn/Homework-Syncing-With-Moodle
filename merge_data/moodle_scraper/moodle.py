from merge_data.moodle_scraper.config import MoodleInit
from merge_data.moodle_scraper.scraper import MoodleScraper
from selenium.webdriver.common.by import By
import json
from tqdm import tqdm

class Moodle():
    def __init__(self, userId, pwd):
        self.moodle = MoodleInit(userId, pwd)                #login to moodle
        self.scraper = MoodleScraper(self.moodle.driver)     #scrape data from moodle

    def get_data(self):
        data = {
            'assessmentName': [],
            'assessmentDueDate': [],
            'assessmentDueTime': [],
            'assessmentDetail': [], 
            'assessmentUrl': []
            }

        self._get_data_recursive(data, 0)

        self.moodle.logout()
        return data

    def _get_data_recursive(self, data, course_index):
        if course_index >= 15:
            return

        # course_name = self.scraper.get_course_name(course_index)
        course_name = self.scraper.navigate_to_course(course_index)
        if course_name:
            assessments = self.moodle.driver.find_elements(By.CLASS_NAME, "activityinstance")
            assessment_links = []
            for assessment in assessments:
                assessment_links.append(assessment.find_element(By.TAG_NAME, "a"))

            self._get_assessment_data_recursive(data, course_name, assessment_links, 0)

            self.moodle.driver.back()           #for course page

        self._get_data_recursive(data, course_index + 1)

    def _get_assessment_data_recursive(self, data, course_name, assessment_links, assessment_index):
        if assessment_index >= len(assessment_links):
            return

        if self.scraper.navigate_to_assessment(assessment_index):
            assessmentName = self.scraper.get_assessment_name()
            assessmentName = course_name + ' | ' + assessmentName
            assessmentDeadline = self.scraper.get_assessment_deadline()
            assessmentName, assesmentDetail = self.scraper.get_assessment_detail(assessmentName)
            assesmentUrl = self.scraper.get_url()

            data['assessmentName'].append(assessmentName)
            data['assessmentDueDate'].append(assessmentDeadline)
            data['assessmentDueTime'].append('')
            data['assessmentDetail'].append(assesmentDetail)
            data['assessmentUrl'].append(assesmentUrl)

            self.moodle.driver.back()       #for assessment page

        self._get_assessment_data_recursive(data, course_name, assessment_links, assessment_index + 1)


    def data_process(self, data):
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
    
    def get_data_loop(self):
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
                continue

            '''
            go though all assessments in a course
            '''
            assessments = self.moodle.driver.find_elements(By.CLASS_NAME, "activityinstance")
            assessment_links = []
            for assessment in assessments:
                assessment_links.append(assessment.find_element(By.TAG_NAME, "a"))

            for assessment_idx in range(len(assessment_links)):
                if not self.scraper.navigate_to_assessment(assessment_idx):
                    continue
                #assessment page
                # print('已進入作業')
                assessmentName = self.scraper.get_assessment_name()
                assessmentName = course_name + ' | ' + assessmentName
                assessmentDeadline = self.scraper.get_assessment_deadline()
                assessmentName, assesmentDetail = self.scraper.get_assessment_detail(assessmentName)
                assesmentUrl = self.scraper.get_url()
                # print('assessmentName: ', assessmentName)
                # print('assessmentDeadline: ', assessmentDeadline)
                # print('assesmentDetail: ', assesmentDetail)
                # print('assesmentUrl: ', assesmentUrl)
                
                '''
                store data
                '''
                data['assessmentName'].append(assessmentName)
                data['assessmentDueDate'].append(assessmentDeadline)
                data['assessmentDueTime'].append('')
                data['assessmentDetail'].append(assesmentDetail)
                data['assessmentUrl'].append(assesmentUrl)
                self.moodle.driver.back()       #for assessment page
            self.moodle.driver.back()           #for course page
        self.moodle.logout()
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