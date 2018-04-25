#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-30 20:53:54
# -i https://pypi.tuna.tsinghua.edu.cn/simple

import xlrd
from facedete import create_app
from facedete.extensions import db
from flask_migrate import Migrate, MigrateCommand
from facedete.models import User, Signlog
from flask_script import Manager, Shell, Server

app = create_app('default')

manager = Manager(app)
manager = Manager(app) #初始化flask-script
migrate = Migrate(app, db)

@manager.command
def readexcel():
    workbook = xlrd.open_workbook(app.config['SIGN_LOGS_CONTENS']+r'./users.xlsx')
    sheet1 = workbook.sheet_by_index(0)
    cols = sheet1.col_values(0)
    for i in range(1, sheet1.nrows):
        stu_number=str(sheet1.cell(i, 1).value)
        check_user = User.query.filter_by(student_num=stu_number).first()
        if check_user:
            pass
        else:
            user = User(name=str(sheet1.cell(i, 0).value),student_num=stu_number,group=str(sheet1.cell(i, 2).value))
            db.session.add(user)
            db.session.commit()

@manager.command
def initdb():
    # 存在drop慎用,会清除数据
    # db.drop_all()
    db.create_all()

# shell运行内容导入
manager.add_command(
    "shell",
    Shell(make_context=lambda: {'app': app, 'db':db, 'user': User, 'signlog': Signlog}))

manager.add_command(
    "runserver",
    Server(host='0.0.0.0'))

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()