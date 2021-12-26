import asyncio
import websockets
""" 
websocket 服务端
https://github.com/Vuka951/tutorial-code/tree/master/py-websockets
"""
connected = set()

async def server(websocket, path):
    # Register.
    connected.add(websocket)
    try:
        async for message in websocket:
            for conn in connected:
                # 发送消息到非发送方的所有客户端
                if conn != websocket:
                    # await conn.send(f'Got a new MSG FOR YOU: {message}')
                    print("Got",message)
                    await conn.send(message)
    finally:
        # Unregister.
        connected.remove(websocket)
    

start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
