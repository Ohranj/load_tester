from main import setup, teardown, BASE_URL
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

import threading
import os
import time

load_dotenv()

def test_can_login():
    driver = setup()

    title = driver.title
    assert title == "Laravel"
    time.sleep(1.5)

    i_email = driver.find_element(By.NAME, 'email')
    i_email.send_keys('alex.dorrington@qav.global')

    i_pwd = driver.find_element(By.NAME, 'password')
    i_pwd.send_keys(os.getenv('MASTER_PASSWORD_PREFIX') + 'ad')

    driver.save_screenshot('./selenium/screenshots/form_input.png')
    time.sleep(1.5)

    submit_btn = driver.find_element(By.TAG_NAME, 'button')
    submit_btn.click()
    time.sleep(1.5)

    driver.save_screenshot('./selenium/screenshots/dashboard.png')

    url = driver.current_url
    assert url == BASE_URL + 'projects/overview'
    time.sleep(1.5)

    teardown(driver)

thread_list = list()

for i in range(10):
    t = threading.Thread(name='Test {}'.format(i), target=test_can_login)
    t.start()
    time.sleep(0.5)
    print('Test ' + str(i + 1) + ': started!')
    thread_list.append(t)

for thread in thread_list:
    thread.join()





#pytest selenium/auth.py
#python3 selenium/auth.py - for threads








# def test_can_not_login():
#     driver = setup()

#     title = driver.title
#     assert title == 'Laravel'
#     time.sleep(1.5)

#     i_email = driver.find_element(By.NAME, 'email')
#     i_email.send_keys('alex.dorrington@qav.global')

#     i_pwd = driver.find_element(By.NAME, 'password')
#     i_pwd.send_keys('incorrect')
#     time.sleep(1.5)

#     submit_btn = driver.find_element(By.TAG_NAME, 'button')
#     submit_btn.click()
#     time.sleep(1.5)

#     url = driver.current_url
#     assert url == BASE_URL

#