from selenium import webdriver

BASE_URL = 'http://localhost/'

def setup():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(950, 950)
    driver.get(BASE_URL)
    return driver

def teardown(driver):
    driver.quit()