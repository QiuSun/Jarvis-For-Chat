import random
import time
from multiprocessing import Pipe, Process

from database import *
from wxpy import *


def singleFriendTest(main_process):
    '''
    向wxpy进程下发单向好友检测命令
    :return:
    '''
    main_process.send(['singlefriend'])


def killWxpyProcess(main_process):
    '''
    杀死微信子进程
    :return:
    '''
    main_process.send(['exit'])


def sendMsg(main_process, friendname_msg):
    '''
    向wxpy进程下发群发命令
    :param groupname_msg_slist: 由(friend, msg)二元组组成的列表
    :return:
    '''
    message = ['sendmsg']
    message.append(friendname_msg[0])
    message.append(friendname_msg[1])
    main_process.send(message)


def saveFriendImage(main_process, save_dir):
    '''
    向wxpy进程发送获取好友头像的命令
    :return:
    '''
    main_process.send(['savefriendimage', save_dir])


def getGroupnames(main_process):
    '''
    获得群聊名称列表
    :return:
    '''
    main_process.send(['getgroupnames'])
    recv = main_process.recv()
    print('父进程收到{}'.format(recv))
    if recv[0] == 'groupnames':
        return recv[1:]


def get_current_time():
    '''
    以字符串形式返回当前时间
    '''
    return str(time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())))


def createWxpyProcess(sub_process, userid, wxid):
    '''
    创建wxpy进程
    :param sub_process:
    :param userid:
    :param wxid:
    :return:
    '''
    print('[ ]开始创建bot')
    bot = Bot()
    print('[+]bot创建成功')

    bot.enable_puid()

    if bot.alive:
        # 如果bot创建成功 向父进程发送succes信息
        sub_process.send(['success'])

    @bot.register()
    def saveMessage(msg):
        if msg.type == 'Text':
            # 如果是群消息
            if msg.member:
                insertWxGroupMessage(userid, wxid, msg.member.name, msg.sender.name,
                                     msg.create_time.strftime("%Y%m%d%H%M%S"), msg.text)
                print('[+]群聊[{}] 成员[{}] 内容[{}] 已存入数据库'.format(msg.sender.name, msg.member.name, msg.text))

    def s_singleFriendTest():
        # 遍历好友列表群发不可见字符
        cnt = 0
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
            cnt += 1
            if cnt > 10:
                print('[ ]即将退出')
                break

    def s_sendmsg(friendname_msg):
        friend = ensure_one(bot.friends().search(friendname_msg[0]))
        friend.send(friendname_msg[1])
        print('[+]向{}发送[{}]成功'.format(friendname_msg[0], friendname_msg[1]))

    def s_getgroupnames():
        groupname_list = ['groupnames']
        for group in bot.groups():
            groupname_list.append(group.name)
        sub_process.send(groupname_list)
        # return groupname_list

    for item in sub_process.__dict__.items():
        print(item)

    # 子程序进入死循环 不断监听管道内是否有命令
    while True:
        print('子进程正在运行')
        recv = sub_process.recv()
        print(recv)
        operate = recv[0]
        print('[!]operate : {}'.format(operate))

        if operate == 'singlefriend':
            # s_singleFriendTest()
            pass
        elif operate == 'sendmsg':
            s_sendmsg(recv[1:3])
        elif operate == 'getgroupnames':
            s_getgroupnames()
        elif operate == 'exit':
            print('[!]Wxpy子进程即将退出')
            exit(0)

        # print('[+]子进程正在运行')


if __name__ == "__main__":
    child_conn, parent_conn = Pipe()
    wxpy_process = Process(target=createWxpyProcess, args=(child_conn, '13038011192', '13038011192'))
    wxpy_process.start()

    time.sleep(5)
    print('即将运行单向好友检测1')
    singleFriendTest(parent_conn)
    time.sleep(5)
    print('即将运行消息群发')
    # sendMsg(("爸爸", "吃饭了吗"))

    time.sleep(5)
    print('即将显示groupnames')
    print(getGroupnames(parent_conn))

    while True:
        time.sleep(5)
        print('[+]父进程正在运行')
