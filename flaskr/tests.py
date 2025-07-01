import time
import ast
from datetime import datetime
from .helpers.Response import Response
from flask import ( Blueprint, request )
from flaskr.db import get_db

bp = Blueprint('tests', __name__, url_prefix='/tests')



#
@bp.route('/', methods=['GET'])
def list():
    db = get_db()
    errors = []
    response = [];
    try:
        response = db.execute( 'SELECT * FROM test' ).fetchall()
        db.commit()
    except Exception as err:
        errors.append({ 'message': 'Please check that the tests name is unique' });
    tests = [];
    for x in response:
        tests.append({
            'id': x['id'],
            'name': x['name'],
            'start': ast.literal_eval(x['body'])[0]['value'],
            'created': datetime.fromtimestamp(x['created']).strftime('%d-%b-%Y %H:%M')
        })

    data = {
        'tests': tests
    }

    jsonData = { 'success': True, 'message': 'Tests retrieved', 'data': data, 'errors': errors }
    response = Response(jsonData, status = 200)
    return response.make_json_response()


#
@bp.route('/', methods=['POST'])
def store():
    body = request.get_json()
    db = get_db()
    didSucceed = True;
    errors = [];
    try:
        db.execute(
            'INSERT INTO test (name, body, created) VALUES (?, ?, ?)',
            (body['name'], str(body['test']), int(time.time()))
        )
        db.commit()
    except Exception as err:
        didSucceed = False;
        errors.append({ 'message': 'Please check that the tests name is unique' });
    jsonData = { 'success': True, 'message': 'Test stored', 'data': [], 'errors': errors }
    status = 200 if didSucceed else 422
    response = Response(jsonData, status = status)
    return response.make_json_response()


#Tidy up how to store json ni sqlite