from time import sleep
import os 
from selenium import webdriver
from conftest import config_env
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains


my_email = os.environ['SECERT_1']
my_password = os.environ['SECERT_2']
Agent_email = 'abcde@gmail.com'
Agent_role = 'Agent'
Agent_name = 'abc@#123'


def startup(config_env, login=0):
    chrome_service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage"]
    for option in options:
        chrome_options.add_argument(option)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    if login == 1:
        if config_env == 'dev':
            driver.get("https://help.readyly.dev/agent/login")
        elif config_env == 'prod':
            driver.get("https://help.readyly.app/agent/login")
        driver.maximize_window()
        sleep(15)
        email = driver.find_elements(By.TAG_NAME, 'input')[0]
        password = driver.find_elements(By.TAG_NAME, 'input')[1]
        global my_email, my_password
        email.send_keys(my_email)
        password.send_keys(my_password)
        loginbutton = driver.find_elements(By.TAG_NAME, 'button')[1]
        sleep(10)
        ActionChains(driver).move_to_element(loginbutton).click().perform()
        sleep(15)
    return driver


def test_Agent_Email_sorting(config_env):
    driver = startup(config_env, 1)
    if config_env != 'dev':
        return
    #  Agent tab Button
    driver.find_elements(By.TAG_NAME, 'a')[0].click()
    #  masking button
    sleep(5)
    driver.find_elements(By.TAG_NAME, 'svg')[1].click()
    sleep(10)
    email_coloum = driver.find_elements(By.TAG_NAME, 'th')[0]
    email_coloum.click()
    table_values = driver.find_elements(By.TAG_NAME, 'td')
    ascending_values = []
    for values in range(0, 42, 6):
        value = table_values[values].text
        if value != ' ' or value != 'None':
            ascending_values.append(value)
    driver.quit()
    assert sorted(ascending_values) == ascending_values
