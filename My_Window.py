import sys
from PyQt5 import QtWidgets, QtCore,QtGui
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

        ################################# QSS ##################################
        self.setStyleSheet('QWidget{background-color: rgb(255,255,255)}')
        self.LeftTabWidget.setStyleSheet('QWidget{background-color: rgb(228,228,228,90)}')
        self.avatar.setStyleSheet('QPushButton{border:0px;background-color:rgb(228,228,228,90)}')
        # --------------------------右边页面-------------------------------------------#
        # 在QStackedWidget对象中填充了4个子控件
        self.stack = QStackedWidget(self)
        self.right_layout = QGridLayout()
        self.stack.setLayout(self.right_layout)
        self.main_layout.addWidget(self.stack, 1, 1, 14, 14)
        ################################# QSS ##################################
        self.stack.setStyleSheet('QWidget{background-color: rgb(0,0,0,10)}')

        # 创建4个小控件和函数
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()
        self.stack1UI(groupname_list)
        self.stack2UI(groupname_list)
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
        self.group = GroupLogic(groupname_list)
        """水平布局"""
        self.layout_1 = QHBoxLayout()
        self.layout_1.setContentsMargins(0, 0, 0, 0)
        """左侧显示框"""
        self.W_left_1 = QtWidgets.QWidget()
        # 垂直布局
        self.W_left_1.setLayout(self.group.mid_init())
        """右侧群组列表"""
        self.group.create_element(groupname_list)
        """加入主体"""
        self.layout_1.addWidget(self.W_left_1)
        self.layout_1.addWidget(self.group)
        self.stack1.setLayout(self.layout_1)

    # 关键词提醒
    def stack2UI(self, groupname_list):
        pass
        # 数据库操作,获取当前用户名+微信号的已有关键词列表keyword_list
        keyword_list = getkeywords()
        # """测试专用"""
        # keyword_list=["@全体成员","柯逍","beta版"]
        ######对对，初始化的时候要调用一次，但是后续具体弄得时候还得再调用，别忘了#########################
        self.keyword_face = KeywordLogic(keyword_list, groupname_list)  # 左侧关键词生成
        """水平布局"""
        self.layout_2 = QGridLayout()
        self.layout_2.setContentsMargins(0, 0, 0, 0)
        """加入主体"""
        self.layout_2.addWidget(self.keyword_face)
        self.stack2.setLayout(self.layout_2)

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

