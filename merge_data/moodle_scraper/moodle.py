from merge_data.moodle_scraper.config import MoodleInit
from merge_data.moodle_scraper.scraper import MoodleScraper
from selenium.webdriver.common.by import By
import json
from tqdm import tqdm

class Moodle():
    '''loop through all courses and assessments in moodle and get data
    '''
    def __init__(self, userId, pwd):
        self.moodle = MoodleInit(userId, pwd)                #login to moodle
        self.scraper = MoodleScraper(self.moodle.driver)     #scrape data from moodle

    def get_data(self) -> dict:
        '''Get all data from moodle recursively

        Returns:
            dict: dictionary of all data
        '''
        data = {
            'assessmentName': [],
            'assessmentDueDate': [],
            'assessmentDueTime': [],
            'assessmentDetail': [], 
            'assessmentUrl': []
            }

        self._get_data_recursive(data, 0)

        self.moodle.logout()
        print('Logout from moodle')
        return data


    def _get_data_recursive(self, data:dict, 
                            course_index:int)->None:
        '''Get into the assessment page according to course_index recursively

        Args:   
            data (dict): all data
            course_index (int): the index of the course in the homepage

        Returns:
            None
        '''

        if course_index >= 15:
            return

        course_name = self.scraper.navigate_to_course(course_index)
        print('Get into course_name: {} Course_index: {}'.format(course_name, course_index))
        if course_name:
            assessments = self.moodle.driver.find_elements(By.CLASS_NAME, "activityinstance")
            assessment_links = []
            for assessment in assessments:
                assessment_links.append(assessment.find_element(By.TAG_NAME, "a"))

            self._get_assessment_data_recursive(data, course_name, assessment_links, 0)

            self.moodle.driver.back()           #for course page
            print('Back to dashboard page. Current index = ', course_index)
        self._get_data_recursive(data, course_index + 1)


    def _get_assessment_data_recursive(self, data:dict, 
                                       course_name:str, 
                                       assessment_links:list, 
                                       assessment_index:int)->None:
        '''Get assessment data according to assessment_index recursively

        Args:
            data (dict): all data
            course_name (str): the name of the course
            assessment_links (list): the list of the assessment links
            assessment_index (int): the index of the assessment in the course page

        Returns:
            None
        '''
        if assessment_index >= len(assessment_links):
            return

        if self.scraper.navigate_to_assessment(assessment_index):
            print('Get into detail page. Assessment index = ', assessment_index)
            assessmentName = self.scraper.get_assessment_name()
            assessmentName = course_name + ' | ' + assessmentName
            print('assessmentName: ', assessmentName)
            assessmentDeadline = self.scraper.get_assessment_deadline()
            print('assessmentDeadline: ', assessmentDeadline)
            assessmentName, assesmentDetail = self.scraper.get_assessment_detail(assessmentName)
            print('assessmentDetail: ', assesmentDetail)
            assesmentUrl = self.scraper.get_url()
            print('assesmentUrl: ', assesmentUrl)

            data['assessmentName'].append(assessmentName)
            data['assessmentDueDate'].append(assessmentDeadline)
            data['assessmentDueTime'].append('')
            data['assessmentDetail'].append(assesmentDetail)
            data['assessmentUrl'].append(assesmentUrl)
            print('---Data appended into the dictionary---')

            self.moodle.driver.back()       #for assessment page
            print('Back to assessment list page.  Aourse index{}  Assessment index = {}'
                  .format(course_name, assessment_index))

        self._get_assessment_data_recursive(data, course_name, assessment_links, assessment_index + 1)


    def data_process(self, data:dict) -> dict:
        '''Split the date and time
        if cannot split, set the value to an empty string

        Args:
            data (dict): all data

        Returns:
            dict: all data with date and time splited
        '''
        for i, date in enumerate(data['assessmentDueDate']):
            try:
                data['assessmentDueDate'][i] = self.scraper.split_date(date)
                print('date splited: ', data['assessmentDueDate'][i])
            except:
                print('cannot split date and time: row data = ', date)
                data['assessmentDueDate'][i] = ''
                data['assessmentDueTime'][i] = ''
            else:
                data['assessmentDueTime'][i] = self.scraper.split_time(date)
                print('time splited: ', data['assessmentDueTime'][i])
        return data
    
    #def get_data_loop(self):
        '''Using for loop to get data from moodle

        Returns:
            dict: all data
        '''
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
                print('已進入作業')
                assessmentName = self.scraper.get_assessment_name()
                assessmentName = course_name + ' | ' + assessmentName
                assessmentDeadline = self.scraper.get_assessment_deadline()
                assessmentName, assesmentDetail = self.scraper.get_assessment_detail(assessmentName)
                assesmentUrl = self.scraper.get_url()
                print('assessmentName: ', assessmentName)
                print('assessmentDeadline: ', assessmentDeadline)
                print('assesmentDetail: ', assesmentDetail)
                print('assesmentUrl: ', assesmentUrl)
                
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
    '''For testing
    '''
    moodle = Moodle(moodle_creds_file='moodle_scraper/creds/moodle_creds.json')
    # data = moodle.get_data()
    with open('data.json', 'r') as f:
        data = json.load(f)
    data = moodle.data_process(data)
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    __main__()