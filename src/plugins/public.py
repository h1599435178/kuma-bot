from nonebot import on_command, on_notice
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message, Event, Bot, MessageSegment
from nonebot.exception import IgnoredException
from nonebot.message import event_preprocessor
from src.libraries.image import *


@event_preprocessor
async def preprocessor(bot, event, state):
    if hasattr(event, 'message_type') and event.message_type == "private" and event.sub_type != "friend":
        raise IgnoredException("not reply group temp message")


help = on_command('帮助', aliases={"help"})


@help.handle()
async def _(bot: Bot, event: Event, state: T_State):
    help_str = '''可用命令如下：
今日舞萌 查看今天的舞萌运势
XXXmaimaiXXX什么 随机一首歌
随个[dx/标准][绿黄红紫白]<难度> 随机一首指定条件的乐曲
查歌<乐曲标题的一部分> 查询符合条件的乐曲
[绿黄红紫白]id<歌曲编号> 查询乐曲信息或谱面信息
<歌曲别名>是什么歌 查询乐曲别名对应的乐曲
定数查歌 <定数>  查询定数对应的乐曲
定数查歌 <定数下限> <定数上限>
分数线 <难度+歌曲id> <分数线> 详情请输入“分数线 帮助”查看
帮助 下棋 或help boardgame  显示棋类游戏帮助
帮助 聊天 或help chat  显示聊天类帮助'''
    await help.send(Message([
        MessageSegment("image", {
            "file": f"base64://{str(image_to_base64(text_to_image(help_str)), encoding='utf-8')}"
        })
    ]))


help_boardgame = on_command('帮助 下棋', aliases={"help boardgame"})


@help_boardgame.handle()
async def _(bot: Bot, event: Event, state: T_State):
    help_boardgame_str = '''可用命令如下：
使用 @'BOT' 发送 <围棋>/<五子棋>/<黑白棋>开始一个对应的棋局，
一个群组内同时只能有一个棋局。
发送“落子 字母+数字”下棋，如“落子 A1”；
游戏发起者默认为先手，可使用 --white 选项选择后手；
发送“结束下棋”结束当前棋局；
发送“查看棋局”显示当前棋局；
发送“悔棋”可以进行悔棋；
发送“跳过回合”可跳过当前回合（仅黑白棋支持）；
手动结束游戏或超时结束游戏时，可发送“重载xx棋局”继续下棋，如 重载围棋棋局；
插件开源自 noneplugin/nonebot-plugin-boardgame'''
    await help.send(Message([
        MessageSegment("image", {
            "file": f"base64://{str(image_to_base64(text_to_image(help_boardgame_str)), encoding='utf-8')}"
        })
    ]))


help_boardgame = on_command('帮助 聊天', aliases={"help chat"})


@help_boardgame.handle()
async def _(bot: Bot, event: Event, state: T_State):
    help_boardgame_str = '''可用命令如下：
聊天 <语句>   获得聊天返回
聊天二 <语句>  获得聊天二返回

注：语句建议小于10个中文字符，超过10位仍读取前10位

由于训练完成度较低，不能很好的进行语句反馈，请见谅'''
    await help.send(Message([
        MessageSegment("image", {
            "file": f"base64://{str(image_to_base64(text_to_image(help_boardgame_str)), encoding='utf-8')}"
        })
    ]))



async def _group_poke(bot: Bot, event: Event) -> bool:
    value = (event.notice_type == "notify" and event.sub_type == "poke" and event.target_id == int(bot.self_id))
    return value


poke = on_notice(rule=_group_poke, priority=10, block=True)


@poke.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if event.__getattribute__('group_id') is None:
        event.__delattr__('group_id')
    await poke.send(Message([
        MessageSegment("poke", {
            "qq": f"{event.sender_id}"
        })
    ]))
