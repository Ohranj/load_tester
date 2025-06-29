from flask import ( jsonify, make_response )

class Response:
    def __init__(self, data, status):
        self.status = status
        self.data = data;
    def make_json_response(self):
        return make_response(jsonify(self.data), self.status)
