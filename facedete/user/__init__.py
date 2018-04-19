#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-30 20:53:54

from flask import Blueprint

user = Blueprint('user', __name__)

from . import views