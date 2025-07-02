from .helpers.Response import Response
from flask import ( Blueprint, request )
import openpyxl
import time

bp = Blueprint('sheet', __name__, url_prefix='/sheet')


#
@bp.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['sheet']
    path = f"./uploads/sheets/{int(time.time())}.xlsx";
    uploaded_file.save(path)


    df = openpyxl.load_workbook(path)
    sheet = df.active
    rows = [];
    for row in range(0, 6):
        rowData = [];
        for col in sheet.iter_cols(1, sheet.max_column):
            rowData.append(col[row].value)
        rows.append(rowData)

    data = {
        'head': rows,
        'name': uploaded_file.filename,
        'rows': sheet.max_row
    }

    jsonData = { 'success': True, 'message': 'Sheet uploaded', 'data': data, 'errors': [] }
    response = Response(jsonData, status = 200)
    return response.make_json_response()