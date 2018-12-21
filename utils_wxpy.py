import random
import time
from multiprocessing import Pipe, Process

import urllib
import hashlib
import datetime
from database import *
from wxpy import *
import http
import database

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
    packet = ['groupsend', message_model]
    for friendname in friendname_list:
        packet.append(friendname)
    # 消息一次性发送到wxpy中 任务在wxpy中执行
    print(packet)
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

def send_industry_sms(tos, smsContent):
    """
    发送信息
    使用秒嘀科技API实现
    :return:
    """
    # 秒嘀科技注册后的账户信息
    accountSid = '6ac4f4828fef413ebaf90e5bf9bff782'          # ACCOUNT SID
    acctKey = '46cc515148fa4bf29fb571ed27b8fa63'          # AUTH TOKEN

    # 定义地址，端口等
    serverHost = "api.miaodiyun.com"
    serverPort = 443
    industryUrl = "/20150822/industrySMS/sendSMS"

    # 格式化时间戳，并计算签名
    timeStamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
    rawsig = accountSid + acctKey + timeStamp
    m = hashlib.md5()
    m.update(rawsig.encode("utf8"))
    sig = m.hexdigest()

    # 定义需要进行发送的数据表单
    params = urllib.parse.urlencode(
        {'accountSid': accountSid,
         'smsContent': smsContent,
         'to': tos,
         'timestamp': timeStamp,
         'sig': sig
         }
    )

    # 定义header
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
    # 与构建https连接
    conn = http.client.HTTPSConnection(serverHost, serverPort)
    # Post数据
    conn.request(method="POST", url=industryUrl, body=params, headers=headers)
    # 返回处理后的数据
    response = conn.getresponse()
    # 读取返回数据
    jsondata = response.read().decode('utf-8')

    # 打印完整的返回数据，测试使用 #
    print(jsondata)


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
        wxid = bot.self.wxid
        packet = ['success', wxid]
        sub_process.send(packet)
    else:
        packet = ['fail', '']
        sub_process.send(packet)

    userid = database.getLogedUserid()
    database.insertIntoWechat(userid, wxid)

    key_group_list = []

    @bot.register()
    def saveMessage(msg):
        print('[+]key_group_list', key_group_list)
        if msg.type == 'Text':
            # 如果是群消息
            if msg.member:
                insertWxGroupMessage(userid, wxid, msg.member.name, msg.sender.name,
                                     msg.create_time.strftime("%Y%m%d%H%M%S"), msg.text)
                print('[+]群聊[{}] 成员[{}] 内容[{}] 已存入数据库'.format(msg.sender.name, msg.member.name, msg.text))

                for key_group in key_group_list:
                    if msg.sender.name == key_group[1] and key_group[0] in msg.text:
                        print('[!]发送短信中!!!')
                        send_industry_sms('13038011192', '【第三视角】您的验证码为'+key_group[0] + '，请于'+ key_group[1] + '分钟内正确输入，如非本人操作，请忽略此短信。')


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
        '''

        :return:
        '''
        print('[+]开始运行【关键词更新】')
        # 从数据读取，更新到key_group_list中
        userid, wxid = getUseridAndWxidWithLogStatus()
        print('[!]userid, wxid', userid, wxid)
        key_group_list = getChosedUserKeywordAndGroup(userid, wxid)
        return key_group_list


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

    def s_getMessage(message_model, friendname):
        '''

        :param message_model:
        :param friendname:
        :return:
        '''
        return message_model

    def s_groupSend(message_model, friendname_list):
        '''
        子进程中的消息群发
        :param message_model: 要群发的消息模板 两个#内部的内容会被替换为名称
        :param friendname_list: 需要群发的好友列表
        :return:
        '''
        print('[+]开始运行【消息群发】')
        for friendname in friendname_list:
            message = s_getMessage(message_model, friendname)
            s_sendMsg(friendname, message)
            time.sleep(random.uniform(2,5))

    # 初始登录时更新
    key_group_list = s_updateKey()

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
            key_group_list = s_updateKey()
        elif operate == 'getfriendnames':       # 获取好友名称列表
            s_getFriendnames()
        elif operate == 'groupsend':
            s_groupSend(recv[1], recv[2:])      # 消息群发



if __name__ == "__main__":
    child_conn, parent_conn = Pipe()
    wxpy_process = Process(target=createWxpyProcess, args=(child_conn, '13038011192', '13038011192'))
    wxpy_process.start()

    time.sleep(5)

    # groupSend(parent_conn, '你好呀', ['俊彦', '凡凡哥'])

    time.sleep(10)
    updateKey(parent_conn)

    while True:
        time.sleep(5)
        print('[+]父进程正在运行')
