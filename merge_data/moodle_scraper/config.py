import json
import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


load_dotenv()

class MoodleInit():
    def __init__(self, userId, pwd):
        self.moodle_creds = {'ID': userId, 'password': pwd}

        self.driver = self._init_driver()
        self.login()


    def lood_moodle_creds(self, file):
        with open(file, 'r') as f:
            return json.load(f)

    def _init_driver(self):
        return webdriver.Chrome()


    def login(self):
        self.driver.get('http://moodle.cute.edu.tw/')

        username = self.driver.find_element(By.NAME, 'username')
        username.send_keys(self.moodle_creds['ID'])
        password = self.driver.find_element(By.NAME, 'password')
        password.send_keys(self.moodle_creds['password'])
        password.send_keys(Keys.RETURN)
        try :
            assert '中國科技大學', 'moodle 學習平台' in self.driver.title
        except AssertionError:
            print('AssertionError : 中國科技大學, moodle 學習平台')
            self.driver.quit()
            return AssertionError('Faild to login to moodle')
        
    def logout(self):
        self.driver.quit()