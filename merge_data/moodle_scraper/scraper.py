from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class MoodleScraper():
    '''The components of scraper for moodle
    '''
    def __init__(self, driver):
        self.driver = driver
    
    #TODO: auto switch semesters
    def navigate_to_course(self, index)-> str:
        '''Get into the course page if the title contains '111(下)'

        Args:
            index (int): the index of the course in the homepage

        Returns:
            string: the title of the course
        '''
        course_titles = self.driver.find_elements(By.TAG_NAME, 'h3')        #course title in the dashboard
        if course_titles[index].text[:6] == '111(下)':
            course_name = course_titles[index].text.split('[')[0][6:]
            if course_titles[index].text.startswith('111(下)') and course_titles[index].text.split('[')[0][6:] == course_name:
                courses_button = self.driver.find_elements(By.CLASS_NAME, 'coursequicklink')
                courses_button[index].click()
                try:
                    assert '課程' in self.driver.title
                except AssertionError:
                    print('AssertionError : 課程', AssertionError)
                return course_name


    def navigate_to_assessment(self, index)-> bool:
        '''Get into the assessment page according to the index

        Args:
            index (int): The number of the assessments in the coures page

        Returns:
            bool: If the assessment is a quiz or assignment, return True. Otherwise, return False.
        '''
        aa = self.driver.find_elements(By.CLASS_NAME, "activityinstance")
        link_elements = []
        for a in aa:
            link_elements.append(a.find_element(By.TAG_NAME, "a"))

        url = link_elements[index].get_attribute("href")
        if 'assign' in url or 'quiz' in url:
            link_elements[index].click()
            return True
        return False


    def get_url(self)-> str:
        '''Get the url of the current page

        Returns:
            string: If the url is valid, return the url. Otherwise, return an empty string.
        '''
        try:
            return self.driver.current_url
        except:
            return ''

    def get_assessment_name(self)-> str:
        '''Get the name of the assessment

        Returns:
            string: If the assessment name is valid, return the name. Otherwise, return an empty string.
        '''
        try:
            assessment_name = self.driver.find_element(By.TAG_NAME, 'h2').text
            return assessment_name
        except NoSuchElementException:
            print('NoSuchElementException: Assessment name not found')
            return ''


    def get_assessment_deadline(self)-> str:
        '''Get the deadline of the assessment: Go though all the possible locators, 
        and return the first valid deadline.
        
        Returns:
            string: If the deadline is valid, return the deadline. Otherwise, return an empty string.
        '''
        locators = {
        'first': [By.XPATH, '//*[@id="region-main"]/div/div[2]/div[1]/table/tbody/tr[4]/td[2]'],
        'sec': [By.XPATH, '//*[@id="region-main"]/div/div[2]/div[2]/table/tbody/tr[4]/td[2]'],
        'third': [By.XPATH, '//*[@id="yui_3_15_0_3_1679661660567_303"]'],
        'testSheet': [By.XPATH, '//*[@id="yui_3_15_0_3_1681126092687_303"]'],
        'testSheet1': [By.XPATH, '//*[@id="region-main"]/div/div[1]/p[2]'],
        'testSheet2': [By.XPATH, '//*[@id="yui_3_15_0_3_1679715868097_305"]/div[1]/p[3]'],
        }

        for locator in locators.values():
            try:
                assessment_deadline = self.driver.find_element(*locator).get_attribute('innerHTML')
                '''
                make sure getting the right deadline
                '''
                if '年' not in assessment_deadline and '月' not in assessment_deadline and '日' not in assessment_deadline :
                    continue
                return assessment_deadline
            except NoSuchElementException:
                print('NoSuchElementException: Assessment deadline not found')
                continue
        return ''
            

    #TODO: using button to determine the status of a test sheet
    def get_assessment_detail(self, assessmentName: str) -> str:
        '''Get the detail of the assessment: Go though all the possible locators,
        and store the first valid status into detailList.
        Adding the assessment detail into detailList
        And find the detail then add it into detailList

        Args:
            assessmentName (string): The name of the assessment
        
        Returns:
            string: If the detail is valid, return the detail. Otherwise, return an empty string.
        '''
        locators = {
            'assesment': [By.XPATH, '//*[@id="region-main"]/div/div[2]/div[1]/table/tbody/tr[2]/td[2]'],
            'assesment2': [By.XPATH, '//*[@id="region-main"]/div/div[2]/div[2]/table/tbody/tr[2]/td[2]'],
            'testSheet': [By.XPATH, '//*[@id="region-main"]/div/table/tbody/tr/td[1]'], 
            'testSheet2': [By.XPATH, '//*[@id="region-main"]/div/table/tbody/tr[1]/td[2]'],
            'testSheet3': [By.XPATH, '//*[@id="region-main"]/div/div[2]/p'],
            'testSheet_oneUpTime': [By.XPATH, '//*[@id="yui_3_15_0_3_1680874833431_310"]'],
            'testSheet_oneUpTime2': [By.XPATH, '//*[@id="yui_3_15_0_3_1680874833431_310"]/span'],
        }
        for locator in locators.values():
            try:
                status = self.driver.find_element(*locator).text
            except NoSuchElementException:
                detailList = '作業狀態 : 無法讀取\n\n'
            else:
                if '已經完成' in status or '已繳交' in status or '已經提交' in status: 
                    detailList = '作業狀態 : 已繳交✅\n\n'
                    assessmentName = '✅' + assessmentName
                elif '測驗還不能使用' in status: 
                    detailList = '作業狀態 : 尚未開放測驗\n\n'
                else: 
                    detailList = '作業狀態 : 未繳交❌\n\n'
                break

        '''get detail'''
        try:
            detail = self.driver.find_elements(By.XPATH, '//*[@id="region-main"]/div/div[1]//p')
            for m in range(len(detail)):
                detailList += detail[m].text + '\n'
            return assessmentName, detailList
        
        except NoSuchElementException:
            print('NoSuchElementException: Assessment detail not found')
            return ''


    def split_date(self, data)-> str:
        '''Split the date from the string

        Args:
            data (string): The string that contains the date

        Returns:
            str: The formatted date
        '''
        date = data.split('(')[0]
        date = '202' + str(date.split('202', 1)[1])
        date = date.replace('年', '-').replace('月', '-').replace('日', '').replace(' ', '')
        return date

    #TODO: return end time and start time
    def split_time(self, data)-> str:
        '''Split the time from the string

        Args:
            data (sting): The string that contains the time

        Returns:
            str: The formatted time
        '''
        data = data.rsplit(' ', 1)[1]
        time = ''
        for t in data:
            if t.isdigit() or t == ":":
                time += t
        return time