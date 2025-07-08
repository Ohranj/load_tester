import os
from flask import Flask
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        WTF_CSRF_SECRET_KEY='Y3liZXJwdW5rc2NpZmlzdHVmZg=='
    )

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
    # csrf = CSRFProtect(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import configure
    app.register_blueprint(configure.bp)

    from . import tests
    app.register_blueprint(tests.bp)

    from . import sheet
    app.register_blueprint(sheet.bp)

    from . import poll
    app.register_blueprint(poll.bp)

    from . import db
    db.init_app(app)

    return app