import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame
from multiprocessing import Pipe, Process
import database as db
import time
import utils_analyse
import utils_wxpy

# 创建用于父子进程通信的管道
child_conn, parent_conn = Pipe()


class Main_Window(QWidget):
    close_signal = pyqtSignal()

    def __init__(self, groupname_list, friendname_list, parent=None):
        # --------------------------主窗体--------------------------------------#
        super(Main_Window, self).__init__(parent)
        self.resize(1000, 650)  # 设置窗口初始位置和大小
        self.center()  # 设置窗口居中
        self.setWindowTitle('Jarvis For Chat')  # 设置窗口标题
        logo = QIcon()  # 设置窗口logo
        logo.addPixmap(QPixmap("./images/Dicon-p.png"), QIcon.Normal)
        self.setWindowIcon(logo)

        # 主窗网格布局，基底
        self.main_layout = QGridLayout(self, spacing=0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        # ------------------------左边菜单栏--------------------------------------#
        self.left_tab_widget = QListWidget()
        self.left_tab_widget.setFixedWidth(180)
        self.left_tab_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.left_tab_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.left_tab_widget.setFrameShape(QListWidget.NoFrame)
        # 左侧组件设置
        self.left_layout = QVBoxLayout()
        self.left_tab_widget.setLayout(self.left_layout)  # 将左侧布局（垂直）绑定到左侧组件上
        # 左侧布局
        self.main_layout.addWidget(self.left_tab_widget, 5, 0)
        self.left_tab_widget.currentRowChanged.connect(self.display)  # 绑定
        # stack功能列表名称#
        list_str = ['热词分析', '关键词提醒', '群发助手', '单项好友删除']
        for i in range(4):
            self.item = QListWidgetItem(list_str[i], self.left_tab_widget)  # 左侧选项的添加
            self.item.setSizeHint(QSize(180, 80))
            self.item.setTextAlignment(Qt.AlignCenter)  # 居中显示
        # --------------------左侧菜单栏头像------------------------------------------#
        self.avatar_layout = QGridLayout()
        self.main_layout.addLayout(self.avatar_layout, 1, 0)
        self.avatar = QtWidgets.QPushButton()
        self.avatar.setFixedSize(QSize(180, 180))
        self.avatar.setIcon(QIcon(r'Resource/images/avatar1.png'))
        self.avatar.setIconSize(QSize(170, 170))
        self.exit_button = QtWidgets.QPushButton()
        self.exit_button.setFixedSize(QSize(180, 20))
        self.exit_button.setText('退出登录')

        self.exit_button.clicked.connect(lambda: self.logoutEvent())

        self.avatar_layout.addWidget(self.avatar, 2, 0, 3, 3)  ##控件名，行，列，占用行数，占用列数，对齐方式###############################
        self.avatar_layout.addWidget(self.exit_button, 5, 0, 3, 3, QtCore.Qt.AlignHCenter)
        self.avatar_layout.setAlignment(self.avatar_layout, Qt.AlignRight)

        ################################# QSS ##################################
        self.setStyleSheet('QWidget{background-color: rgb(255,255,255)}')
        self.left_tab_widget.setStyleSheet('QWidget{background-color: rgb(228,228,228,90)}')
        self.avatar.setStyleSheet('QPushButton{border:0px;background-color:rgb(228,228,228,90)}')
        self.exit_button.setStyleSheet('QPushButton{border:0px;background-color:rgb(108,228,228,90)}')
        # --------------------------右边页面-------------------------------------------#
        # 在QStackedWidget对象中填充了4个子控件
        self.stack = QStackedWidget(self)
        self.right_layout = QGridLayout()
        self.stack.setLayout(self.right_layout)
        self.main_layout.addWidget(self.stack, 1, 1, 5, 14)
        ################################# QSS ##################################
        self.stack.setStyleSheet('QWidget{background-color: rgb(0,0,0,10)}')

        # 创建4个小控件和函数
        self.stack1 = QWidget()  # 热词分析
        self.stack2 = QWidget()  # 关键词提醒
        self.stack3 = QWidget()  # 群发助手
        self.stack4 = QWidget()  # 单向好友检测
        self.setStack1UI(groupname_list)
        self.setStack2UI(groupname_list)
        self.setStack3UI(friendname_list)
        self.setStack4UI()
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)
        self.stack.addWidget(self.stack4)

    def logoutEvent(self):

        info=db.getUseridAndWxidWithLogStatus()
        db.statusChange_Logout(info[0])
        self.close()
        import os
        os.system('python Welcome_Window.py')
        pass

    # 设置窗口居中
    def center(self):
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())

    # ____________________热词分析_____________________#
    def setStack1UI(self, groupname_list):
        self.group = GroupLogic(groupname_list)
        """水平布局"""
        self.layout_s1 = QHBoxLayout()
        self.layout_s1.setContentsMargins(0, 0, 0, 0)
        """左侧显示框"""
        self.W_left = QtWidgets.QWidget()
        # 垂直布局
        self.W_left.setLayout(self.group.mid_init())
        """右侧群组列表"""
        self.group.create_element(groupname_list)
        """加入主体"""
        self.layout_s1.addWidget(self.W_left)
        self.layout_s1.addWidget(self.group)

        # 设置布局
        self.stack1.setLayout(self.layout_s1)

    # ____________________热词分析_____________________#

    # ___________________关键词提醒_____________________#
    def setStack2UI(self, groupname_list):
        try:
            # 数据库操作，获取用户ID和微信ID
            uidwid = db.getUseridAndWxidWithLogStatus()
            keyword_list = db.getUserKeyword(uidwid[0], uidwid[1])
            self.keyword_face = KeywordLogic(keyword_list, groupname_list)  # 左侧关键词生成
        except:
            print("stack2UI: error")
        """水平布局"""
        self.layout_2 = QGridLayout()
        self.layout_2.setContentsMargins(0, 0, 0, 0)
        """加入主体"""
        self.layout_2.addWidget(self.keyword_face)
        self.stack2.setLayout(self.layout_2)

    # ___________________关键词提醒_____________________#

    # ____________________群发助手_____________________#
    def setStack3UI(self, friendname_list):
        self.groupfriends = FriendListLogic(friendname_list)
        """水平布局"""
        self.layout_s3 = QHBoxLayout()
        self.layout_s3.setContentsMargins(0, 0, 0, 0)
        """左侧显示框"""
        self.G_left = QtWidgets.QWidget()
        """右侧群组列表"""
        friends_sending_dict = self.groupfriends.createFriendListElement(friendname_list)
        # 垂直布局
        self.G_left.setLayout(self.groupfriends.groupSendingInit(friends_sending_dict))
        """加入主体"""
        self.layout_s3.addWidget(self.G_left)
        self.layout_s3.addWidget(self.groupfriends)

        # 设置布局
        self.stack3.setLayout(self.layout_s3)

    # ____________________群发助手_____________________#

    # __________________单向好友检测___________________#
    def setStack4UI(self):
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
        self.warning_text_41 = QLabel('该功能有可能导致您的网页版微信被暂时封号！', self)
        self.warning_text_42 = QLabel()
        self.warning_text_42.setText(
            "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">请慎重使用!!!!!</span></p></body></html>")
        self.instructions_41 = QLabel('点击【开始检测】→扫描弹出的二维码登录您的微信→耐心等待几分钟', self)
        self.instructions_42 = QLabel('即可在手机端确认您的单向好友！', self)

        # 检测按钮
        self.test_button_41 = QPushButton(self)
        self.test_button_41.setIcon(QIcon(QPixmap('Resource/images/one-way-friend/button.png')))  # icon
        self.test_button_41.setText("开始检测")  # text

        # 间隔区
        self.spacer_41 = QtWidgets.QSpacerItem(10, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spacer_42 = QtWidgets.QSpacerItem(10, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        # 点击信号与槽函数进行连接，这一步实现：在控制台输出被点击的按钮
        self.test_button_41.clicked.connect(lambda: self.printWhichButton(self.test_button_41))

        # 实现单向好友检测
        self.test_button_41.clicked.connect(lambda: self.clickTestSingleFriend(self.instructions_42))
        self.test_button_41.setToolTip("点击开始检测")  # Tool tip

        # 添加控件
        self.layout_s4.addItem(self.spacer_41)
        self.layout_s4.addWidget(self.logo_1abel_4, 0, QtCore.Qt.AlignHCenter)
        self.layout_s4.addWidget(self.warning_text_41, 0, QtCore.Qt.AlignHCenter)
        self.layout_s4.addWidget(self.warning_text_42, 0, QtCore.Qt.AlignHCenter)
        self.layout_s4.addWidget(self.instructions_41, 0, QtCore.Qt.AlignHCenter)
        self.layout_s4.addWidget(self.instructions_42, 0, QtCore.Qt.AlignHCenter)
        self.layout_s4.addWidget(self.test_button_41, 0, QtCore.Qt.AlignHCenter)
        self.layout_s4.addItem(self.spacer_42)

        # 设置布局
        self.stack4.setLayout(self.layout_s4)

    def clickTestSingleFriend(self, btn):
        # 调用后端的单向好友检测函数#
        utils_wxpy.singleFriendTest(parent_conn)
        # btn.setText("检测完成！请到手机端微信确认您的单向好友")

    # __________________单向好友检测___________________#

    def printWhichButton(self, btn):
        # 在控制台输出被点击的按钮#
        print('clicked button is ' + btn.text())

    def display(self, i):
        # 设置当前可见的选项卡的索引
        self.stack.setCurrentIndex(i)

    # 关闭事件#
    def closeEvent(self, event):
        utils_wxpy.killWxpyProcess(parent_conn)
        info=db.getUseridAndWxidWithLogStatus()
        db.statusChange_Logout(info[0])
        self.close()
        event.accept()


# ------------------右边页面的类---------------#


# __________________热词分析___________________#
from scroll import Group_Form


class GroupLogic(QFrame, Group_Form):
    """
    动态生成群聊列表的类
    """

    def __init__(self, groupname_list, parent=None):
        super(GroupLogic, self).__init__(parent)
        """初始化函数"""
        self.setupUi(self)
        self.retranslateUi(self)
        """初始化list"""
        self.data = ['a', 'b', 'c']
        """初始化列表"""
        # self.create_element()
        """初始化搜索框"""
        # self.LE_search.setTextMargins(0, 0, 0, 0)
        self.LE_search.setPlaceholderText("搜索")
        ################################# QSS ##################################
        self.setStyleSheet('QWidget{background-color: rgb(255,255,255,0)}'
                           'QLineEdit{background-color:rgb(255,255,255,100);border-radius:3px;border-width:0px;}'
                           'QScrollBar{width:2px;}'
                           'QPushButton{background-color: rgb(255,255,255,100);border:1px;}'
                           'QComboBox{border:0px;border-radius:3px;background: rgb(255,255,255,100);}'
                           'QComboBox:editable{background:rgb(255,255,255,100);}')

    def create_element(self, groupname_list):
        """
        给定参数，动态生成全部群组
        :return:
        """
        self.topFiller = QtWidgets.QWidget()
        self.topFiller.setContentsMargins(0, 0, 0, 0)
        for button in range(len(groupname_list)):
            self.PB_group = QtWidgets.QPushButton(self.topFiller)
            self.PB_group.resize(270, 60)
            self.PB_group.setText(str(groupname_list[button]))
            self.topFiller.setMinimumSize(0, (button + 1) * 60)
            self.PB_group.move(0, button * 61)
            # 点击信号与槽函数进行连接，这一步实现：获取被点击的按钮的text
            self.PB_group.clicked.connect(lambda: self.choose_group(self.sender().text()))
        self.SA_group.setWidget(self.topFiller)
        self.SA_group.setContentsMargins(0, 0, 0, 0)

    def choose_group(self, group_name):
        """
        获取群名及时间段，并传给后端
        """
        # 获取群名#
        # 获取时间段#
        from datetime import datetime, timedelta
        end_Time = datetime.now()
        # 根据选择按钮文本，获取start_Time
        time_Text = self.CBB_time.currentText()
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
        self.data.clear()
        self.data.insert(0, group_name)
        self.data.insert(1, start_Time_Int)
        self.data.insert(2, end_Time_Int)
        print(self.data)
        self.mid_dynamically()

    def mid_init(self):
        """
        初始的热词分析界面
        :return:
        """
        self.W_left_layout = QVBoxLayout()
        self.W_left_layout.setContentsMargins(0, 0, 0, 0)
        self.l1 = QLabel(self)  # 图片
        self.l1.setGeometry(0, 0, 540, 200)
        self.logo = QPixmap('./images/logo-p.png').scaled(self.l1.width(), self.l1.height())
        self.l1.setPixmap(self.logo)
        self.l2 = QLabel(self)
        self.l2.setText('请在右侧列表中选择你感兴趣的群组及时间段')
        self.l3 = QLabel(self)
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
        return self.W_left_layout

    def mid_dynamically(self):
        print("mid_dynamically come in")
        # 先把初始化的东西都删掉
        self.l4.close()
        self.l2.close()
        self.l3.close()
        self.l5.close()
        print("llll closed！")
        # -----------------------再插入词云--------------------------------#
        # 生成路径
        path = 'result/' + str(time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))) + '.jpg'
        print("path ok")
        #######################这句不能用#############################
        utils_analyse.getWordCloud('13038011192', '13038011192', self.data[0], self.data[1],
                                   self.data[2], path, image_mask_path='map.png')
        print(path)
        self.l1.setGeometry(0, 0, 540, 455)
        self.worldcloud = QPixmap(path).scaled(self.l1.width(), self.l1.height())
        self.l1.setPixmap(self.worldcloud)
        self.l1.setStyleSheet('background: rgb(255,255,255)')
        self.W_left_layout.addWidget(self.l1)
        # print("over")

    def searchgroup(self):
        """
        搜索框搜索指定群组，并显示
        :return:
        """
        pass


# __________________热词分析___________________#


# _________________关键词提醒___________________#
from keywords import Keyword_Form


class KeywordLogic(QFrame, Keyword_Form):
    """
    属于：关键词
    用途：生成关键词
    """

    def __init__(self, keyword_list, groupname_list, parent=None):
        super(KeywordLogic, self).__init__(parent)
        """初始化函数"""
        self.setupUi(self)
        self.retranslateUi(self)
        """初始化输入框"""
        self.LE_edit.setPlaceholderText("新建关键词")
        """初始化ACTION"""
        self.grouplist = groupname_list
        self.init_keyword(keyword_list)
        self.PB_add.clicked.connect(self.add_keyword)

    def init_keyword(self, keyword_list):
        """
        生成初始关键词列表
        关键词用按钮生成
        选中高亮
        :return:
        """
        for item in range(len(keyword_list)):
            PB_keyword = QtWidgets.QPushButton()
            PB_keyword.setText(keyword_list[item])  # 显示
            PB_keyword.setObjectName(keyword_list[item])  # 类型名
            self.gridLayout.addWidget(PB_keyword, item / 3, item % 3, 1, 1)
            # 点击信号与槽函数进行连接，这一步实现：获取被点击的按钮的text
            PB_keyword.clicked.connect(lambda: self.select_scope(self.sender().text()))
            # 右键删除关键词
            PB_keyword.setContextMenuPolicy(Qt.CustomContextMenu)
            PB_keyword.customContextMenuRequested[QtCore.QPoint].connect(
                lambda: self.showcontextmenu(self.sender().objectName()))  # 右键点击时显示
            self.contextMenu = QtWidgets.QMenu(self)
            self.action = self.contextMenu.addAction("删除")
            self.action.triggered.connect(lambda: self.rightdelet(self.PB_clicked))
        self.SA_keyword.setContentsMargins(0, 0, 0, 0)

    def showcontextmenu(self, PB_name):
        self.PB_clicked = PB_name
        self.contextMenu.show()
        self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def rightdelet(self, oname):
        # 先把界面上所有的关键词先删掉
        try:
            # 数据库操作，获取用户ID和微信ID
            uidwid = db.getUseridAndWxidWithLogStatus()
            # 数据库操作，获取当前关键词列表
            nowkeyword_list = db.getUserKeyword(uidwid[0], uidwid[1])
            for item in nowkeyword_list:
                self.findChild(QPushButton, item).deleteLater()
        except:
            print("rightdelet: deletkeyword_list error")
        # 再把数据库里的关键词删掉
        try:
            # 数据库操作，获取用户ID和微信ID
            uidwid = db.getUseridAndWxidWithLogStatus()
            #  数据库操作，删除关键词
            db.deleteKeyword(uidwid[0], uidwid[1], oname)
        except:
            print("rightdelet: db for delete keyword error")
        # 尝试关闭当前群聊列表
        self.closegroup()
        # 再重新生成一次关键词列表
        try:
            # 数据库操作，获取用户ID和微信ID
            uidwid = db.getUseridAndWxidWithLogStatus()
            # 数据库操作，获取当前关键词列表
            nowkeyword_list = db.getUserKeyword(uidwid[0], uidwid[1])
            self.init_keyword(nowkeyword_list)  # 重新生成关键词列表
        except:
            print("rightdelet: keyword_list error")


    def add_keyword(self):
        """
         添加新生成的关键词
         创建一个新的关键字的时候,要求自动将所有群聊标为未选
        :return:
        """
        keyword = self.LE_edit.text()
        self.LE_edit.setText("")
        self.PB_keyword = QtWidgets.QPushButton()
        self.PB_keyword.setText(str(keyword))
        self.PB_keyword.setObjectName(keyword)
        # 右键删除关键词
        self.PB_keyword.setContextMenuPolicy(Qt.CustomContextMenu)
        self.PB_keyword.customContextMenuRequested[QtCore.QPoint].connect(
            lambda: self.showcontextmenu(self.sender().text()))  # 右键点击时显示
        self.contextMenu = QtWidgets.QMenu(self)
        self.action = self.contextMenu.addAction("删除")
        self.action.triggered.connect(lambda: self.rightdelet(self.PB_clicked))
        try:
            # 数据库操作，获取用户ID和微信ID
            uidwid = db.getUseridAndWxidWithLogStatus()
            # 数据库操作，再获取一次keyword_list
            self.keyword_list = db.getUserKeyword(uidwid[0], uidwid[1])
        except:
            print("add_keyword: keyword_list error")
        try:
            # 数据库操作，获取用户ID和微信ID
            uidwid = db.getUseridAndWxidWithLogStatus()
            # 数据库操作，插入新关键词并初始化所有群聊为0
            if db.setKeywords_0(uidwid[0], uidwid[1], keyword, self.grouplist):
                print("add_keyword: ADD MEW KEYWORD SUCCESS")
            self.gridLayout.addWidget(self.PB_keyword, len(self.keyword_list) / 3, len(self.keyword_list) % 3, 1, 1)
        except:
            print("add_keyword: ADD MEW KEYWORD FALSE")
        # 点击信号与槽函数进行连接，这一步实现：获取被点击的按钮的text
        self.PB_keyword.clicked.connect(lambda: self.select_scope(self.sender().text()))

    def select_scope(self, keyword):
        """
        被链接：add_keyword 在生成新按钮时链接
        action：点击关键词按钮，出现群聊列表，并进行相关操作
        :param keyword:
        :return:
        """
        try:
            if self.findChild(QScrollArea, "SA_group"):
                self.groupkey.close()
        except:
            print("select_scope: error")
        self.groupkey = GkeywordLogic(keyword)
        self.horizontalLayout.addWidget(self.groupkey)

    def closegroup(self):
        """
        用途：关闭当前的群聊列表
        :return:
        """
        try:
            self.groupkey.close()
        except:
            print("closegroup: error")

    def mousePressEvent(self, event):
        """
        action：点击空白位置，群组列表消失
        :param event:
        :return:
        """
        if event.buttons() == QtCore.Qt.LeftButton:
            try:
                self.groupkey.close()
            except:
                print("mousePressEvent: not exit grouopkey")


"""注意切换关键词的时候，上一个的群聊列表要么清空，要么关闭"""
from scroll_keyword import Gkeyword_Form


class GkeywordLogic(QFrame, Gkeyword_Form):
    """
    属于：关键词
    用途：生成群聊列表
    区别：用QCheckBox实现群聊
    """

    def __init__(self, keyword, parent=None):
        super(GkeywordLogic, self).__init__(parent)
        """初始化函数"""
        self.setupUi(self)
        self.retranslateUi(self)
        """初始化变量"""
        self.keyword = keyword
        self.groupschange = []
        """初始化搜索框"""
        self.LE_search.setPlaceholderText("搜索")
        """初始化ACTION"""
        self.create_element()
        self.PB_confirmgroup.clicked.connect(self.confirmgroup)
        ################################# QSS ##################################
        self.setStyleSheet('QWidget{background-color: rgb(255,255,255,0)}'
                           'QLineEdit{background-color:rgb(255,255,255,100);border-radius:3px;border-width:0px;}'
                           'QScrollBar{width:2px;}'
                           'QPushButton{background-color: rgb(255,255,255,100);border:1px;}'
                           'QComboBox{border:0px;border-radius:3px;background: rgb(255,255,255,100);}')

    def create_element(self):
        """
        给定参数，动态生成全部群组
        :return:
        """
        # 数据库操作：根据关键字返回的群聊+状态，checkbox置选中或未选中
        """ 不行，我还是需要一个能将所有群聊都返回的函数，李翔你就认命吧 """
        try:
            # 数据库操作，获取用户ID和微信ID
            uidwid = db.getUseridAndWxidWithLogStatus()
            # 数据库操作，获取关键词的历史作用群聊
            self.groupwithstatulist = db.keyWordGroupStatus(uidwid[0], uidwid[1], self.keyword)  # 包含字典的list
        except:
            print("create_element: db in create_element error")
        self.topFiller = QtWidgets.QWidget()
        self.topFiller.setContentsMargins(0, 0, 0, 0)
        # """测试专用"""
        # groupname_list=[("create",1),("element",0)]
        for item in range(len(self.groupwithstatulist)):
            self.CB_group = QtWidgets.QCheckBox(self.topFiller)
            self.CB_group.resize(270, 60)
            self.CB_group.setText(str(self.groupwithstatulist[item][0]))
            if self.groupwithstatulist[item][1]:
                self.CB_group.setChecked(True)  # 存在即选中
            self.topFiller.setMinimumSize(0, (item + 1) * 60)
            self.CB_group.move(0, item * 61)
        self.SA_group.setWidget(self.topFiller)
        self.SA_group.setContentsMargins(0, 0, 0, 0)

    def confirmgroup(self):
        """
        一次性发送消息给数据库
        :return:
        """
        allgroup = self.findChildren(QCheckBox)
        for item in allgroup:
            if item.isChecked() == True:
                self.groupschange.append(item.text())
            try:
                # 数据库操作，获取用户ID和微信ID
                uidwid = db.getUseridAndWxidWithLogStatus()
                # 数据库操作,修改关键词作用的群聊
                if db.setKeywords_1(uidwid[0], uidwid[1], self.keyword, self.groupschange):
                    # utils_wxpy.updatekey(parent_conn)  # 通知，作用域改变 ############################################张扬
                    self.diasuccess()  # 用户可见
                    print("confirmgroup: DB INSTER SUCCESS")  # 调试方便
            except:
                print("confirmgroup: DB INSTER ERROR")

    def diasuccess(self):
        """
        类别：弹窗
        作用：确认数据设置成功
        操作：2秒自动关闭
        :return:
        """
        self.dialog = Success_Dialog()
        self.dialog.show()


from untitled import Ui_Dialog


class Success_Dialog(QDialog, Ui_Dialog):
    """
    关键词对应群聊设置成功的提示框
    """

    def __init__(self, parent=None):
        super(Success_Dialog, self).__init__(parent)
        """初始化"""
        self.setupUi(self)
        self.retranslateUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去边框
        # 定时
        timer = QTimer(self)
        timer.timeout.connect(self.close)
        timer.start(3000)
        
# _________________关键词提醒___________________#


# __________________群发助手___________________#
from scroll_friendslist import FriendList_Ui


class FriendListLogic(QFrame, FriendList_Ui):
    """
    动态生成群发功能右侧好友列表的类
    """

    def __init__(self, friendname_list, parent=None):
        super(FriendListLogic, self).__init__(parent)
        """初始化函数"""
        self.setupUi(self)
        ################################# QSS ##################################
        self.setStyleSheet('QWidget{background-color: rgb(255,255,255,0)}'
                           'QLineEdit{background-color:rgb(255,255,255,100);border-radius:3px;border-width:0px;}'
                           'QScrollBar{width:2px;}'
                           'QPushButton{background-color: rgb(255,255,255,100);border:1px;}'
                           'QComboBox{border:0px;border-radius:3px;background: rgb(255,255,255,100);}'
                           'QComboBox:editable{background:rgb(255,255,255,100);}')

    def groupSendingInit(self, friends_sending_dict):
        """
        函数：群发功能-群发内容设置界面的初始化函数
        返回值：self.G_left_layout
        :return:
        """
        self.G_left_layout = QGridLayout()

        # 输入文本框
        self.textbox = QtWidgets.QTextEdit(self)
        self.textbox.setGeometry(QtCore.QRect(30, 30, 321, 192))
        # 确认群发按钮
        self.confirm_group_button = QtWidgets.QPushButton()
        self.confirm_group_button.setGeometry(QtCore.QRect(410, 110, 75, 23))
        self.confirm_group_button.setObjectName("confirm_group_button")
        self.confirm_group_button.setText("确认群发")

        # 使用提示
        self.user_instructions = QtWidgets.QLabel()
        self.user_instructions.setGeometry(QtCore.QRect(370, 160, 151, 81))
        self.user_instructions.setObjectName("user_instructions")
        self.user_instructions.setText(
            "<html><head/><body><p align=\"center\">群发模板编辑完毕后</p><p align=\"center\">请在右侧选择群发对象~</p><p align=\"center\">并点击确认群发</p></body></html>")

        # 祝福模板按钮#
        self.blessing_temp_1 = QtWidgets.QPushButton()
        self.blessing_temp_1.setGeometry(QtCore.QRect(30, 280, 150, 100))
        self.blessing_temp_1.setObjectName("blessing_temp_1")
        self.blessing_temp_2 = QtWidgets.QPushButton()
        self.blessing_temp_2.setGeometry(QtCore.QRect(200, 280, 150, 101))
        self.blessing_temp_2.setObjectName("blessing_temp_2")
        self.blessing_temp_3 = QtWidgets.QPushButton()
        self.blessing_temp_3.setGeometry(QtCore.QRect(370, 280, 150, 100))
        self.blessing_temp_3.setObjectName("blessing_temp_3")
        self.blessing_temp_4 = QtWidgets.QPushButton()
        self.blessing_temp_4.setGeometry(QtCore.QRect(30, 410, 150, 100))
        self.blessing_temp_4.setObjectName("blessing_temp_4")
        self.blessing_temp_5 = QtWidgets.QPushButton()
        self.blessing_temp_5.setGeometry(QtCore.QRect(200, 410, 150, 100))
        self.blessing_temp_5.setObjectName("blessing_temp_5")
        self.blessing_temp_6 = QtWidgets.QPushButton()
        self.blessing_temp_6.setGeometry(QtCore.QRect(370, 410, 150, 100))
        self.blessing_temp_6.setObjectName("blessing_temp_6")
        # 设置祝福模板文字
        self.blessing_temp_1.setText("#XX#，圣诞节快乐！")
        self.blessing_temp_2.setText("#XX#，元旦节快乐！")
        self.blessing_temp_3.setText("#XX#，新年快乐！")
        self.blessing_temp_4.setText("#XX#，平安夜快乐！")
        self.blessing_temp_5.setText("#XX#，元宵节快乐！")
        self.blessing_temp_6.setText("#XX#，反正祝你快乐！")

        # 点击信号与槽函数进行连接，这一步实现：获取被点击的按钮的text
        self.blessing_temp_1.clicked.connect(lambda: self.choose_template(self.sender().text()))
        self.blessing_temp_2.clicked.connect(lambda: self.choose_template(self.sender().text()))
        self.blessing_temp_3.clicked.connect(lambda: self.choose_template(self.sender().text()))
        self.blessing_temp_4.clicked.connect(lambda: self.choose_template(self.sender().text()))
        self.blessing_temp_5.clicked.connect(lambda: self.choose_template(self.sender().text()))
        self.blessing_temp_6.clicked.connect(lambda: self.choose_template(self.sender().text()))

        # 点击信号与槽函数进行连接，这一步实现：获取被点击的按钮的text
        self.confirm_group_button.clicked.connect(lambda: self.confirmButtonClick(friends_sending_dict))

        # 添加控件
        self.G_left_layout.addWidget(self.textbox, 0, 0, 3, 6)  ##控件名，行，列，占用行数，占用列数，对齐方式###############################
        self.G_left_layout.addWidget(self.confirm_group_button, 0, 7, 1, 1)
        self.G_left_layout.addWidget(self.user_instructions, 2, 7, 1, 1)
        self.G_left_layout.addWidget(self.blessing_temp_1, 4, 0, 2, 3)
        self.G_left_layout.addWidget(self.blessing_temp_2, 4, 3, 2, 3)
        self.G_left_layout.addWidget(self.blessing_temp_3, 4, 6, 2, 3)
        self.G_left_layout.addWidget(self.blessing_temp_4, 6, 0, 2, 3)
        self.G_left_layout.addWidget(self.blessing_temp_5, 6, 3, 2, 3)
        self.G_left_layout.addWidget(self.blessing_temp_6, 6, 6, 2, 3)
        ################################# QSS ##################################
        return self.G_left_layout

    def confirmButtonClick(self, friends_sending_dict):
        '''
        函数：确定群发按钮的响应事件函数
        功能逻辑：获取群发内容并检查文本格式正确性
                （1）若格式正确，向后端传递参数，进行群发，并弹窗提示用户群发成功
                （2）否则，弹窗提示用户重新编辑群发内容
        '''
        textboxValue = self.textbox.toPlainText()  # 获取文本框内容
        # 检查输入格式是否正确
        if (self.testInputRight(textboxValue)):
            self.textbox.setPlainText('')  # 输入格式正确，清空文本框
            self.groupSending(textboxValue, friends_sending_dict)  # 给后端群发函数传递参数
            self.groupsendSuccessDialog()  # 发出【群发成功】提示信息
        else:
            self.inputErrorDialog()  # 输入格式错误，发出【输入格式错误】提示信息

    def groupSending(self, textmodel, friends_sending_dict):
        '''与后端连接，调用后端群发接口'''
        print('[!]调用后端群发接口...')
        friends_name_list = []
        for choose_name, choose_state in friends_sending_dict.items():
            if (choose_state == 1):
                friends_name_list.append(choose_name)
        print('[群发内容]：', textmodel)
        print('[群发对象]：', friends_name_list)
        # 调用群发语句，待增加......
        # groupsend(textmodel,friends_name_list)
        utils_wxpy.groupSend(parent_conn, textmodel, friends_name_list)

    def testInputRight(self, textboxValue):
        '''
        函数：判断文本输入格式是否正确
        返回值：bool
        功能逻辑：检查输入文本中的#个数
                （1）若个数为0个或2个，格式正确，返回True
                （2）否则，输入格式错误，返回False
        '''
        number_jinghao = 0  # 井号个数统计
        for iword in textboxValue:
            if (iword == '#'):
                number_jinghao = number_jinghao + 1
        if ((number_jinghao == 0) or (number_jinghao == 2)):
            # 井号只能为0个或2个
            return True
        else:
            return False

    def createFriendListElement(self, friendname_list):
        """
        函数：给定参数，动态生成【好友列表】
        返回值：friends_sending_dict{ 好友名，选择状态 }
        :return:
        """
        friends_sending_dict = {}
        self.topFiller = QtWidgets.QWidget()
        self.topFiller.setContentsMargins(0, 0, 0, 0)
        for button in range(len(friendname_list)):
            self.PB_group = QtWidgets.QCheckBox(self.topFiller)
            self.PB_group.resize(270, 60)
            self.PB_group.setText(str(friendname_list[button]))
            friends_sending_dict[str(friendname_list[button])] = 0  # 插入字典
            self.topFiller.setMinimumSize(0, (button + 1) * 60)
            self.PB_group.move(0, button * 61)
            # 点击信号与槽函数进行连接，这一步实现：获取被点击的按钮的text
            self.PB_group.clicked.connect(lambda: self.chooseFriends(friends_sending_dict))
        self.SA_group.setWidget(self.topFiller)
        self.SA_group.setContentsMargins(0, 0, 0, 0)
        return friends_sending_dict

    def choose_template(self, blessing_template):
        '''将输入框文本设置为群发祝福模板'''
        self.textbox.setPlainText(blessing_template)

    def chooseFriends(self, friends_sending_dict):
        """
        选择好友，根据用户点击修改dict的状态标志位
        """
        source = self.sender()
        friends_group_name = source.text()
        if (source.isChecked()):
            friends_sending_dict[friends_group_name] = 1
        else:
            friends_sending_dict[friends_group_name] = 0

    def groupsendSuccessDialog(self):
        """
        函数：群发成功提示弹窗
        操作：3秒自动关闭
        :return:
        """
        self.dialog = G_Success_Dialog()
        self.dialog.show()

    def inputErrorDialog(self):
        """
        函数：输入文本格式错误警告弹窗
        操作：3秒自动关闭
        :return:
        """
        self.dialog = G_Error_Dialog()
        self.dialog.show()


from groupsend_success_dialog import Ui_Groupsend_Success_Dialog


class G_Success_Dialog(QDialog, Ui_Groupsend_Success_Dialog):
    """
    群发成功的提示框
    """

    def __init__(self, parent=None):
        super(G_Success_Dialog, self).__init__(parent)
        """初始化"""
        self.setupUi(self)
        self.retranslateUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去边框
        # 定时
        timer = QTimer(self)
        timer.timeout.connect(self.close)
        timer.start(3000)


from input_error_dialog import Ui_Input_Error_Dialog


class G_Error_Dialog(QDialog, Ui_Input_Error_Dialog):
    """
    群发内容输入格式错误的提示框
    """

    def __init__(self, parent=None):
        super(G_Error_Dialog, self).__init__(parent)
        """初始化"""
        self.setupUi(self)
        self.retranslateUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去边框
        # 定时
        timer = QTimer(self)
        timer.timeout.connect(self.close)
        timer.start(3000)


# __________________群发助手___________________#


# --------------------主函数--------------------#
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 创建wxpy子进程
    # 传递的参数分别为(管道中子进程的一端) (userid) (微信id)  这里默认微信id与userid一致
    wxpy_process = Process(target=utils_wxpy.createWxpyProcess, args=(child_conn, '13038011192', '13038011192'))
    # 启动wxpy子进程
    wxpy_process.start()
    # 接受登录状态
    recv = parent_conn.recv()

    # 登陆成功
    if recv[0] == 'success':
        print('[+]bot创建成功')
        wxid = recv[1]  # 这里是由wxpy传递过来的wxid
    # 登录失败
    elif recv[1] == 'fail':
        print('[-]bot创建失败 即将退出')
        exit(0)

    # 向子进程请求获得群聊名称 参数为(管道中父进程的一端)
    groupnames = utils_wxpy.getGroupnames(parent_conn)
    # groupnames = ['我是群组1', '222', '333']
    friendnames = utils_wxpy.getFriendnames(parent_conn)
    print('[+]创建窗口中...')
    # 初始化功能页面 传入的参数为[群聊名称列表]
    demo = Main_Window(groupnames, friendnames)
    # demo.left_tab_widget.currentRowChanged.connect(s.handle_click)
    demo.close_signal.connect(demo.close)
    # 功能页面显示
    demo.show()
    # 安全退出
    sys.exit(app.exec_())
