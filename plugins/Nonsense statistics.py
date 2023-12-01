# from nonebot import *
# from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
# from nonebot.rule import *
#
#
# async def shuiqun_rule(event: Event) -> bool:
#     with open("whitelist.txt", encoding='utf-8') as file:  # 不用txt也是可以的
#         white_block = []
#         for line in file:
#             line = line.strip()
#             line = re.split("[ |#]", line)
#             white_block.append(line[0])
#     try:
#         whatever, group_id, user_id = event.get_session_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
#     except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
#         group_id = None
#         user_id = event.get_session_id()
#     if group_id == None or group_id in white_block:
#         return True
#     else:
#         return False
#
#
# shuiqun = on_message(rule=shuiqun_rule, priority=50)
#
#
# @shuiqun.handle()  # 针对特定事项进行回复
# async def shuiqun(bot: Bot, event: GroupMessageEvent):
#     await updade_fayan(user_id, group_id, data)
#
#
# import sqlite3
#
# async def updade_fayan(user_id, group_id, data):
#     rk = sqlite3.connect('你的数据库文件想存放的位置和名字.db') #不需要自己手动建一个，当没有链接到时sqlite3会自动新建一个db文件
#     # 判断是否存在群成员发言排行表
#     c = rk.cursor() # 新建一个数据库的游标
#     biaoming = "group" + group_id #对于每一个群聊都分别建一个表进行消息处理，表名随意，需要注意的是不能数字开头
#     c.execute(f'''CREATE TABLE if not exists {biaoming}
#                                                 (ID int primary key not null,
#                                                 cishu int not null
#                                                 )
#                                             ''')
#     '''
#     这里使用的是create table if not exists来判断是否存在一个以当前群聊命名的表
#     当然，这个的前提是当天群聊内有人发言。所以在设置消息接收的优先级时可以往高级设
#     或者可以每天0点新建一遍所有群聊的表名
#     表内列名只用写id——对应的发言人，cishu——该用户发言次数即可
#     如果想一表多用什么的就自己加吧
#     '''
#     # 判断当前群聊是否全部成员已加入（这部分并不需要写，可以只判断当前发言用户有没有加入，我这么写会导致后面一个地方出问题）
#     for i in data: #这个data是接受消息代码中获取的当前群聊用户列表
#         c.execute(f"select ID from {biaoming} where ID={i['user_id']}")
#         result = c.fetchone()
#         if result:
#             www = 1
#         else: #如果没有这个成员
#             c.execute(f"insert into {biaoming}(ID,cishu) VALUES ({i['user_id']}, 0)") #插入以taQQ号作为id的列，cishu设置为0
#     # 开始加发言次数
#     w = c.execute(f"select cishu from {biaoming} where ID={user_id}") #获取发言用户的发言次数
#     for row in w:
#         c.execute(f"update {biaoming} set cishu = {row[0] + 1} where ID ={user_id}") #更新，次数加一
#     rk.commit() #上传修改
#     rk.close() #一定要记得关闭
