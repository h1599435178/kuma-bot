class Config:
    # 记录使用中的群组（白名单）
    user_in_group = []
    # 插件(plugins)执行优先级
    low_priority = 1
    mid_priority = 5
    high_priority = 10
    # 接话冷却时间（秒），在这段时间内不会连续两次接话
    chat_cd = 15
    # 戳一戳冷却时间（秒）
    notice_cd = 900
    # 机器人QQ号
    bot_id = "2224869353"
    # 管理员QQ号，管理员无视冷却cd和触发概率
    super_uid = ["1599435178"]
    # 聊天回复概率，用百分比表示，0-100%
    p_chat_response = 60
    # 戳一戳回复概率，用百分比表示，0-100%
    p_poke_response = 20
    # 默认禁言时间，每多戳一次会在默认禁言时间上翻倍
    default_ban_time = 60