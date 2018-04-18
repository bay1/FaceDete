#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-30 20:53:54
# -i https://pypi.tuna.tsinghua.edu.cn/simple

from homeapp import create_app
from flask_script import Manager, Shell, Server

app = create_app('default')

manager = Manager(app)

# shell运行内容导入
manager.add_command(
    "shell",
    Shell(make_context=lambda: {'app': app}))

manager.add_command(
    "runserver",
    Server(host='0.0.0.0'))

if __name__ == '__main__':
    manager.run()