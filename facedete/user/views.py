#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-30 20:53:54

import re
import base64
import xlwt
from . import user
from ..extensions import db
from datetime import datetime, timedelta
from ..models import User, Signlog
from flask import current_app, request, jsonify, send_from_directory


@user.route('/sign', methods=['GET'])
def sign():
    return current_app.send_static_file('sign.html')


@user.route('/reg', methods=['GET'])
def reg():
    return current_app.send_static_file('reg.html')


@user.route('/checkSign', methods=['POST'])
def checkSign():
    data = request.get_json(force=True)
    image = data['img']
    if image:
        client = current_app.config['CLIENT']
        image = base64.b64decode(image.split(',')[-1])
        groupId = current_app.config['GROUP_ID']
        options = current_app.config['FYOPTIONS']
        result = client.identifyUser(groupId, image, options)
        if 'error_code' in result:
            return jsonify({"status": False, 'msg': "请检查是否对准了摄像头"})
        scores = result['result'][0]['scores'][0]
        if scores > 80:
            uid = result['result'][0]['uid']
            user = User.query.filter_by(student_num=uid).first()
            if not user:
                return jsonify({"status": False, 'msg': "未找到您的信息！！"})
            now_time = datetime.now()
            if user.signlogs and now_time-user.signlogs[-1].signtime < timedelta(hours=1):
                return jsonify({"status": False, 'msg': "您签到太频繁了!!\n至少间隔一小时才能签到一次哦~"})
            add_log = Signlog(
                ip=request.headers['X-Real-Ip']
            )
            add_log.user_student_num = user.id
            db.session.add(add_log)
            return jsonify({"status": True, 'msg': user.name+"\n您签到成功了~"})
        else:
            return jsonify({"status": False, 'msg': "服务出错了！！"})
    else:
        return jsonify({"status": False, 'msg': "请求失败"})


@user.route('/checkReg', methods=['POST'])
def checkReg():
    data = request.get_json(force=True)
    image = data['img']
    student_id = data["student_id"]
    if image and student_id:
        try:
            # 匹配字母和数字
            check_id = re.compile("[^a-zA-Z0-9]").sub('', student_id)
            if len(check_id) != len(student_id) or len(student_id) >= 20:
                return jsonify({"status": False, 'msg': "你想干嘛~"})
            else:
                result_id = str(check_id)
                check_stu_num = User.query.filter_by(
                    student_num=result_id).first()
                if not check_stu_num:
                    return jsonify({"status": False, 'msg': "您不是工作室成员哦~"})
        except:
            return jsonify({"status": False, 'msg': "请检查学号"})
        client = current_app.config['CLIENT']
        image = base64.b64decode(image.split(',')[-1])
        det_options = current_app.config['DETOPTIONS']
        check_image = client.detect(image, det_options)
        if check_image['result'][0]['face_probability'] != 1:
            return jsonify({"status": False, 'msg': "请对准人脸"})
        groupId = current_app.config['GROUP_ID']
        add_options = current_app.config['ADDOPTIONS']
        userInfo = ''
        result = client.addUser(result_id, userInfo,
                                groupId, image, add_options)
        if 'error_code' in result:
            return jsonify({"status": False, 'msg': "请检查是否对准了摄像头"})
        check_stu_num.log_id = result['log_id']
        if check_stu_num.log_id:
            return jsonify({"status": True, 'msg': "人脸更新成功"})
        else:
            return jsonify({"status": True, 'msg': "注册成功"})
    else:
        return jsonify({"status": False, 'msg': "请检查输入"})


@user.route('/download', methods=['GET'])
def download():
    users = User.query.all()
    row = 1
    data = xlwt.Workbook(encoding='utf-8')
    table = data.add_sheet('signlogs')
    third_col = table.col(3)
    fourth_col = table.col(4)
    third_col.width = 256*20
    fourth_col.width = 256*20
    table.write(0, 0, u'学号')
    table.write(0, 1, u'姓名')
    table.write(0, 2, u'组别')
    table.write(0, 3, '签到IP')
    table.write(0, 4, u'签到时间')
    for user in users:
        if user.signlogs:
            for user_signlog in user.signlogs:
                column = 0
                table.write(row, column, user.student_num)
                table.write(row, column+1, user.name)
                table.write(row, column+2, user.group)
                table.write(row, column+3, user_signlog.ip)
                table.write(
                    row, column+4, user_signlog.signtime.strftime("%Y-%m-%d %H:%M:%S"))
                row += 1
    data.save(current_app.config['SIGN_LOGS_CONTENS']+r'/result.xls')
    return send_from_directory(current_app.config['SIGN_LOGS_CONTENS'], 'result.xls')
