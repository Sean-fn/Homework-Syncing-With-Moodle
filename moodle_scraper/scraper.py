from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class MoodleScraper():
    def __init__(self, driver):
        self.driver = driver
    def get_course_name(self, index):
        course_titles = self.driver.find_elements(By.TAG_NAME, 'h3')        #course title in the dashboard
        course_name = course_titles[index].text.split('[')[0][6:]
        return course_name

    '''
    TODO: auto switch semesters
    '''
    def navigate_to_course(self, index):
        course_titles = self.driver.find_elements(By.TAG_NAME, 'h3')        #course title in the dashboard
        if course_titles[index].text[:6] == '111(下)':
            course_name = course_titles[index].text.split('[')[0][6:]
            print('此課程名子：', course_name)
            if course_titles[index].text.startswith('111(下)') and course_titles[index].text.split('[')[0][6:] == course_name:
                courses_button = self.driver.find_elements(By.CLASS_NAME, 'coursequicklink')
                courses_button[index].click()
                print('進入', course_name, '課程')
                try:
                    assert '課程' in self.driver.title
                except AssertionError:
                    print('AssertionError : 課程')
                return True
            print('非111下的課程')
            return False


    def navigate_to_assessment(self, index, assessment_type = [' 作業', ' 測驗卷'], not_assessment_type = [' 檔案',  ' 討論區', ' SCORM教材包']):
        assessment_links = self.driver.find_elements(By.CLASS_NAME, "instancename")
        hw_type = assessment_links[index].find_elements(By.CLASS_NAME, "accesshide ")
        for type in hw_type:
            print('tag = ', type.get_attribute('innerHTML'))
            if type.get_attribute('innerHTML') in not_assessment_type:
                return False
            elif type.get_attribute('innerHTML') in assessment_type:
                assessment_links[index].click()
                return True
        #if no type tag, click the link
        assessment_links[index].click()
        return True


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
        'testSheet': [By.XPATH, '//*[@id="region-main"]/div/div[1]/p[2]'],
        'testSheet2': [By.XPATH, '//*[@id="yui_3_15_0_3_1679715868097_305"]/div[1]/p[3]'],
        }

        for locator in locators.values():
            try:
                print('exicute = ', locator)
                assessment_deadline = self.driver.find_element(*locator)
                print('assessment_deadline = ', assessment_deadline.get_attribute('innerHTML'))
                return assessment_deadline.get_attribute('innerHTML')
            except NoSuchElementException:
                print('NoSuchElementException: Assessment deadline not found')
                print('finding next element')
                continue
        return ''
            

    def get_assessment_detail(self, assessmentName):
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
                print('status = ', status)
            except:
                detailList = '作業狀態 : 無法讀取\n\n'
                print('detailList = ', detailList)
            else:
                if '已經完成' in status or '已繳交' in status or '已經提交' in status: 
                    detailList = '作業狀態 : 已繳交✅\n\n'
                    assessmentName = '✅' + assessmentName
                elif '測驗還不能使用' in status: detailList = '作業狀態 : 尚未開放測驗\n\n'
                else: detailList = '作業狀態 : 未繳交❌\n\n'
                print('detailList = ', detailList)
                break

        try:
            detail = self.driver.find_elements(By.XPATH, '//*[@id="region-main"]/div/div[1]//p')
            for m in range(len(detail)):
                detailList += detail[m].text + '\n'
            return assessmentName, detailList
        except NoSuchElementException:
            print('NoSuchElementException: Assessment detail not found')
            return ''


    def split_date(self, data):
        print('processing date: ', data)
        date = data.split('(')[0]
        print('date = ', date)
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