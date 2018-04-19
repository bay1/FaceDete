$(document).ready(function () {
    var video = document.getElementById('video'),
        canvas = document.getElementById('canvas'),
        regButton = document.getElementById('regButton'),
        student_id = document.getElementById('student'),
        vendorUrl = window.URL || window.webkitURL;
    //媒体对象
    // 老的浏览器可能根本没有实现 mediaDevices，所以我们可以先设置一个空的对象
    if (navigator.mediaDevices === undefined) {
        navigator.mediaDevices = {};
    }
    // 一些浏览器部分支持 mediaDevices。我们不能直接给对象设置 getUserMedia 
    // 因为这样可能会覆盖已有的属性。这里我们只会在没有getUserMedia属性的时候添加它。
    if (navigator.mediaDevices.getUserMedia === undefined) {
        navigator.mediaDevices.getUserMedia = function (constraints) {

            // 首先，如果有getUserMedia的话，就获得它
            var getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

            // 一些浏览器根本没实现它 - 那么就返回一个error到promise的reject来保持一个统一的接口
            if (!getUserMedia) {
                return Promise.reject(new Error('getUserMedia is not implemented in this browser'));
            }

            // 否则，为老的navigator.getUserMedia方法包裹一个Promise
            return new Promise(function (resolve, reject) {
                getUserMedia.call(navigator, constraints, resolve, reject);
            });
        }
    }

    navigator.mediaDevices.getUserMedia({ audio: false, video: { 'facingMode': "user" } })
        .then(function (stream) {
            var video = document.querySelector('video');
            // 旧的浏览器可能没有srcObject
            if ("srcObject" in video) {
                video.srcObject = stream;
            } else {
                // 防止在新的浏览器里使用它，因为它已经不再支持了
                video.src = window.URL.createObjectURL(stream);
            }
            video.onloadedmetadata = function (e) {
                video.play();
            };
        })
        .catch(function (err) {
            console.log(err.name + ": " + err.message);
        });
    regButton.addEventListener('click', function () {

        //绘制canvas图形
        canvas.getContext('2d').drawImage(video, 0, 0, 400, 300);

        //把canvas图像转为img图片
        var data = {
            img: canvas.toDataURL("image/png"),
            student_id: student_id.value
        }
        $.ajax(
            {
                type: 'POST',
                url: '../checkReg',
                data: JSON.stringify(data),
                dataType: "json",
                complete: function(res){
                    console.log(res);
                    if (res.responseJSON) {
                        alert(res.responseJSON.msg);
                    }
                    else {
                        alert("服务端发生错误")
                    }
                }
            }
        )
    });
})