from scroll import Group_Form
class GroupLogic(QFrame, Group_Form):
    """
    属于：热词分析
    用途：动态生成群聊列表
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
        self.W_left_layout_1 = QVBoxLayout()
        self.W_left_layout_1.setContentsMargins(0, 0, 0, 0)
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
        self.W_left_layout_1.addWidget(self.l4)  # , 0, QtCore.Qt.AlignHCenter
        self.W_left_layout_1.addWidget(self.l1, 0, QtCore.Qt.AlignHCenter)
        self.W_left_layout_1.addWidget(self.l2, 0, QtCore.Qt.AlignHCenter)
        self.W_left_layout_1.addWidget(self.l3, 0, QtCore.Qt.AlignHCenter)
        self.W_left_layout_1.addWidget(self.l5)
        ################################# QSS ##################################
        self.l1.setStyleSheet('QLabel{background-color:rgb(0,0,0,0);}')
        self.l2.setStyleSheet('QLabel{background-color:rgb(0,0,0,0);font-family:微软雅黑;font-size:20px;font-weight:bold;}')
        self.l3.setStyleSheet('QLabel{background-color:rgb(0,0,0,0);font-family:微软雅黑;font-size:20px;font-weight:bold;}')
        self.l4.setStyleSheet('QLabel{background-color:rgb(0,0,0,0);}')
        self.l5.setStyleSheet('QLabel{background-color:rgb(0,0,0,0);}')
        return self.W_left_layout_1

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
        self.W_left_layout_1.addWidget(self.l1)
        # print("over")

    def searchgroup(self):
        """
        搜索框搜索指定群组，并显示
        :return:
        """
        pass




from keywords import Keyword_Form
class KeywordLogic(QFrame, Keyword_Form ):
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



    """左self.verticalLayout右self.groupkey两个页面应该要事先设定好最大、最小值，再扔进self.horizontalLayout"""
    """我想实现点击空白部分，群聊消失，这部分应该设置为实时监听，不然只会调用一次"""
    def init_keyword(self, keyword_list):
        """
        生成初始关键词列表
        关键词用按钮生成
        选中高亮
        :return:
        """
        for item in range(len(keyword_list)):
            self.PB_keyword = QtWidgets.QPushButton()
            # self.PB_keyword.setMinimumSize(QtCore.QSize(200, 0))
            # self.PB_keyword.setMaximumSize(QtCore.QSize(200, 0))
            self.PB_keyword.setText(str(keyword_list[item])) # 显示
            self.PB_keyword.setObjectName(str(keyword_list[item])) # 类型名
            self.gridLayout.addWidget(self.PB_keyword, item / 3, item % 3, 1, 1)  #
            # 点击信号与槽函数进行连接，这一步实现：获取被点击的按钮的text
            self.PB_keyword.clicked.connect(lambda: self.select_scope(self.sender().text()))
            # 右键删除关键词
            self.PB_keyword.setContextMenuPolicy(Qt.CustomContextMenu)
            self.PB_keyword.customContextMenuRequested[QtCore.QPoint].connect(lambda :self.showcontextmenu(self.sender().text()))  # 右键点击时显示
            self.contextMenu = QtWidgets.QMenu(self)
            self.action = self.contextMenu.addAction("删除")
            self.action.triggered.connect(lambda: self.rightdelet(self.PB_clicked))
        self.SA_keyword.setContentsMargins(0, 0, 0, 0)

    def showcontextmenu(self,PB_name):
        self.PB_clicked=PB_name
        self.contextMenu.show()
        self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def rightdelet(self, oname):
        try:
            self.findChild(QPushButton,oname).close()  # 尝试删除关键词
            # 数据库操作，删除关键词
            try:
                # 数据库操作，获取用户ID和微信ID
                uidwid = db.getUseridAndWxidWithLogStatus()
                #  数据库操作，删除关键词
                if db.deleteKeyword(uidwid[0],uidwid[1],oname):
                    print("Delete keyword success")
            except:
                print("db for delete keyword error")
            self.closegroup()  # 尝试删除群聊列表
            # 数据库操作，获取当前关键词列表
            keyword_list = db.getkeywords()
            # """测试专用"""
            # keyword_list=["right","delet"]
            self.init_keyword(keyword_list)  # 重新生成关键词列表
        except:
            print("No such button")

    def add_keyword(self):
        """
         添加新生成的关键词
        :return:
        """
        # 数据库操作：在创建一个新的关键字的时候，要求自动将所有群聊标为未选
        print("enter")
        keyword = self.LE_edit.text()
        print(keyword)
        self.PB_keyword = QtWidgets.QPushButton()
        # self.PB_keyword.setMaximumSize(QtCore.QSize(200, 0))
        self.PB_keyword.setText(str(keyword))
        self.PB_keyword.setObjectName(keyword)
        # 数据库操作，再获取一次keyword_list
        keyword_list = db.getkeywords()
        # """测试专用"""
        # keyword_list=["add","keyword","third"]
        self.gridLayout.addWidget(self.PB_keyword, len(keyword_list) / 3, len(keyword_list) % 3, 1, 1) #
        try:
            # 数据库操作，获取用户ID和微信ID
            uidwid = db.getUseridAndWxidWithLogStatus()
            # 数据库操作，插入新关键词并初始化所有群聊为0
            if db.setKeywords_0(uidwid[0],uidwid[1],keyword,self.grouplist):
                print("ADD MEW KEYWORD SUCCESS")
        except:
            print("ADD MEW KEYWORD FALSE")
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
            if self.findChild(QScrollArea,"SA_group"):
                self.groupkey.close()
        except:
            print("select_scope error")
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
            print("closegroup error")

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
            groupname_list = db.keyWordGroupStatus(uidwid[0], uidwid[1], self.keyword)  # 包含字典的list
        except:
            print("db in create_element error")
        self.topFiller = QtWidgets.QWidget()
        self.topFiller.setContentsMargins(0, 0, 0, 0)
        # """测试专用"""
        # groupname_list=[("create",1),("element",0)]
        for item in range(len(groupname_list)):
            self.CB_group = QtWidgets.QCheckBox(self.topFiller)
            self.CB_group.resize(270, 60)
            self.CB_group.setText(str(groupname_list[item][0]))
            if groupname_list[item][1]:
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
                    utils_wxpy.updatekey(parent_conn)  # 通知，作用域改变
                self.diasuccess()   # 用户可见
                print("DB INSTER SUCCESS")  # 调试方便
            except:
                print("DB INSTER ERROR")

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
        self.setWindowFlags(Qt.FramelessWindowHint) # 去边框
        # 定时
        timer = QTimer(self)
        timer.timeout.connect(self.close)
        timer.start(3000)


# ---------------主函数------------------------#

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
    if recv == 'success':
        print('[+]bot创建成功')
    # 登录失败
    elif recv == 'fail':
        print('[-]bot创建失败 即将退出')
        exit(0)
    # 向子进程请求获得群聊名称 参数为(管道中父进程的一端)
    groupnames = utils_wxpy.getGroupnames(parent_conn)
    print('[+]创建窗口中...')
    # 初始化功能页面 传入的参数为[群聊名称列表]
    demo = Main_Window(groupnames)
    # demo.LeftTabWidget.currentRowChanged.connect(s.handle_click)
    demo.close_signal.connect(demo.close)
    # 功能页面显示
    demo.show()
    # 安全退出
    sys.exit(app.exec_())
