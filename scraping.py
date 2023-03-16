import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class scrape():
    def __init__(self):#ID, password):
        self.driver = webdriver.Chrome()
        self.driver.get('http://moodle.cute.edu.tw/')

        username = self.driver.find_element(By.NAME, 'username')
        username.send_keys('1112461002')#ID)
        password = self.driver.find_element(By.NAME, 'password')
        password.send_keys('Qwer1234')#password)
        password.send_keys(Keys.RETURN)

        assert '中國科技大學', 'moodle 學習平台' in self.driver.title

    def extracting(self):
        data = {
            'courseName': [],
            'assesmentName': [],
            'assesmentDetail': [],
            'assesmentDate': [], 
            'assesmentTime': {}
        }
        for i in range(2, 3):
            title = self.driver.find_elements(By.TAG_NAME, 'h3')        #course title in the dashboard
            if title[i].text[:6] == '111(下)':

                #get course name
                courseName = title[i].text.split('[')
                courseName = courseName[0][6:]                      #course name
                print('此課程名子：', courseName)
                data['courseName'].append(courseName)
                print('已加入字典(課程名子)###################')

                #enter course page
                button = self.driver.find_elements(By.CLASS_NAME, 'coursequicklink')        #courses button in the dashboard
                button[i].click()

                forCount = 0
                while forCount < len(self.driver.find_elements(By.CLASS_NAME, "instancename")):     #no while loop#####################
                    outerClass = self.driver.find_elements(By.CLASS_NAME, "instancename")
                    for j in range(forCount, len(outerClass)):
                        forCount += 1
                        hw_type = outerClass[j].find_elements(By.CLASS_NAME, "accesshide ")
                        for k in hw_type:
                            print('tag = ', k.get_attribute('innerHTML'))
                            if k.get_attribute('innerHTML') in [' 作業']:#, ' 測驗卷']:
                                outerClass[j].click()
                                self.driver.implicitly_wait(3)

                                #get assesment detail
                                # status = self.driver.find_element(By.XPATH, '//*[@id="region-main"]/div/div[2]/div[1]/table/tbody/tr[4]/td[2]')      #value of status in the assesment page
                                # print(status.get_attribute('innerHTML'))
                                # data['assesmentDate'].append(status)
                                # print('已加入字典(作業狀態)###################')
                                
                                #get assesment detail
                                detailList = []
                                #status = self.driver.find_elements(By.CLASS_NAME, 'cell c1 lastcol')      #value of status in the assesment page
                                status = self.driver.find_elements(By.XPATH, '//*[@id="region-main"]/div/div[2]/div[1]/table/tbody/tr[4]/td[2]')      #value of status in the assesment page
                                #status = tagtbody.find_elements(By.CLASS_NAME, 'cell c1 lastcol')      #value of status in the assesment page
                                for m in range(len(status)):
                                    print('第', m+1, '個是', status[m].get_attribute('innerHTML'))
                                    detailList.append(status[m].get_attribute('innerHTML'))
                                data['assesmentDate'].append(detailList)
                                print(detailList)
                                print('已加入字典(作業狀態)###################')


                                #get assesment name
                                assesmentName = self.driver.find_element(By.TAG_NAME, 'h2')     #title in the assesment page
                                print('此作業名子：', courseName+' | '+assesmentName.text)
                                data['assesmentName'].append(courseName+' | '+assesmentName.text)
                                print('已加入字典(作業名子)###################')

                                self.driver.back()
                                break
                        break
                    print('forCount = ', forCount)
                self.driver.back()
        print(data)
        time.sleep(10)
        self.driver.quit()
        return data 
    

    def split_date(self, data):
        for i in range(len(data['assesmentDate'])):
            timing = data['assesmentDate'][i].rsplit(' ', 1)
            data['assesmentTime'][i] = timing[1]

            date= data['assesmentDate'][i].split('(')
            processed = date[0].split(' ')
            data['assesmentDate'][i] = processed[0][:4] + processed[1][:2] + processed[2][:2]
        print(data['assesmentDate'])
        return data

    #for 2D array
    def split_date_2D(self, data):
        for i in range(len(data['assesmentDate'][0])):
            timing = data['assesmentDate'][0][i].rsplit(' ', 1)
            data['assesmentTime'][i] = timing[1]

            date= data['assesmentDate'][0][i].split('(')
            processed = date[0].split(' ')
            data['assesmentDate'][0][i] = processed[0][:4] + processed[1][:2] + processed[2][:2]
        print(data['assesmentDate'])
        return data


def __main__():
    s = scrape()
    data = s.extracting()
    #s.split_date(data)
    s.split_date_2D(data)

if __name__ == '__main__':
    __main__()