import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape():
    driver = webdriver.Chrome()
    driver.get('http://moodle.cute.edu.tw/')

    username = driver.find_element(By.NAME, 'username')
    username.send_keys('1112461002')
    password = driver.find_element(By.NAME, 'password')
    password.send_keys('Qwer1234')
    password.send_keys(Keys.RETURN)

    driver.implicitly_wait(10)

    button = driver.find_elements(By.CLASS_NAME, 'coursequicklink')
    button[2].click()

    driver.implicitly_wait(10)

    #assert 'Dashboard' in driver.title
    
    assesmentName = driver.find_elements(By.CLASS_NAME, 'instancename')
    for i in assesmentName:
        print(i.text)

    driver.quit()


def __main__():
    scrape()

if __name__ == '__main__':
    __main__()