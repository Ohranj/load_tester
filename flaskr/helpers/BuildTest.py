from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from PIL import Image
from .Configs import Configs
import time, io, base64, os, glob, pathlib

class BuildTest:
    screenshotDir = './screenshots/temp'
    completedSteps = 0
    def __init__(self, steps):
        self.screenshotPaths = [];
        self.steps = steps;
    def setupDriver(self):
        driver = webdriver.Chrome()
        driver.set_window_size(1536, 864)
        driver.implicitly_wait(3)
        self.driver = driver;
    def run(self):
        for idx, x in enumerate(self.steps):
            print(x)
            match(x['type']):
                case 'visit':
                    self.driver.get(x['value'])
                case 'sleep':
                    time.sleep(x['value'])
                case 'screenshot':
                    path = int(time.time()) + idx
                    dir_exists = os.path.isdir(self.screenshotDir)
                    if dir_exists == False:
                        pathlib.Path(self.screenshotDir).mkdir(parents=True)
                    self.driver.save_screenshot(f"{self.screenshotDir}/{path}.png")
                    self.screenshotPaths.append({'path': path, 'name': x['screenshot_name']})
                case 'input':
                    actions = Configs()
                    find_by = actions.elementLookups[x['selector_type']]
                    elem = self.get_elem_on_page(find_by, x['value']);
                    match x['field_type_id']:
                        case 0 | 1:
                            elem.send_keys(x['field_value'])
                        case 2:
                            select_elem = Select(elem)
                            select_elem.select_by_visible_text(x['field_value'])
                        case 3:
                            elem.click()
                case 'click':
                    actions = Configs()
                    find_by = actions.elementLookups[x['selector_type']]
                    elem = self.get_elem_on_page(find_by, x['value']);
                    elem.click()
            self.completedSteps += 1;
    def get_elem_on_page(self, find_by, value):
        elem = None;
        match find_by['human_type']:
            case 'Element Id':
                elem = self.driver.find_element(By.ID, value)
            case 'Element Class':
                elem = self.driver.find_element(By.CLASS_NAME, value)
            case 'Element Tag':
                elem = self.driver.find_element(By.TAG_NAME, value)
            case 'Element Name':
                elem = self.driver.find_element(By.NAME, value)
            case 'Element Link Text':
                elem = self.driver.find_element(By.LINK_TEXT, value)
            case 'Element CSS Selector':
                elem = self.driver.find_element(By.CSS_SELECTOR, value)
        return elem;
    def retrieve_screenshots(self):
        screenshots = [];
        for x in self.screenshotPaths:
            path = f"{self.screenshotDir}/{x['path']}.png"
            encodedImg = self.get_encoded_img(path)
            screenshots.append({'encoding': encodedImg, 'name': x['name']})
        return screenshots
    def get_encoded_img(self, path):
        img = Image.open(path, mode='r')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
        return encoded_img
    def trash_existing_temp_screenshots(self):
        files = glob.glob(self.screenshotDir + '/*')
        for f in files:
            os.remove(f)
    def closeDriver(self):
        self.driver.quit()
