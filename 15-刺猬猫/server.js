const express = require('express');
const app = express();
const decrypt_content = require('./decrypt_content');

var bodyParser = require('body-parser');
 
app.use(bodyParser());
 
app.post('/decrypt',function(req,res){
    var request = req.body;
    console.log('收到客户端消息',request["access_key"]);
    var content =  decrypt_content.decrypt(request["chapter_content"],request["encryt_keys"],request["access_key"]);
    res.send(content);
}) 
 
 
app.listen(3000,()=>{
    console.log('开启服务，端口3000');
})