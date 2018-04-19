#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-30 20:53:54

from . import extensions
from flask import Flask, current_app
from .config import config

def create_app(config_name='default'):
    """
    :config_name: 要使用的配置名
    :returns: Flask实例
    """

    app = Flask(__name__, static_folder='static')

    # 配置当前app
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_blueprints(app)
    register_extensions(app)

    return app

def register_extensions(app):
    extensions.db.init_app(app)

def register_blueprints(app):
    # 注册蓝图
    from .user import user
    app.register_blueprint(user)

    from .error import error
    app.register_blueprint(error, url_prefix='/error')
