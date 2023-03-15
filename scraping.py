import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape():
    # Set up the driver
    driver = webdriver.Chrome()

    # Navigate to the login page
    driver.get('http://moodle.cute.edu.tw/')

    # Find the username and password fields and enter your credentials
    username = driver.find_element(By.NAME, 'username')
    username.send_keys('1112461002')
    password = driver.find_element(By.NAME, 'password')
    password.send_keys('Qwer1234')
    password.send_keys(Keys.RETURN)

    # Wait for the page to load
    driver.implicitly_wait(10)

    button = driver.find_elements(By.CLASS_NAME, 'coursequicklink')

    # Click the button
    button[2].click()

    # Wait for the page to load
    driver.implicitly_wait(10)

    # Verify that you are logged in
    #assert 'Dashboard' in driver.title
    
    assesmentName = driver.find_elements(By.CLASS_NAME, 'instancename')
    for i in assesmentName:
        print(i.text)


    # Close the browser
    driver.quit()

def __main__():
    scrape()

if __name__ == '__main__':
    __main__()