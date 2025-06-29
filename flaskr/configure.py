import functools
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from .helpers.Response import Response


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, make_response
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('configure', __name__, url_prefix='/configure')

#
@bp.route('/test', methods=['POST'])
def run_test():
    driver = webdriver.Chrome()
    driver.set_window_size(950, 950)
    
    body = request.get_json()
    for x in body['steps']:
        print(x)

    didSucceed = True;
    try:
        driver.get('https://google.com')
        # submit_btn = driver.find_element(By.TAG_NAME, 'button')
        # submit_btn.click()
        time.sleep(1)
    except Exception as e:
        didSucceed = False;
    driver.quit()

    jsonData = { 'success': didSucceed, 'message': 'Test ran', 'data': [], 'errors': [] }
    status = 200 if didSucceed else 422
    response = Response(jsonData, status)
    return response.make_json_response()