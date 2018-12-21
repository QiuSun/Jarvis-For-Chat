# coding=utf-8
"""
继承自登录的基础界面——my_login_ui.py
使用sqlite和数据库jarvis.sqlite3交互
"""

import sys
import time
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QLabel, QApplication
from PyQt5.QtCore import *
from Login import Ui_Dialog
import database as db


class LoginLogic(QDialog, Ui_Dialog):
    def __init__(self, welcome_window,parent=None):
        super(LoginLogic, self).__init__(parent)
        """初始化函数"""
        self.setupUi(self)
        self.retranslateUi(self)
        """窗口初始化"""
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        """输入框初始化"""
        # 此处改变密码输入框LEpassword的属性，使其不现实密码
        self.LE_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LE_username.setTextMargins(40, 0, 0, 0)
        self.LE_username.setPlaceholderText("请输入用户名")
        self.LE_password.setPlaceholderText("请输入密码")
        """logo初始化"""
        PNG_logo = QtGui.QPixmap('./images/LOGO.png')
        self.LB_logo.setPixmap(PNG_logo)
        self.LB_logo.setScaledContents(True)
        """icon初始化"""
        PNG_username = QtGui.QPixmap('./images/username.png')
        PNG_password = QtGui.QPixmap('./images/password.png')
        self.LBP_username.setPixmap(PNG_username)
        self.LBP_username.setScaledContents(True)
        self.LBP_password.setPixmap(PNG_password)
        self.LBP_password.setScaledContents(True)
        """信号槽初始化"""
        # qt的信号槽机制，连接按钮的点击事件和相应的方法
        self.PB_login.clicked.connect(lambda: self.sign_in(welcome_window))
        # 关闭按钮关闭当前对话框
        self.PB_close.clicked.connect(self.close)
        self.PB_tosignup.clicked.connect(lambda: self.signup(welcome_window))
        # 输入框有输入时，清空提示信息
        self.LE_username.textChanged.connect(lambda: self.empty_note())
        self.LE_password.textChanged.connect(lambda: self.empty_note())
        ################################# QSS ##################################
        self.setStyleSheet('QWidget{background-color:#FAFAFA;border-top:1px solid gray;border-width:0;}'
                           'QLineEdit{background-color:#FFFFFF;border-width:0;border-color:#D7D7D7;}'
                           'QLabel{background-color:#FFFFFF;color:red;border-width:0;}'
                           'QLabel#LB_note{font-color: red;background-color: rgb(0,0,0,0);}'
                           'QPushButton{background-color : #0094C8;border-width:0;}'
                           'QPushButton#PB_close{background-color:rgb(0,0,0,0);border-width:0;border-image: url(./images/close-g.png);}'
                           'QPushButton#PB_reset,#PB_tosignup{background-color : rgb(0,0,0,0);border-width:0;}')

    def empty_note(self):
        self.LB_note.setText("")

    def sign_in(self,welcome_window):
        """
        登陆方法
        :return:
        """
        user_name = self.LE_username.text()
        user_password = self.LE_password.text()
        if user_name == "" or user_password == "":
            self.LB_note.setText("请输入用户名和密码")
        else:
            password = db.IsExistUser(user_name)
            if password != None:
                if db.hash(user_password) == password:
                    if db.statusChange_Login(user_name):
                        self.LB_note.setText("登录成功")
                        # ___________登录成功转到主窗口_____________#
                        welcome_window.hide()
                        self.mainwindow_up()
                        # ___________登录成功转到主窗口_____________#
                    else:
                        self.LB_note.setText("登录失败，请重试！")
                    timer=QtCore.QTimer(self)
                    timer.timeout.connect(self.close)
                    timer.start(3000)


                else:
                    self.LB_note.setText("密码不正确")
            else:
                self.LB_note.setText("此用户未注册")
                ######___________登录成功转到主窗口_____________#######
                ######此处仅为测试功能用，待完善后需要删除
                welcome_window.hide()
                self.mainwindow_up()
                ######___________登录成功转到主窗口_____________#######


    def signup(self,welcome_window):
        """
        去往注册的界面
        :return:
        """
        from my_signup_py import SignupLogic
        sig = SignupLogic(welcome_window)
        sig.show()
        self.close()

    def mainwindow_up(self):
        """
            去往Main_Window的界面
            :return:
        """
        self.hide()
        import os
        os.system('python My_Window.py')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    welcome = QtWidgets
    ui = LoginLogic(welcome)
    ui.show()
    sys.exit(app.exec_())
