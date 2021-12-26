import asyncio
import websockets

# 获取事件循环
loop = asyncio.get_event_loop()

async def hello(message):
    # 连接 websocket 并发送消息 获取相应
    async with websockets.connect("ws://localhost:5000") as websocket:
        await websocket.send(message)
        return await websocket.recv()


def get_encrypt(message):
    print(loop.run_until_complete(hello(message)))


if __name__ =="__main__":
    for i in range(10):
        get_encrypt(str(i))



