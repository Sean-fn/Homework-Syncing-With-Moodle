from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class MoodleScraper():
    def __init__(self, driver):
        self.driver = driver

    '''
    TODO: auto switch semesters
    '''
    def navigate_to_course(self, index):
        course_titles = self.driver.find_elements(By.TAG_NAME, 'h3')        #course title in the dashboard
        if course_titles[index].text[:6] == '111(下)':
            course_name = course_titles[index].text.split('[')[0][6:]
            # print('此課程名子：', course_name)
            if course_titles[index].text.startswith('111(下)') and course_titles[index].text.split('[')[0][6:] == course_name:
                courses_button = self.driver.find_elements(By.CLASS_NAME, 'coursequicklink')
                courses_button[index].click()
                # print('進入', course_name, '課程')
                try:
                    assert '課程' in self.driver.title
                except AssertionError:
                    print('AssertionError : 課程', AssertionError)
                return course_name
            return False


    def navigate_to_assessment(self, index):
        aa = self.driver.find_elements(By.CLASS_NAME, "activityinstance")
        link_elements = []
        for a in aa:
            link_elements.append(a.find_element(By.TAG_NAME, "a"))

        url = link_elements[index].get_attribute("href")
        if 'assign' in url or 'quiz' in url:
            link_elements[index].click()
            return True
        return False


    def get_url(self):
        try:
            return self.driver.current_url
        except:
            return ''

    def get_assessment_name(self):
        try:
            assessment_name = self.driver.find_element(By.TAG_NAME, 'h2').text
            return assessment_name
        except NoSuchElementException:
            print('NoSuchElementException: Assessment name not found')
            return ''


    def get_assessment_deadline(self):
        locators = {
        'first': [By.XPATH, '//*[@id="region-main"]/div/div[2]/div[1]/table/tbody/tr[4]/td[2]'],
        'sec': [By.XPATH, '//*[@id="region-main"]/div/div[2]/div[2]/table/tbody/tr[4]/td[2]'],
        'third': [By.XPATH, '//*[@id="yui_3_15_0_3_1679661660567_303"]'],
        'testSheet': [By.XPATH, '//*[@id="yui_3_15_0_3_1681126092687_303"]'],
        'testSheet1': [By.XPATH, '//*[@id="region-main"]/div/div[1]/p[2]'],
        'testSheet2': [By.XPATH, '//*[@id="yui_3_15_0_3_1679715868097_305"]/div[1]/p[3]'],
        }

        for i, locator in enumerate(locators.values()):
            try:
                assessment_deadline = self.driver.find_element(*locator).get_attribute('innerHTML')
                '''
                make sure getting the right deadline
                '''
                if '年' not in assessment_deadline and '月' not in assessment_deadline and '日' not in assessment_deadline :
                    continue
                return assessment_deadline
            except NoSuchElementException:
                continue
        return ''
            

    #TODO: using button to determine the status of a test sheet
    def get_assessment_detail(self, assessmentName):
        '''
        get stsatus
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
        for i, locator in enumerate(locators.values()):
            try:
                status = self.driver.find_element(*locator).text
            except:
                detailList = '作業狀態 : 無法讀取\n\n'
            else:
                if '已經完成' in status or '已繳交' in status or '已經提交' in status: 
                    detailList = '作業狀態 : 已繳交✅\n\n'
                    assessmentName = '✅' + assessmentName
                elif '測驗還不能使用' in status: detailList = '作業狀態 : 尚未開放測驗\n\n'
                else: detailList = '作業狀態 : 未繳交❌\n\n'
                break

        '''
        get detail
        '''
        try:
            detail = self.driver.find_elements(By.XPATH, '//*[@id="region-main"]/div/div[1]//p')
            for m in range(len(detail)):
                detailList += detail[m].text + '\n'
            return assessmentName, detailList
        except NoSuchElementException:
            return ''


    def split_date(self, data):
        date = data.split('(')[0]
        date = '202' + str(date.split('202', 1)[1])
        date = date.replace('年', '-').replace('月', '-').replace('日', '').replace(' ', '')
        return date
    
    # def split_date2(self, data):
    #     print('processing date: ', data)
    #     if '(' not in date:
    #         return ''
    #     date = data.split('(')[0]
    #     date = date.replace('年', '-').replace('月', '-').replace('日', '').replace(' ', '')
    #     result = ''
    #     for i in date:
    #         if i.isdigit() or i == '-':
    #             result += i
    #     print('result = ', result)
    #     return result

    #TODO: return end time and start time
    def split_time(self, data):
        data = data.rsplit(' ', 1)[1]
        time = ''
        for t in data:
            if t.isdigit() or t == ":":
                time += t
        return time