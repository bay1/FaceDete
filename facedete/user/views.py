#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-30 20:53:54

import re
import socket
import base64
from . import user
from ..extensions import db
from ..models import User, Signlog
from flask import current_app, request, jsonify


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
            pcname = socket.getfqdn(socket.gethostname(  ))
            ip = socket.gethostbyname(pcname)
            uid = result['result'][0]['uid']
            user = User.query.filter_by(student_num=uid).first()
            add_log = Signlog(
                ip =ip,
                pc_name = pcname
            )
            add_log.user_student_num=user.id
            db.session.add(add_log)
            return jsonify({"status": True, 'msg': user.name+"\n您在\n电脑:"+pcname+"上\n签到成功了~"})
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
                check_stu_num = User.query.filter_by(student_num=result_id).first()
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
        check_stu_num.log_id=result['log_id']
        if check_stu_num.log_id:
            return jsonify({"status": True, 'msg': "人脸更新成功"})
        else:
            return jsonify({"status": True, 'msg': "注册成功"})
    else:
        return jsonify({"status": False, 'msg': "请检查输入"})
