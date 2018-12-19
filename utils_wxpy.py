import random
import time
from multiprocessing import Pipe, Process

from database import *
from wxpy import *

def singleFriendTest(main_process):
    '''
    向wxpy子进程下发"单向好友检测"命令
    :param main_process: 管道中代表父进程的一端
    :return:
    '''
    main_process.send(['singlefriend'])


def groupSend(main_process, message_model, friendname_list):
    '''

    :param main_process: 管道中代表父进程的一端
    :param message_model: 要群发的消息模板 两个#内部的内容会被替换为名称
    :param friendname_list: 需要群发的好友列表
    :return:
    '''
    packet = ['groupSend', message_model].append(friendname_list)
    # 消息一次性发送到wxpy中 任务在wxpy中执行
    main_process.send(packet)



def killWxpyProcess(main_process):
    '''
    向wxpy子进程下发"自杀"命令
    :param main_process: 管道中代表父进程的一端
    :return:
    '''
    main_process.send(['exit'])


def sendMsg(main_process, friendname, message):
    '''
    向wxpy进程下发群发命令
    :param main_process: 管道中代表父进程的一端
    :param friendname_msg: (friend, msg)二元组
    :return:
    '''
    packet = ['sendmsg']
    packet.append(friendname)
    packet.append(message)
    # 向子进程发送['sendmsg', friendname, message]列表
    # 例如：若friendname='爸爸' message='吃饭了吗'
    # 构成的packet为['sendmsg', '爸爸', '吃饭了吗']
    # 将向好友列表中的'爸爸'发送'吃饭了吗'
    main_process.send(packet)


def saveFriendImage(main_process, save_dir):
    '''
    向wxpy子进程发送获取好友头像 并存放在指定文件夹下(以'好友名.jpg'存储)
    :param main_process: 管道中代表父进程的一端
    :param save_dir: 好友头像保存的文件夹
    :return:
    '''
    main_process.send(['savefriendimage', save_dir])


def getGroupnames(main_process):
    '''
    获得群聊名称列表
    :param main_process: 管道中代表父进程的一端
    :return: 群聊名称的列表
    '''
    main_process.send(['getgroupnames'])
    while True:
        recv = main_process.recv()
        print('父进程收到{}'.format(recv))
        if recv[0] == 'groupnames':
            return recv[1:]


def getFriendnames(main_process):
    '''
    获得好友名称列表
    :param main_process: 管道中代表父进程的一端
    :return: 好友名称的列表
    '''
    main_process.send(['getfriendnames'])
    while True:
        recv = main_process.recv()
        print('getFriendnames父进程收到{}'.format(recv))
        if recv[0] == 'friendnames':
            return recv[1:]

def updateKey(main_process):
    '''
    向子进程发送更新关键词列表的命令
    :param main_process: 管道中代表父进程的一端
    :return:
    '''
    main_process.send(['updatekey'])


def get_current_time():
    '''
    以字符串形式返回当前时间
    '''
    return str(time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())))


def createWxpyProcess(sub_process, userid, wxid):
    '''
    创建wxpy进程
    :param sub_process: 管道中代表子进程的一端
    :param userid: userid
    :param wxid: wxid
    :return:
    '''
    print('[ ]开始创建bot')
    bot = Bot()
    print('[+]bot创建成功')

    bot.enable_puid()

    if bot.alive:
        # 如果bot创建成功 向父进程发送succes信息
        sub_process.send(['success'])

    key_list = []

    @bot.register()
    def saveMessage(msg):
        if msg.type == 'Text':
            # 如果是群消息
            if msg.member:
                insertWxGroupMessage(userid, wxid, msg.member.name, msg.sender.name,
                                     msg.create_time.strftime("%Y%m%d%H%M%S"), msg.text)
                print('[+]群聊[{}] 成员[{}] 内容[{}] 已存入数据库'.format(msg.sender.name, msg.member.name, msg.text))

            for key in key_list:
                if key in msg:
                    pass


    def s_singleFriendTest():
        '''
        执行单向好友检测(子进程内部调用 外部无法直接调用)
        :return:
        '''
        print('[+]调用[单向好友检测]中')

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

    def s_sendMsg(friendname, message):
        '''
        向好友发送消息(子进程内部调用 外部无法直接调用)
        :param friendname: 好友名
        :param message: 消息内容
        :return:
        '''
        print('[+]调用[发送消息]中')
        friend = ensure_one(bot.friends().search(friendname))
        friend.send(message)
        print('[+]向{}发送[{}]成功'.format(friendname, message))

    def s_getGroupNames():
        '''
        获得群组的名称列表
        :return:
        '''
        # 准备报文
        packet = ['groupnames']
        for group in bot.groups():
            packet.append(group.name)
        # 子进程向父进程发送群聊列表报文
        sub_process.send(packet)

    def s_updateKey():
        # 从数据读取，更新到keylist中
        pass

    def s_getFriendnames():
        '''
        获得群组的名称列表
        :return:
        '''
        # 准备报文
        packet = ['friendnames']
        for friend in bot.friends():
            packet.append(friend.name)
        # 子进程向父进程发送群聊列表报文
        print('[ ]packet: {}'.format(packet))
        sub_process.send(packet)

    def s_groupSend(message_model, friendname_list):
        '''
        子进程中的消息群发
        :param message_model: 要群发的消息模板 两个#内部的内容会被替换为名称
        :param friendname_list: 需要群发的好友列表
        :return:
        '''

    # 子程序进入死循环 不断监听管道内是否有命令
    while True:
        print('子进程正在运行')
        recv = sub_process.recv()
        operate = recv[0]
        print('[!]operate : {}'.format(operate))
        print('[ ]packet: {}'.format(recv))

        if operate == 'singlefriend':
            # 暂时关闭单向好友检测
            # s_singleFriendTest()
            pass
        elif operate == 'sendmsg':              # 向单个好友发送消息
            s_sendMsg(recv[1], recv[2])
        elif operate == 'getgroupnames':        # 获取群聊名称列表
            s_getGroupNames()
        elif operate == 'exit':                 # wxpy自杀
            print('[!]Wxpy子进程即将退出')
            exit(0)
        elif operate == 'updatekey':            # 更新关键词列表
            s_updateKey()
        elif operate == 'getfriendnames':       # 获取好友名称列表
            s_getFriendnames()
        elif operate == 'groupsend':
            s_groupSend(recv[1], recv[2,])      # 消息群发



if __name__ == "__main__":
    child_conn, parent_conn = Pipe()
    wxpy_process = Process(target=createWxpyProcess, args=(child_conn, '13038011192', '13038011192'))
    wxpy_process.start()

    time.sleep(5)
    # print('即将运行单向好友检测1')
    # singleFriendTest(parent_conn)
    # time.sleep(5)
    # print('即将运行消息群发')
    # # sendMsg(("爸爸", "吃饭了吗"))
    #
    # time.sleep(5)
    # print('即将显示groupnames')
    # print(getGroupnames(parent_conn))

    friend_names = getFriendnames(parent_conn)

    print(friend_names)

    while True:
        time.sleep(5)
        print('[+]父进程正在运行')
