import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from barabove_py import BarLogic

sys.path.append("..")


class Main_Window(QWidget):
    def __init__(self, parent=None):
        # --------------------------主窗体--------------------------------------#
        super(Main_Window, self).__init__(parent)
        self.resize(1000, 650)  # 设置窗口初始位置和大小
        self.center()  # 设置窗口居中
        self.setWindowTitle('Jarvis For Chat - Welcome')  # 设置窗口标题
        logo = QIcon()  # 设置窗口logo
        logo.addPixmap(QPixmap("./images/Dicon-p.png"), QIcon.Normal)
        self.setWindowIcon(logo)
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 设置隐藏边框
        # 主窗网格布局，基底
        self.main_layout = QGridLayout(self, spacing=0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        # ------------------------上边框--------------------------------------#
        # self.bara = BarLogic()
        # self.main_layout.addWidget(self.bara,0,0,1,0)
        # ------------------------左边菜单栏--------------------------------------#
        self.LeftTabWidget = QListWidget()
        self.LeftTabWidget.setFixedWidth(180)
        self.LeftTabWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.LeftTabWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.LeftTabWidget.setFrameShape(QListWidget.NoFrame)
        # 左侧组件设置
        self.left_layout = QVBoxLayout()
        self.LeftTabWidget.setLayout(self.left_layout)  # 将左侧布局（垂直）绑定到左侧组件上
        # 左侧布局
        self.main_layout.addWidget(self.LeftTabWidget, 5, 0)
        self.LeftTabWidget.currentRowChanged.connect(self.display)  # 绑定
        list_str = ['Welcome']
        for i in range(1):
            self.item = QListWidgetItem(list_str[i], self.LeftTabWidget)  # 左侧选项的添加
            self.item.setSizeHint(QSize(180, 80))
            # self.item.set(0,(i+1)*180)
            self.item.setTextAlignment(Qt.AlignCenter)  # 居中显示
        # --------------------左侧菜单栏头像------------------------------------------#
        self.avatar_layout = QGridLayout()
        self.main_layout.addLayout(self.avatar_layout, 1, 0)
        # 头像
        self.avatar = QtWidgets.QPushButton()
        self.avatar.setFixedSize(QSize(180, 180))
        self.avatar.setIcon(QIcon(r'images/avatar.png'))
        self.avatar.setIconSize(QSize(170, 170))
        self.avatar_layout.addWidget(self.avatar, 2, 0, 3, 3)  ##控件名，行，列，占用行数，占用列数，对齐方式
        self.avatar_layout.setAlignment(self.avatar_layout,Qt.AlignRight)
        # 微信/QQ
        #self.weixin = QtWidgets.QPushButton()
        #self.weixin.setFixedSize(QSize(45, 45))
        #self.weixin.setIcon(QIcon(r'Resource/images/weixin1.png'))
        #self.avatar_layout.addWidget(self.weixin, 4, 4, 1, 1)
        #self.avatar_layout.setAlignment(self.weixin, Qt.AlignRight)
        #self.avatar_layout.setAlignment(self.weixin, Qt.AlignBottom)

        ################################# QSS ##################################
        self.setStyleSheet('QWidget{background-color: rgb(255,255,255)}')
        self.LeftTabWidget.setStyleSheet('QWidget{background-color: rgb(228,228,228,90)}')
        self.avatar.setStyleSheet('QPushButton{border:0px;background-color:rgb(228,228,228,90)}')
        # --------------------------右边页面-------------------------------------------#
        # 在QStackedWidget对象中填充了4个子控件
        self.stack = QStackedWidget(self)
        self.right_layout = QGridLayout()
        # self.main_layout.addLayout(self.right_layout,0,5)
        self.stack.setLayout(self.right_layout)
        self.main_layout.addWidget(self.stack, 1, 1, 14, 14)
        # self.stack.setMinimumSize(620,600)
        ################################# QSS ##################################
        self.stack.setStyleSheet('QWidget{background-color: rgb(0,0,0,10)}')
        # --------------------函数调用------------------------------------------#
        # 创建欢迎控件和函数
        self.stack1 = QWidget()
        self.stack1UI()
        self.stack.addWidget(self.stack1)
        # --------------------信号槽设置------------------------------------------#
        # 实现登录交互
        self.avatar.clicked.connect(lambda: self.click_login_up())
        # 关闭主窗体
        # self.bara.PB_close.clicked.connect(QApplication.instance().quit)

    def center(self):  # 设置窗口居中
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())



    # ----------------右边页面的类-------------#
    # __________________Welcome___________________#
    # Welcome
    def stack1UI(self):
        # 水平布局
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        # 提示文字
        self.text_1 = QLabel('Welcome！', self)
        self.text_2 = QLabel('欢迎使用Jarvis For Chat', self)
        self.text_3 = QLabel('开启你的数据之旅', self)
        # 检测按钮
        self.pushButton = QPushButton(self)
        self.pushButton.setText("立即登录")  # text
        self.pushButton.setShortcut('Enter')  # shortcut key
        self.pushButton.setToolTip("立即登录")  # Tool tip
        # 间隔区
        self.spacer_1 = QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spacer_3 = QtWidgets.QSpacerItem(10, 30, QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Expanding)
        ##点击信号与槽函数进行连接，这一步实现：在控制台输出被点击的按钮
        self.pushButton.clicked.connect(lambda: self.whichbtn(self.pushButton))
        # 实现登录交互
        self.pushButton.clicked.connect(lambda: self.click_login_up())
        # 添加控件
        self.layout.addItem(self.spacer_1)
        self.layout.addWidget(self.text_1, 0, QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.text_2, 0, QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton, 0, QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.text_3, 0, QtCore.Qt.AlignHCenter)
        self.layout.addItem(self.spacer_3)
        # 设置布局
        self.stack1.setLayout(self.layout)
        ################################# QSS ##################################
        self.text_1.setStyleSheet('QLabel{background-color:rgb(0,0,0,0);font-family:微软雅黑;font-size:30px;font-weight:bold;}')
        self.text_2.setStyleSheet('QLabel{background-color:rgb(0,0,0,0);font-family:微软雅黑;font-size:20px;font-weight:bold;}')
        self.text_3.setStyleSheet('QLabel{background-color:rgb(0,0,0,0);font-family:微软雅黑;font-size:20px;font-weight:bold;}')
        self.pushButton.setStyleSheet('QPushButton{background-color:rgb(255,255,255);border:2px solid #000000;border-radius:10px;'
                                      'font-family:微软雅黑;font-size:20px;font-weight:normal;}')
        # self.pushButton.setContentsMargins(10,10,10,10)

    def click_login_up(self):
        """
        打开登录窗口
        """
        from my_login_py import LoginLogic
        login = LoginLogic()
        login.show()
        # check_login_window(login)

    def check_login_window(self,login):
        if not login.isVisible():#主窗口关闭时
            self.hide()

    def whichbtn(self, btn):
        # 输出被点击的按钮
        print('clicked button is ' + btn.text())

    # __________________Welcome___________________#

    def display(self, i):
        # 设置当前可见的选项卡的索引
        self.stack.setCurrentIndex(i)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Main_Window()
    demo.show()
    sys.exit(app.exec_())
