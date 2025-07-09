from .helpers.Response import Response
from .helpers.Configs import Configs
from .helpers.BuildTest import BuildTest
from selenium.common.exceptions import NoSuchElementException
import threading
import time
from flaskr.db import get_db
from flaskr.sheet import read_sheet
import math
from flask import current_app


from flask import ( Blueprint, request )

bp = Blueprint('configure', __name__, url_prefix='/configure')

timeline = {
    "failed": [],
    "complete": []
};

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
    body = request.get_json()

    runner = BuildTest(body['steps'])
    runner.trash_existing_temp_screenshots()
    runner.setupDriver()

    errors = [];
    didSucceed = True;
    try:
        if body['steps'][0]['type'] != 'visit':
            raise Exception('A visit should be the first step');
        runner.run()
    except NoSuchElementException as err:
        print(err)
        errors.append({ 'message': 'Element not found' })
        didSucceed = False;
    except Exception as err:
        print(err)
        errors.append({ 'message': 'Please check your steps and try again' })
        didSucceed = False;

    runner.closeDriver()

    data = {
        'screenshots': runner.retrieve_screenshots(),
        'completedSteps': runner.completedSteps
    }

    jsonData = { 'success': didSucceed, 'message': 'Test completed', 'data': data, 'errors': errors }
    status = 200 if didSucceed else 422
    response = Response(jsonData, status)
    return response.make_json_response()


@bp.route('/load/<id>', methods=['POST'])
def run_load(id):
    body = request.get_json()

    db = get_db()
    sheet = db.execute('SELECT * FROM sheet WHERE id = ?', [body['sheet']]).fetchone()
    df = read_sheet(sheet['path'])

    computedSteps = [];
    startRow = body['settings']['row'];
    threadCount = body['settings']['threads']
    for i in range(startRow, startRow + threadCount):
        threadSteps = [];
        for val in body['steps']:
            if val['dynamic']:
                cellValue = df[val['column'].upper() + str(i)].value
                if val['type'] == 'input':
                    val['field_value'] = cellValue
                else:
                    val['value'] = cellValue
            threadSteps.append(val.copy())
        computedSteps.append(threadSteps)

    thread_list = list()

    chunking = math.floor(body['settings']['threads'] / body['settings']['chunks'])
    row = 0

    global timeline
    timeline = {
        "failed": [],
        "complete": []
    }

    cur = db.cursor()
    run = cur.execute(
        'INSERT INTO run (test_id, created, results, sheet_id) VALUES (?, ?, ?, ?) RETURNING id',
        (id, int(time.time()), str([]), sheet['id'])
    )
    runRow = run.fetchone()
    db.commit()



    app = current_app._get_current_object();


    for x in range(0, body['settings']['chunks']):
        for i in range(row, row + chunking):
            t = threading.Thread(name='Test {}'.format(i), target=temp, args=(i, computedSteps[i], runRow, startRow, app))
            t.start()
            time.sleep(body['settings']['threadBreak'])
            thread_list.append(t)
        row += chunking
        if body['settings']['waitForChunkToFinish'] == True:
            for thread in thread_list:
                thread.join()
        time.sleep(body['settings']['chunkBreak'])

    if body['settings']['waitForChunkToFinish'] == False:
        for thread in thread_list:
            thread.join()


    jsonData = { 'success': True, 'message': 'Test completed', 'data': [], 'errors': [] }
    status = 200
    response = Response(jsonData, status)
    return response.make_json_response()


def temp(i, steps, runRow, startRow, app):
    runner = BuildTest(steps, True, runRow, i)
    runner.setupDriver()
    success = runner.run()
    if success is True:
        runner.closeDriver()
    else:
        timeline['failed'].append('Failed Row ' + str(i + startRow) + ' on step ' + str(runner.completedSteps + 1))
        with app.app_context():
            db = get_db()
            db.execute('UPDATE run SET results = ? WHERE id = ?', (str(timeline), runRow['id']))
            db.commit()