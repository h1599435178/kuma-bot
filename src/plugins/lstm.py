import re

import requests
from nonebot import on_command, on_regex, Bot, on_notice
from nonebot.params import CommandArg, EventMessage
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment, NoticeEvent, bot

predict = on_command("聊天二", priority=5)


# 定义命令处理器，当用户发送“predict”命令时执行
@predict.handle()
async def predict(bot: Bot, event: Event, message: Message = EventMessage()):
    # 定义一个正则表达式，匹配中文字符
    pattern = re.compile(r'([\u4e00-\u9fa5]+)\s*(.*)')
    # 从会话中获取用户发送的参数
    input_data = re.match(pattern, str(message)).group(2)

    url = "http://127.0.0.1:3652/chat"
    params = {
        "input": input_data,
    }
    response = requests.get(url, params=params)
    message = response.text
    await bot.send(event=event, message=MessageSegment.text(message))


predict2 = on_command("聊天", priority=5)


@predict2.handle()
async def predict2(bot: Bot, event: Event, message: Message = EventMessage()):
    # 定义一个正则表达式，匹配中文字符
    pattern = re.compile(r'([\u4e00-\u9fa5]+)\s*(.*)')
    # 从会话中获取用户发送的参数
    input_data = re.match(pattern, str(message)).group(2)
    url = "http://127.0.0.1:3653/chatb"
    params = {
        "input": input_data,
    }
    response = requests.get(url, params=params)
    message = response.text
    await bot.send(event=event, message=MessageSegment.text(message))
