# coding=utf-8
import sys
import random
import http.client
import urllib
import hashlib
import datetime
import time
import re
import database as db
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Signup import Ui_Dialog



class SignupLogic(QDialog,Ui_Dialog):
    def __init__(self,parent=None):
        super(SignupLogic, self).__init__(parent)
        """初始化"""
        self.setupUi(self)
        self.retranslateUi(self)
        """初始化变量"""
        self.verifycode = "1"
        self.timer = QtCore.QTimer(self) #计时器
        self.timer1 = QtCore.QTimer(self)
        """窗口初始化"""
        # self.setWindowOpacity(0.95)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        """输入框初始化"""
        # 此处改变密码输入框LEpassword的属性，使其不现实密码
        self.LE_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LE_username.setTextMargins(40, 0, 0, 0)
        """logo初始化"""
        PNG_logo = QtGui.QPixmap('./images/LOGO.png')
        self.LB_logo.setPixmap(PNG_logo)
        self.LB_logo.setScaledContents(True)
        """icon初始化"""
        PNG_username = QtGui.QPixmap('./images/username.png')
        PNG_password = QtGui.QPixmap('./images/password.png')
        PNG_phone = QtGui.QPixmap('./images/phone1.png')
        self.LBP_username.setPixmap(PNG_username)
        self.LBP_username.setScaledContents(True)
        self.LBP_phone.setPixmap(PNG_phone)
        self.LBP_phone.setScaledContents(True)
        self.LBP_password.setPixmap(PNG_password)
        self.LBP_password.setScaledContents(True)
        self.LBP_rpassword.setPixmap(PNG_password)
        self.LBP_rpassword.setScaledContents(True)
        """初始化输入框"""
        self.LE_username.setPlaceholderText("请输入昵称")
        self.LE_rpassword.setPlaceholderText("请再次输入密码")
        """初始化密码输入框"""
        # 此处改变密码输入框lineEdit_password的属性，使其不显示密码
        # 且通过正则限制输入的字符长度最多为15位
        self.LE_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LE_rpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LE_password.setPlaceholderText("密码不超过15位")
        self.LE_rpassword.setPlaceholderText("请再次输入密码")
        regx = QRegExp("^[\S|\s]{15}$")
        self.LE_password.setValidator(QRegExpValidator(regx, self.LE_password))
        self.LE_rpassword.setValidator(QRegExpValidator(regx, self.LE_rpassword))
        """初始化信号槽"""
        # qt的信号槽机制，连接按钮的点击事件和相应的方法
        self.PB_signup.clicked.connect(lambda: self.sign_up())
        self.PB_vcode.clicked.connect(lambda : self.creat_vcode())
        # 关闭按钮关闭当前对话框
        self.PB_close.clicked.connect(self.close)
        self.PB_return.clicked.connect(lambda: self.return_main())
        # 输入框有输入时，清空提示信息
        self.LE_username.textChanged.connect(lambda: self.empty_note())
        self.LE_phone.textChanged.connect(lambda: self.empty_note())
        self.LE_password.textChanged.connect(lambda: self.empty_note())
        self.LE_rpassword.textChanged.connect(lambda: self.empty_note())
        self.LE_vcode.textChanged.connect(lambda: self.empty_note())
        ################################# QSS ##################################
        self.setStyleSheet('QWidget{background-color:#FAFAFA;border-top:1px solid gray;border-width:0;}'
                           'QLineEdit{background-color:#FFFFFF;border-width:0;border-color:#D7D7D7;}'
                           'QLabel{background-color:#FFFFFF;color:red;border-width:0;}'
                           'QLabel#LB_note{font-color:red;background-color:rgb(0,0,0,0);}'
                           'QPushButton{background-color:#0094C8;border-width:0;}'
                           'QPushButton#PB_close{background-color:rgb(0,0,0,0);border-width:0;border-image:url(./images/close-g.png);}'
                           'QPushButton#PB_return{background-color:rgb(0,0,0,0);border-width:0;border-image:url(images/left.png);}'
                           'QPushButton#PB_reset,#PB_tosignup{background-color:rgb(0,0,0,0);border-width:0;}')

    def empty_note(self):
        self.LB_note.setText("")


    def sign_up(self):
        """
        注册方法
        :return:
        """
        user_name = self.LE_username.text()
        user_phone=self.LE_phone.text()
        user_password = self.LE_password.text()
        user_repassword = self.LE_rpassword.text()
        user_vcode=self.LE_vcode.text()


        if user_name == "" or user_phone == ""or user_password == ""or user_repassword == ""or user_vcode == "":
            self.LB_note.setText("请将以上信息填写完整")
        elif user_password != user_repassword:
            self.LB_note.setText("密码不一致")
            self.LE_rpassword.setText("")
        elif user_vcode != self.verifycode:
            self.LB_note.setText("验证码错误，请重新输入")
            self.LE_vcode.setText("")
        else:
            user_password = db.hash(user_password)
            if db.IsExistUser(user_name) == None:
                db.Insert_User(user_name,user_name,user_phone,user_password)
                self.LB_note.setText("注册成功")
                self.timer.timeout.connect(self.return_main)
                self.timer.start(3000)
            else:
                self.LB_note.setText("用户名重复")


    def creat_vcode(self):
        """
        生成验证码
        调用send_industry_sms()发送信息
        :return:
        """
        chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        x = random.choice(chars), random.choice(chars), random.choice(chars), random.choice(chars), random.choice(
            chars), random.choice(chars)
        self.verifycode = "".join(x)
        self.vtime="5"
        # 获取用户的手机号
        tos = self.LE_phone.text()
        # 构造短信内容，需事先在秒嘀科技审核通过该短信模板
        smsContent = '【第三视角】您的验证码为' + self.verifycode + '，请于'+ self.vtime + '分钟内正确输入，如非本人操作，请忽略此短信。'
        # 验证手机号正确性
        ret = re.match(r"^1[35678]\d{9}$", tos)
        if tos == "":
            self.LB_note.setText("请填写手机号")
        elif ret:
            # 发送短信
            self.send_industry_sms(tos, smsContent)
            # 设置倒计时
            self.count=0
            self.timer1.timeout.connect(self.count_time)
            self.timer1.start(1000)
        else:
            self.LB_note.setText("请填写符合规范的手机号")

    def count_time(self):
        self.PB_vcode.setEnabled(False)
        self.count=self.count+1
        self.PB_vcode.setText("%d秒后重新发送"%(60-self.count))
        if self.count == 60:
            self.timer1.stop()
            self.PB_vcode.setEnabled(True)
            self.PB_vcode.setText("发送验证码")


    def send_industry_sms(self,tos, smsContent):
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


    def return_main(self):
        """
        返回登录的界面
        :return:
        """
        from my_login_py import LoginLogic
        Log =LoginLogic()
        Log.show()
        if self.timer.isActive():
            self.timer.stop()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = SignupLogic()
    ui.show()
    sys.exit(app.exec_())