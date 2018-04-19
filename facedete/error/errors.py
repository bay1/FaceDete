from flask import current_app
from . import error

#  错误处理
@error.app_errorhandler(403)
@error.app_errorhandler(404)
@error.app_errorhandler(500)
def error(e):
    return current_app.send_static_file('error.html')
