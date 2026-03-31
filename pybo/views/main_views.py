from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return 'Pybo index!'

@bp.route('/hello')
def hello_world():
    return 'Hello Pybo!'

@bp.route('/bye')
def bye_world():
    return 'Bye Pybo!'