// 将百度登录的RSA 加密代码导出到windows
// 与app.py 建立的websocket 连接

!(function () {
    window.zhiyuan = e;
    var ws = new WebSocket('ws://localhost:5000');
    ws.onopen = function (evt) {
        console.log('Connection open ...');
        ws.send('Hello WebSockets!');
    };
    ws.onmessage = function (evt) {
        var password = evt.data;
        var encrypt_password = window.zhiyuan.RSA.encrypt(evt.data);
        console.log('password=' + password + '; encrypt_password=' + encrypt_password);
        ws.send('password=' + password + '; encrypt_password=' + encrypt_password);
    };
})();