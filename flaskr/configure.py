from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import io
import os
import glob
import base64
from PIL import Image
from .helpers.Response import Response
from .helpers.Configs import Configs
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select


from flask import ( Blueprint, request )

bp = Blueprint('configure', __name__, url_prefix='/configure')


screenshotPaths = []
screenshotDir = './screenshots/temp/'

#
@bp.route('/list', methods=['GET'])
def list_config():
    actions = Configs()
    data = {
        'actionsList': actions.actionsList,
        'elementLookups': actions.elementLookups,
        'fieldTypes': actions.fieldTypes
    }
    jsonData = { 'success': True, 'message': 'Config variables retrieved', 'data': data, 'errors': [] }
    response = Response(jsonData, 200)
    return response.make_json_response()

#
@bp.route('/test', methods=['POST'])
def run_test():
    files = glob.glob(screenshotDir + '*')
    for f in files:
        os.remove(f)

    driver = webdriver.Chrome()
    driver.set_window_size(1536, 864)
    driver.implicitly_wait(3)

    body = request.get_json()
    for x in body['steps']:
        print(x)

    errors = [];
    didSucceed = True;
    try:
        if body['steps'][0]['type'] != 'visit':
            raise Exception('A visit should be the first step');
        step_through_test(driver, body['steps'])
    except NoSuchElementException as err:
        print(err)
        errors.append({ 'message': 'Element not found' })
        didSucceed = False;
    except Exception as err:
        print(err)
        errors.append({ 'message': 'Please check steps and try again' })
        didSucceed = False;
    driver.quit()

    data = {
        'screenshots': []
    }
    for x in screenshotPaths:
        path = f"{screenshotDir}{x['path']}.png"
        encodedImg = get_encoded_img(path)
        data['screenshots'].append({'encoding': encodedImg, 'name': x['name']})

    jsonData = { 'success': didSucceed, 'message': 'Test completed', 'data': data, 'errors': errors }
    del screenshotPaths[:]
    status = 200 if didSucceed else 422
    response = Response(jsonData, status)
    return response.make_json_response()

def step_through_test(driver, steps):
    for x in range(0, len(steps)):
        step = steps[x];
        match(step['type']):
            case 'visit':
                driver.get(step['value'])
            case 'sleep':
                time.sleep(step['value'])
            case 'screenshot':
                path = int(time.time())
                driver.save_screenshot(f"{screenshotDir}{path}.png")
                screenshotPaths.append({'path': path, 'name': step['screenshot_name']})
            case 'input':
                actions = Configs()
                find_by = actions.elementLookups[step['selector_type']]
                elem = get_elem_on_page(driver, find_by, step['value']);
                match step['field_type_id']:
                    case 0 | 1:
                        elem.send_keys(step['field_value'])
                    case 2:
                        select_elem = Select(elem)
                        select_elem.select_by_visible_text(step['field_value'])
                    case 3:
                        elem.click()
            case 'click':
                actions = Configs()
                find_by = actions.elementLookups[step['selector_type']]
                elem = get_elem_on_page(driver, find_by, step['value']);
                elem.click()

def get_elem_on_page(driver, find_by, value) -> str:
    elem = None;
    match find_by['human_type']:
        case 'Element Id':
            elem = driver.find_element(By.ID, value)
        case 'Element Class':
            elem = driver.find_element(By.CLASS_NAME, value)
        case 'Element Tag':
            elem = driver.find_element(By.TAG_NAME, value)
        case 'Element Name':
            elem = driver.find_element(By.NAME, value)
        case 'Element Link Text':
            elem = driver.find_element(By.LINK_TEXT, value)
        case 'Element CSS Selector':
            elem = driver.find_element(By.CSS_SELECTOR, value)
    return elem;

def get_encoded_img(path):
    img = Image.open(path, mode='r')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
    return my_encoded_img