from .helpers.Response import Response
from flask import ( Blueprint, request )
from datetime import datetime
import os, time, pathlib
from flaskr.db import get_db
import psutil

bp = Blueprint('poll', __name__, url_prefix='/poll')


#
@bp.route('/', methods=['GET'])
def index():
    data = {
        'sys_ram':  dict(psutil.virtual_memory()._asdict())['percent'],
        'cpu_prcnt': psutil.cpu_percent(interval=1)
    }

    #Read db

    jsonData = { 'success': True, 'message': 'Load retrieved', 'data': data, 'errors': [] }
    response = Response(jsonData, status = 200)
    return response.make_json_response()
