# B 站弹幕 protobuf 协议还原分析
> 原文链接 https://mp.weixin.qq.com/s/OzcjH8UXZl62p8TUgZQadg


## Protobuf介绍
Protobuf (Protocol Buffers) 是谷歌开发的一款无关平台，无关语言，可扩展，**轻量级高效的序列化结构的数据格式**，用于将自定义数据结构序列化成字节流，和将字节流反序列化为数据结构。所以很适合做数据存储和为不同语言，不同应用之间互相通信的数据交换格式，只要实现相同的协议格式，即后缀为proto文件被编译成不同的语言版本，加入各自的项目中，这样不同的语言可以解析其它语言通过Protobuf序列化的数据。目前官方提供c++，java，go等语言支持。
压缩程度高，相同量数据传输速度更快。

## protobuf协议还原
安装编译器 Protocol Compiler Installation
```https://github.com/protocolbuffers/protobuf/releases```

安装python模块
```
pip install protobuf
```

反序列化
```
response = requests.get('https://api.bilibili.com/x/v2/dm/web/seg.so', params=params, cookies=cookies,
                            headers=headers)
info = Feed()
info.ParseFromString(response.content)
_data = MessageToDict(info, preserving_proto_field_name=True)
messages = _data.get("message") or []
```