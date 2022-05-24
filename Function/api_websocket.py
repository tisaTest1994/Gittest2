import asyncio
import logging
import json
import websockets
from Function.api_function import *

logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


# 向服务器端认证，用户名密码通过才能退出循环
async def auth_system(websocket):
    while True:
        cred_text = input("please enter your username and password: ")
        await websocket.send(cred_text)
        response_str = await websocket.recv()
        if "congratulation" in response_str:
            return True


# 向服务器端发送认证后的消息
async def send_msg(websocket, params):
    data = {
        "op": "subscribe",
        "device_id": "",
        "token": "1",
        "params": params,
        "seq": 1
    }
    await websocket.send(json.dumps(data))
    while True:
        text = await websocket.recv()
        logger.info('获得数据是{}'.format(text))
        return text


# 客户端主逻辑
async def main_logic(params):
    async with websockets.connect(get_json()['websocket']['url']) as websocket:
        #await auth_system(websocket)
        await send_msg(websocket, params)

