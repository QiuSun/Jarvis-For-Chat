# 导入模块
from wxpy import *
import time
import random

# 新建机器人对象
bot = Bot(cache_path=True)

# 遍历好友列表群发不可见字符
for friend in bot.friends():
    chat_name = friend.name
    # 设置时延防止封号
    time.sleep(random.uniform(3, 5))
    # 使用try避免群发过程中的错误，比如无法给自己账号发送
    try:
        friend.send_msg(" ॣ ॣ ॣ")
        print("[+]{}".format(chat_name))
    except:
        print("[-]向{}发送信息失败".format(chat_name))

# 群发检测完毕
print("请到手机端微信确认单向好友")
