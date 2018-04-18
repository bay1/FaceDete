#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-30 20:53:54

from flask import Blueprint

error = Blueprint('error', __name__)

from . import errors