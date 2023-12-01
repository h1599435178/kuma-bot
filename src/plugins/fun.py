import json
import random
import re
from io import BytesIO

import httpx
import nonebot.exception
import requests
from nonebot import on_command, on_regex, Bot, on_notice
from nonebot.params import CommandArg, EventMessage
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment, NoticeEvent
from nonebot.typing import T_State

# 查天气的url
url = "https://devapi.qweather.com/v7/weather/3d"
# 通过GEOAPI查LocationID
url2 = "https://geoapi.qweather.com/v2/city/lookup"
# 七日天气url
url3 = "https://devapi.qweather.com/v7/weather/7d"
# 实时天气url
url4 = ""


def get_location_id(city):
    params = {
        "location": city,
        "key": "82a171e17d1d4326adc46e6947550620"
    }

    response = requests.get(url2, params=params)
    result = response.json()
    if result["code"] == "200":
        location_id = result["location"][0]["id"]
        return location_id
    else:
        ValueError(f"获取城市 LocationID 失败：{result['message']}")


weather_3days = on_command('查天气', priority=5)


@weather_3days.handle()
async def _(bot: Bot, event: Event, message: Message = EventMessage()):
    # 定义一个正则表达式，匹配中文字符
    pattern = re.compile(r'([\u4e00-\u9fa5]+)\s*(.*)')
    # 匹配中文字符，并用空格分割城市名
    city_names = re.match(pattern, str(message)).group(2)

    # 如果城市名不存在，提示用户输入城市名
    if not city_names:
        await bot.send(event, '请输入城市名, 格式：查天气 <城市名>')
        return
    elif not re.compile(r'[\u4e00-\u9fa5]').findall(city_names):
        await bot.send(event, f'城市名非法！请输入正确的中文城市名, 你的输入: {city_names}')
        return

    location_id = str(get_location_id(city_names))
    querystring = {
        "location": location_id,
        "key": "82a171e17d1d4326adc46e6947550620"
    }

    response = requests.get(url, params=querystring)
    data = response.json()

    message = f"{city_names}未来三天天气预报：\n"
    for day in data["daily"]:
        date = day["fxDate"] + "日 "
        temp = day["tempMax"] + "℃ ~ " + day["tempMin"] + "℃"
        text_day = day["textDay"]
        text_night = day["textNight"]
        wind_dir = day["windDirDay"]
        wind_scale = day["windScaleDay"] + "级"
        message += f"{date} {temp} {text_day}~{text_night} {wind_dir}{wind_scale}\n"
    message = message.strip()
    await bot.send(event=event, message=MessageSegment.text(message))


weather_7days = on_command('七日天气', priority=5)


@weather_7days.handle()
async def _(bot: Bot, event: Event, message: Message = EventMessage()):
    # 定义一个正则表达式，匹配中文字符
    pattern = re.compile(r'([\u4e00-\u9fa5]+)\s*(.*)')
    # 匹配中文字符，并用空格分割城市名
    city_names = re.match(pattern, str(message)).group(2)
    # 如果城市名不存在，提示用户输入城市名
    if not city_names:
        await bot.send(event, '请输入城市名, 格式：七日天气 <城市名>')
        return
    elif not re.compile(r'[\u4e00-\u9fa5]').findall(city_names):
        await bot.send(event, f'城市名非法！请输入正确的中文城市名, 你的输入: {city_names}')
        return
    location_id = str(get_location_id(city_names))
    querystring = {
        "location": location_id,
        "key": "82a171e17d1d4326adc46e6947550620"
    }

    response = requests.request("GET", url3, params=querystring)
    data = response.json()

    message = f"{city_names}未来七天天气预报：\n"
    for day in data["daily"]:
        date = day["fxDate"] + "日 "
        temp = day["tempMax"] + "℃ ~ " + day["tempMin"] + "℃"
        text_day = day["textDay"]
        text_night = day["textNight"]
        wind_dir = day["windDirDay"]
        wind_scale = day["windScaleDay"] + "级"
        message += f"{date} {temp} {text_day}~{text_night} {wind_dir}{wind_scale}\n"
    message = message.strip()
    await bot.send(event=event, message=MessageSegment.text(message))


hhsh = on_command('说人话', priority=5)


