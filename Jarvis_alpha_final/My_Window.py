import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFrame
from barabove_py import BarLogic
from scroll import Ui_Form as Group
from multiprocessing import Pipe, Process
import time
import utils_analyse

sys.path.append("..")

import utils_wxpy

child_conn, parent_conn = Pipe()


class Main_Window(QWidget):
    close_signal = pyqtSignal()

    def __init__(self, groupname_list, parent=None):
        # --------------------------主窗体--------------------------------------#
        super(Main_Window, self).__init__(parent)
        self.resize(1000, 650)  # 设置窗口初始位置和大小
        self.center()  # 设置窗口居中
        self.setWindowTitle('Jarvis For Chat')  # 设置窗口标题
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
        list_str = ['热点分析', '关键词提醒', '群发助手', '单项好友删除']
        for i in range(4):
            self.item = QListWidgetItem(list_str[i], self.LeftTabWidget)  # 左侧选项的添加
            self.item.setSizeHint(QSize(180, 80))
            self.item.setTextAlignment(Qt.AlignCenter)  # 居中显示
        # --------------------左侧菜单栏头像------------------------------------------#
        self.avatar_layout = QGridLayout()
        self.main_layout.addLayout(self.avatar_layout, 1, 0)
        self.avatar = QtWidgets.QPushButton()
        self.avatar.setFixedSize(QSize(180, 180))
        self.avatar.setIcon(QIcon(r'Resource/images/avatar1.png'))
        self.avatar.setIconSize(QSize(170, 170))
        self.avatar_layout.addWidget(self.avatar, 2, 0, 3, 3)  ##控件名，行，列，占用行数，占用列数，对齐方式###############################
        self.avatar_layout.setAlignment(self.avatar_layout, Qt.AlignRight)
        # self.weixin = QtWidgets.QPushButton()
        # self.weixin.setFixedSize(QSize(45, 45))
        # self.weixin.setIcon(QIcon(r'Resource/images/weixin1.png'))
        # self.avatar_layout.addWidget(self.weixin, 4, 4, 1, 1)
        # self.avatar_layout.setAlignment(self.weixin, Qt.AlignRight)
        # self.avatar_layout.setAlignment(self.weixin, Qt.AlignBottom)

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
        self.main_layout.addWidget(self.stack, 1, 1, 14, 14)  ################################# 我改了
        # self.stack.setMinimumSize(620,600)
        ################################# QSS ##################################
        self.stack.setStyleSheet('QWidget{background-color: rgb(0,0,0,10)}')

        # 创建4个小控件和函数
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()
        self.stack1UI(groupname_list)
        self.stack2UI()
        self.stack3UI()
        self.stack4UI()
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)
        self.stack.addWidget(self.stack4)


    def center(self):  # 设置窗口居中
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())

    # 热词分析
    def stack1UI(self, groupname_list):
        # 水平布局
        self.layout_s1 = QHBoxLayout()
        self.layout_s1.setContentsMargins(0, 0, 0, 0)
        """左侧显示框"""
        self.W_left = QtWidgets.QWidget()
        # 垂直布局
        self.W_left_layout = QVBoxLayout()
        self.W_left_layout.setContentsMargins(0, 0, 0, 0)
        self.mid_init()  # 生成初始界面
        self.W_left.setLayout(self.W_left_layout)
        """右侧群组列表"""
        from scroll_py import GroupLogic
        self.group = GroupLogic(groupname_list)
        self.create_element(groupname_list)
        # self.group.PB_group.clicked.connect(self.mid_dynamically)
        """加入主体"""
        self.layout_s1.addWidget(self.W_left)
        self.layout_s1.addWidget(self.group)
        self.stack1.setLayout(self.layout_s1)
        ################################# QSS ##################################
        # self.W_left.setStyleSheet('QWidget{background-color: rgb(228,228,228,10)}')

    def mid_init(self):
        """
        初始的热词分析界面
        :return:
        """
        # 图片
        self.l1 = QLabel(self)
        self.l1.setGeometry(0, 0, 540, 200)
        self.logo = QPixmap('./images/logo-p.png').scaled(self.l1.width(), self.l1.height())
        self.l1.setPixmap(self.logo)
        self.l2 = QLabel(self)
        self.l2.setText('请在右侧列表中选择你感兴趣的群组及时间段')
        self.l3 = QLabel( self)
        self.l3.setText('开启你的【热词分析】之旅~')
        # 间隔区
        self.l4 = QtWidgets.QLabel(self)
        self.l5 = QtWidgets.QLabel(self)
        # 添加控件
        self.W_left_layout.addWidget(self.l4)  # , 0, QtCore.Qt.AlignHCenter
        self.W_left_layout.addWidget(self.l1, 0, QtCore.Qt.AlignHCenter)
        self.W_left_layout.addWidget(self.l2, 0, QtCore.Qt.AlignHCenter)
        self.W_left_layout.addWidget(self.l3, 0, QtCore.Qt.AlignHCenter)
        self.W_left_layout.addWidget(self.l5)
        ################################# QSS ##################################
        self.l1.setStyleSheet('QLabel{background-color:rgb(0,0,0,0);}')
        self.l2.setStyleSheet('QLabel{background-color:rgb(0,0,0,0);font-family:微软雅黑;font-size:20px;font-weight:bold;}')
        self.l3.setStyleSheet('QLabel{background-color:rgb(0,0,0,0);font-family:微软雅黑;font-size:20px;font-weight:bold;}')
        self.l4.setStyleSheet('QLabel{background-color:rgb(0,0,0,0);}')
        self.l5.setStyleSheet('QLabel{background-color:rgb(0,0,0,0);}')


    def create_element(self, groupname_list):
        """
        给定参数，动态生成全部群组
        :return:
        """
        # import My_Window
        # groupnames=My_Window.get_groupnames()

        self.topFiller = QtWidgets.QWidget()
        self.topFiller.setContentsMargins(0, 0, 0, 0)
        for button in range(len(groupname_list)):
            self.PB_group = QtWidgets.QPushButton(self.topFiller)
            self.PB_group.resize(270, 60)
            # PNG_group=QtGui.QPixmap('./images/search.png')
            # self.PB_group.setIcon(QtGui.QIcon(r"./images/search.png"))
            # self.PB_group.setText(str(button))
            self.PB_group.setText(str(groupname_list[button]))
            self.topFiller.setMinimumSize(0, (button + 1) * 60)
            self.PB_group.move(0, button * 61)
            # 点击信号与槽函数进行连接，这一步实现：获取被点击的按钮的text
            self.PB_group.clicked.connect(lambda: self.choose_group(self.group.sender().text()))

        self.group.SA_group.setWidget(self.topFiller)
        self.group.SA_group.setContentsMargins(0, 0, 0, 0)

    def choose_group(self, group_name):
        """
        获取群名及时间段，并传给后端
        """
        # 获取群名#
        # 获取时间段#
        from datetime import datetime, timedelta
        end_Time = datetime.now()
        # 根据选择按钮文本，获取start_Time
        time_Text = self.group.CBB_time.currentText()
        if (time_Text == "过去6小时"):
            start_Time = end_Time - timedelta(hours=6)
        elif (time_Text == "过去24小时"):
            start_Time = end_Time - timedelta(hours=24)
        elif (time_Text == "过去三天"):
            start_Time = end_Time - timedelta(days=3)
        elif (time_Text == "过去一周"):
            start_Time = end_Time - timedelta(days=7)

        # 将时间转为int#
        start_Time_Int = int(start_Time.strftime("%Y%m%d%H%M%S"))
        end_Time_Int = int(end_Time.strftime("%Y%m%d%H%M%S"))
        self.group.data.clear()
        self.group.data.insert(0, group_name)
        self.group.data.insert(1, start_Time_Int)
        self.group.data.insert(2, end_Time_Int)
        print(self.group.data)
        self.mid_dynamically()

    def mid_dynamically(self):
        # 先把初始化的东西都删掉
        self.l4.close()
        self.l2.close()
        self.l3.close()
        self.l5.close()

        # -----------------------再插入词云--------------------------------#
        # 生成路径

        # path ="ciyun\\" + self.group.data[0] + "\\" + str(self.group.data[1]) + str(self.group.data[2]) + '.jpg'
        path = 'result/' + str(time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))) + '.jpg'
        # print(self.group.data[0]," ",self.group.data[1]," ",self.group.data[2]," ",path)
        utils_analyse.getWordCloud('13038011192', '13038011192', self.group.data[0], self.group.data[1],
                                   self.group.data[2], path, image_mask_path='map.png')
        print(path)
        self.l1.setGeometry(0, 0, 540, 455)
        # self.l1.setMidLineWidth(540)
        # self.l1.setFixedHeight(600)

        # self.worldcloud = QPixmap('./images/ciyun.jpg').scaled(self.l1.width(), self.l1.height())
        self.worldcloud = QPixmap(path).scaled(self.l1.width(), self.l1.height())
        self.l1.setPixmap(self.worldcloud)

        self.l1.setStyleSheet('background: rgb(255,255,255)')
        # self.l1.setMinimumSize(620, 640)
        # main_layout_3.addWidget(buntton)
        # self.l1.setScaledContents(True) # 自适应
        self.W_left_layout.addWidget(self.l1)
        # print("[3]flag")

    # 关键词提醒
    # --------未完工------------#
    def stack2UI(self):
        main_layout_2 = QGridLayout()
        main_layout_2.setContentsMargins(0, 0, 0, 0)
        # self.stack2.resize(620, 600)
        self.stack2.setLayout(main_layout_2)
        buntton = QPushButton('[关键词]功能正在紧张开发中balabal')
        # btn = QPushButton
        # btn.setFrameShape
        # buntton.setGeometry(0,300,100,40)
        # buntton.setStyleSheet('backgroud:rgb(33,33,33)'；)
        # buntton.setStyleSheet('background: rgb(19,60,85);')
        # buntton.setMinimumSize(620, 600)
        main_layout_2.addWidget(buntton)

    # 群发助手
    def stack3UI(self):
        main_layout_3 = QGridLayout()
        main_layout_3.setContentsMargins(0, 0, 0, 0)
        # self.stack2.resize(620, 600)
        self.stack3.setLayout(main_layout_3)
        buntton = QPushButton('[群发助手]功能正在紧张开发中balabal')
        # btn = QPushButton
        # btn.setFrameShape
        # buntton.setGeometry(0,300,100,40)
        # # buntton.setStyleSheet('backgroud:rgb(33,33,33)'；)
        # buntton.setStyleSheet('background: rgb(19,60,85)')
        # buntton.setMinimumSize(620, 650)
        main_layout_3.addWidget(buntton)

    # 单向好友检测
    def stack4UI(self):
        # 水平布局
        self.layout_s4 = QVBoxLayout()
        self.layout_s4.setContentsMargins(0, 0, 0, 0)

        # 图片
        self.logo_4 = QPixmap('Resource/images/one-way-friend/logo.png')
        self.logo_1abel_4 = QLabel(self)
        self.logo_1abel_4.setGeometry(0, 0, 150, 150)
        # lbl.setScaledContents (True)  # 让图片自适应label大小
        self.logo_1abel_4.setPixmap(self.logo_4)

        # 提示文字
        self.Warning1_4 = QLabel('该功能有可能导致您的网页版微信被暂时封号！', self)
        self.Warning2_4 = QLabel()
        self.Warning2_4.setText(
            "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">请慎重使用!!!!!</span></p></body></html>")
        self.l2_4 = QLabel('点击【开始检测】→扫描弹出的二维码登录您的微信→耐心等待几分钟', self)
        self.l3_4 = QLabel('即可在手机端确认您的单向好友！', self)

        # 检测按钮
        self.pushButton_4 = QPushButton(self)
        self.pushButton_4.setIcon(QIcon(QPixmap('Resource/images/one-way-friend/button.png')))  # icon
        self.pushButton_4.setText("开始检测")  # text
        # self.pushButton.setShortcut('Ctrl+D')#shortcut key

        # 间隔区
        self.spacer_1_4 = QtWidgets.QSpacerItem(10, 30, QtWidgets.QSizePolicy.Minimum,
                                                QtWidgets.QSizePolicy.Expanding)
        self.spacer_2_4 = QtWidgets.QSpacerItem(10, 30, QtWidgets.QSizePolicy.Minimum,
                                                QtWidgets.QSizePolicy.Expanding)

        # 点击信号与槽函数进行连接，这一步实现：在控制台输出被点击的按钮
        self.pushButton_4.clicked.connect(lambda: self.whichbtn(self.pushButton))

        # 实现单向好友检测
        self.pushButton_4.clicked.connect(lambda: self.click_Test_OneWayFriends(self.l2))
        self.pushButton_4.setToolTip("点击开始检测")  # Tool tip

        # 添加控件
        self.layout_s4.addItem(self.spacer_1_4)
        self.layout_s4.addWidget(self.logo_1abel_4, 0, QtCore.Qt.AlignHCenter)
        self.layout_s4.addWidget(self.Warning1_4, 0, QtCore.Qt.AlignHCenter)
        self.layout_s4.addWidget(self.Warning2_4, 0, QtCore.Qt.AlignHCenter)
        self.layout_s4.addWidget(self.l2_4, 0, QtCore.Qt.AlignHCenter)
        self.layout_s4.addWidget(self.l3_4, 0, QtCore.Qt.AlignHCenter)
        self.layout_s4.addWidget(self.pushButton_4, 0, QtCore.Qt.AlignHCenter)
        self.layout_s4.addItem(self.spacer_2_4)

        # 设置布局
        self.stack4.setLayout(self.layout_s4)

    def click_Test_OneWayFriends(self, btn):
        utils_wxpy.singleFriendTest(parent_conn)
        btn.setText("检测完成！请到手机端微信确认您的单向好友")

    def whichbtn(self, btn):
        # 输出被点击的按钮
        print('clicked button is ' + btn.text())

    # __________________单向好友检测___________________#

    def display(self, i):
        # 设置当前可见的选项卡的索引
        self.stack.setCurrentIndex(i)

    # 关闭事件#
    def closeEvent(self, event):
        utils_wxpy.killWxpyProcess(parent_conn)
        event.accept()


# ----------------右边页面的类-------------#


# ---------------主函数------------------------#

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # style = open(r"../Qss/MetroUI.qss", "r", encoding='utf-8')
    # style_str = style.read()
    # app.setStyleSheet(style_str)

    ###创建wxpy

    wxpy_process = Process(target=utils_wxpy.createWxpyProcess, args=(child_conn, '13038011192', '13038011192'))
    wxpy_process.start()

    recv = parent_conn.recv()
    if recv == 'success':
        print('[+]bot创建成功')
    elif recv == 'fail':
        print('[-]bot创建失败 即将退出')
        exit(0)

    groupnames = utils_wxpy.getGroupnames(parent_conn)

    ####test使用，正式功能请使用上一行
    groupnames = ['有趣', '2hhhh', '3hhhh']

    print('[+]创建窗口中...')

    demo = Main_Window(groupnames)

    # demo.LeftTabWidget.currentRowChanged.connect(s.handle_click)
    demo.close_signal.connect(demo.close)

    demo.show()

    sys.exit(app.exec_())
