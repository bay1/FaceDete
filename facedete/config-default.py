#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-30 20:53:54

import os
from aip import AipFace
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xxxxxxxxxxx'
    CSRF_ENABLED = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    # 导出文件目录
    SIGN_LOGS_CONTENS = basedir+'/file'
    # 百度AI第三方配置
    APP_ID = 'xxxxxx'
    API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxx'
    SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    CLIENT = AipFace(APP_ID,
                     API_KEY,
                     SECRET_KEY)
    GROUP_ID = 'xx'

    """ 如果有可选参数 """
    FYOPTIONS = {}
    FYOPTIONS["ext_fields"] = "faceliveness"
    FYOPTIONS["top_num"] = 3
    ADDOPTIONS = {}
    ADDOPTIONS["action_type"] = "replace"
    DETOPTIONS = {}
    DETOPTIONS["max_face_num"] = 1

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data/data-dev.sqlite')


class ProductionConfig(Config):
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data/data.sqlite')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
