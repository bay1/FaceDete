#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-30 20:53:54

import re
import base64
from . import user
from aip import AipFace
from flask import current_app, request, jsonify


@user.route('/login', methods=['GET'])
def login():
    return current_app.send_static_file('login.html')


@user.route('/reg', methods=['GET'])
def reg():
    return current_app.send_static_file('reg.html')


@user.route('/checkLogin', methods=['POST'])
def checkLogin():
    data = request.get_json(force=True)
    image = data['img']
    if image:
        client = AipFace(current_app.config['APP_ID'],
                         current_app.config['API_KEY'], current_app.config['SECRET_KEY'])
        image = base64.b64decode(image.split(',')[-1])
        groupId = current_app.config['GROUP_ID']
        options = current_app.config['FYOPTIONS']
        result = client.identifyUser(groupId, image, options)
        if 'error_code' in result:
            return jsonify({"status": False, 'msg': "请检查是否对准了摄像头"})
        scores = result['result'][0]['scores'][0]
        if scores > 80:
            return jsonify({"status": True, 'msg': "签到成功~"})
        else:
            return jsonify({"status": False, 'msg': "你好像照丑了哦~再拍一张吧！"})
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
        except:
            return jsonify({"status": False, 'msg': "请检查学号"})
        client = AipFace(current_app.config['APP_ID'],
                         current_app.config['API_KEY'], current_app.config['SECRET_KEY'])
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
        return jsonify({"status": True, 'msg': "注册成功"})
    else:
        return jsonify({"status": False, 'msg': "请检查输入"})
