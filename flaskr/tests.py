import time
import ast
import math
from datetime import datetime
from .helpers.Response import Response
from flask import ( Blueprint, request )
from flaskr.db import get_db

bp = Blueprint('tests', __name__, url_prefix='/tests')



#
@bp.route('/<id>', methods=['GET'])
def show(id):
    db = get_db()
    errors = []
    response = db.execute( 'SELECT * FROM test WHERE id = ?', [id] ).fetchone()
    testRow = {
        'id': response['id'],
        'name': response['name'],
        'created': datetime.fromtimestamp(response['created']).strftime('%d-%b-%Y %H:%M'),
        'steps': ast.literal_eval(response['body'])
    }

    data = {
        'test': testRow
    }

    jsonData = { 'success': True, 'message': 'Tests retrieved', 'data': data, 'errors': errors }
    response = Response(jsonData, status = 200)
    return response.make_json_response()


#
@bp.route('/', methods=['GET'])
def list():
    db = get_db()
    errors = []
    #Show 5 per page
    page = request.args.get('page')
    offset = (int(page) - 1) * 5
    response = db.execute( 'SELECT * FROM test LIMIT ? OFFSET ?', [5, offset] ).fetchall()
    rowsAsJson = [];
    for x in response:
        rowsAsJson.append({
            'id': x['id'],
            'name': x['name'],
            'start': ast.literal_eval(x['body'])[0]['value'],
            'created': datetime.fromtimestamp(x['created']).strftime('%d-%b-%Y %H:%M'),
            'steps': ast.literal_eval(x['body'])
        })

    totalRows = db.execute('SELECT COUNT(*) as count FROM test').fetchone()

    data = {
        'tests': rowsAsJson,
        'totalRows': totalRows['count'],
        'totalPages': math.ceil(totalRows['count'] / 5)
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
        errors.append({ 'message': 'Check that the tests name is unique' });
    jsonData = { 'success': True, 'message': 'Test stored', 'data': [], 'errors': errors }
    status = 200 if didSucceed else 422
    response = Response(jsonData, status = status)
    return response.make_json_response()