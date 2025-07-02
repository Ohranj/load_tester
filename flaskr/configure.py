from .helpers.Response import Response
from .helpers.Configs import Configs
from .helpers.BuildTest import BuildTest
from selenium.common.exceptions import NoSuchElementException


from flask import ( Blueprint, request )

bp = Blueprint('configure', __name__, url_prefix='/configure')


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