@hhsh.handle()
async def _(bot: Bot, event: Event, message: Message = EventMessage()):
    url = 'https://lab.magiconch.com/api/nbnhhsh/guess'
    value = str(message).split(' ')[1]
    data = {
        "text": f"{value}"
    }
    json_data = json.dumps(data)
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, data=json_data, headers=headers)
    # 检查响应
    try:
        if response.status_code == 200:
            data_list = response.json()[0]
            if 'trans' in data_list:
                output = '，'.join(data_list['trans'])
                await bot.send(event, f"{value}翻译过来人话是：" + output)
                return
            else:
                await bot.send(event, f'我也不知道{value}的人话是啥，自己去百度吧')
                return
        else:
            await bot.send(event, '远程服务器错误，请联系狗管理')
            return
    except Exception as e:
        await bot.send(event, '暂时只支持输入拼音，如遇到其他错误请联系狗管理')
    # await bot.send(event=event, message=MessageSegment.text(message))


wife = on_command("随个老婆", priority=5)


@wife.handle()
async def _(bot: Bot, event: Event, message: Message = EventMessage()):
    try:
        msg = await get_wifepic(bot, event)
        await wife.finish(MessageSegment.image(msg))

    except json.JSONDecodeError:
        await bot.send(event, '未知错误，请联系狗管理')


setu = on_command("随机涩图", aliases={"随机色图", "色色"}, priority=5)


@setu.handle()
async def _(bot: Bot, event: Event, message: Message = EventMessage()):
    try:
        try:
            msg = await get_sexypic(bot, event)
            await setu.finish(MessageSegment.image(msg))
        except nonebot.exception.ActionFailed:
            await bot.send(event, '图片太涩发不出来，请重新获取')
    except json.JSONDecodeError:
        await bot.send(event, '未知错误，请联系狗管理')


dog = on_command("随机狗狗图", aliases={'来只狗', '随个狗'}, priority=5)


@dog.handle()
async def _(bot: Bot, event: Event, message: Message = EventMessage()):
    try:
        msg = await get_dogpic()
        await dog.finish(MessageSegment.image(msg))

    except json.JSONDecodeError:
        await bot.send(event, '未知错误，请联系狗管理')


cat = on_command("随机猫猫图", aliases={'来只猫', '随个猫'}, priority=5)


@cat.handle()
async def _(bot: Bot, event: Event, message: Message = EventMessage()):
    try:
        msg = await get_catpic()
        await cat.finish(MessageSegment.image(msg))

    except json.JSONDecodeError:
        await bot.send(event, '未知错误，请联系狗管理')


async def get_catpic():
    url = 'https://api.thecatapi.com/v1/images/search?limit=1'
    async with httpx.AsyncClient() as client:
        response = requests.get(url)
        data = response.json()
        image_url = data[0]['url']
    return image_url


async def get_dogpic():
    url = 'https://api.thedogapi.com/v1/images/search?limit=1'
    async with httpx.AsyncClient() as client:
        response = requests.get(url)
        data = response.json()
        image_url = data[0]['url']
    return image_url


async def get_wifepic(bot: Bot, event: Event):
    url = ['https://api.yimian.xyz/img',
           'https://t.mwm.moe/pc/',
           'https://t.mwm.moe/mp/',
           ]
    num = random.randint(0, 3)
    fore_url = url[num]
    async with httpx.AsyncClient() as client:

        response = requests.get(fore_url)
        if response.status_code == 200:
            data = response.url
            return data
        else:
            return bot.send(event, '请求错误，请重新获取')


async def get_sexypic(bot: Bot, event: Event):
    url = ['https://sex.nyan.xyz/api/v2/img?r18',
           'https://api.vvhan.com/api/girl',
           'https://ybapi.cn/API/pe_acgimg.php',
           'https://api.lolicon.app/setu/v2']
    num = random.randint(0, 3)
    fore_url = url[num]
    async with httpx.AsyncClient() as client:
        if fore_url == 'https://api.lolicon.app/setu/v2':
            r18_url = f'https://api.lolicon.app/setu/v2?r18=2'
            response = requests.get(r18_url)
            data = response.json()
            image_url = data['data'][0]['urls']['original']
            return image_url
        else:
            response = requests.get(fore_url)
            if response.status_code == 200:
                data = response.url
                return data
            else:
                return bot.send(event, '请求错误，请重新获取')


notice = on_notice()


@notice.handle()
async def handel_poke(bot: Bot, event: Event):
    description = event.get_event_description()
    values = json.loads(description.replace("'", '"'))
    # 如果机器人被戳
    if values['notice_type'] == 'notify' and values['sub_type'] == 'poke' and str(values['target_id']) == '2224869353':
        await bot.send("干啥？")
