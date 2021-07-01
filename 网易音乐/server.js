
const express = require('express');
const app = express();
const encparams = require('./163');
var bodyParser = require('body-parser');

app.use(bodyParser());

app.post('/encrpt',function(req,res){
    var request = req.body;
    console.log('收到客户端消息',request);
    var result = encparams.get_params(request['ids']);
    console.log('返回加密后的params',JSON.stringify(result));
    res.send(JSON.stringify(result));
}) 


app.listen(3000,()=>{
    console.log('开启服务，端口3000');
})
