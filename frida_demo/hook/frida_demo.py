import frida
import sys
""" 
夜神模拟器 adb connect 127.0.0.1:62001
逍遥模拟器 adb connect 127.0.0.1:21503
木木模拟器 adb connect 127.0.0.1:7555

"""

device = frida.get_remote_device()
# 豆瓣的包名
session = device.attach("com.douban.frodo")
# 懒人听书的包名
# session = device.attach("bubei.tingshu")
# bubei.tingshu

def on_message(message, data):
    if message["type"] == "send":
        print("[+] {}".format(message["payload"]))
    else:
        print("[-] {}".format(message))

src = open("hook0.1.js",encoding='utf-8').read()
# src = open("lanren.js",encoding='utf-8').read()


script = session.create_script(src)
script.on("message", on_message)
script.load()
sys.stdin.read()