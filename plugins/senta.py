# from nonebot import on_message
# from nonebot.adapters import Bot
# from nonebot.adapters.onebot.v11 import MessageEvent, Event, Bot, MessageSegment
#
# import paddlehub as hub
#
# senta = hub.Module(name="senta_bilstm")
#
# text = ['']
#
# Senta = on_message(priority=1)
#
#
# @Senta.handle()
# async def handle_Senta(bot: Bot, event: MessageEvent):
#     text[0] = event.raw_message
#     input_dict = {"text": text}
#     result = senta.sentiment_classify(data=input_dict)
#     if (result[0]['positive_probs'] > 0.9):
#         await bot.send(event, message=result[0]['sentiment_key'])
#     elif (result[0]['negative_probs'] > 0.9):
#         await bot.send(event, message=result[0]['sentiment_key'])