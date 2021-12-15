import asyncio
from websockets import connect
import logging
import json
import websockets

logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


# async def hello(uri):
#     async with connect(uri) as websocket:
#         data = {
#             "op": "subscribe",
#             "params": ["quote@BTCUSDT"],
#             "seq": 1
#         }
#         await websocket.send(json.dumps(data))
#         await websocket.recv()
#
# asyncio.run(hello("wss://api.latibac.com/api/v1/realtime/ws"))

# 向服务器端认证，用户名密码通过才能退出循环
async def auth_system(websocket):
    while True:
        cred_text = input("please enter your username and password: ")
        await websocket.send(cred_text)
        response_str = await websocket.recv()
        if "congratulation" in response_str:
            return True


# 向服务器端发送认证后的消息
async def send_msg(websocket):
    data = {
        "op": "subscribe",
        "params": ["quote@BTCUSDT"],
        "seq": 1
    }
    await websocket.send(json.dumps(data))
    while True:
        recv_text = await websocket.recv()
        print(f"{recv_text}")


# 客户端主逻辑
async def main_logic():
    async with websockets.connect('wss://api.latibac.com/api/v1/realtime/ws') as websocket:
        #await auth_system(websocket)
        await send_msg(websocket)

asyncio.get_event_loop().run_until_complete(main_logic())