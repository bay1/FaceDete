#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-30 20:53:54

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xxxxxxxxxxx'
    CSRF_ENABLED = True
    # 百度AI第三方配置
    APP_ID = 'xxxxxx'
    API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxx'
    SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    GROUP_ID = 'yb'
    
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

class ProductionConfig(Config):
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}