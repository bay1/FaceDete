# FaceDete

>结合百度AI摄像头人脸识别值班签到

##本地预览方法

>首先需要修改config-default中百度AI的应用key
并重命名为config

>依此按照下面命令

```
D:\Github\FaceDete
$ virtualenv venv

//进入venv\Scripts目录
D:\Github\FaceDete\venv\Scripts
$ activate
D:\Github\FaceDete
(venv) $ pip install -r requirements.txt
D:\Github\FaceDete
(venv) $ python manage.py runserver

>浏览器打开 
签到：http://127.0.0.1:5000/sign
注册：http://127.0.0.1:5000/reg