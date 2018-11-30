import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from multiprocessing import Process

def singleFrinedTest(name, *args):
    import os
    os.system('python single_friend_test.py')

class Main_Window(QWidget):
    def __init__(self):
        # --------------------------主窗体--------------------------------------#
        super(Main_Window, self).__init__()
        # self.setGeometry(0, 0, 800, 600
        self.resize(800, 600)  # 设置窗口初始位置和大小
        self.center()  # 设置窗口居中
        self.setWindowTitle('Jarvis For Chat 主界面框架')  # 设置窗口标题
        # self.setWindowFlag(Qt.FramelessWindowHint)

        # 水平布局，添加部件到布局中
        self.main_layout = QHBoxLayout(self, spacing=0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        # ------------------------左边菜单栏--------------------------------------#
        self.LeftTabWidget = QListWidget()
        self.LeftTabWidget.setFixedWidth(180)
        # self.LeftTabWidget.setGeometry(0,40,180,1080)
        self.LeftTabWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.LeftTabWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.LeftTabWidget.setFrameShape(QListWidget.NoFrame)
        self.main_layout.addWidget(self.LeftTabWidget)

        list_str = ['热点分析', '关键词提醒', '群发助手', '单项好友删除']
        for i in range(4):
            self.item = QListWidgetItem(list_str[i], self.LeftTabWidget)  # 左侧选项的添加
            self.item.setSizeHint(QSize(180, 80))
            self.item.setTextAlignment(Qt.AlignCenter)  # 居中显示
        # --------------------------右边页面-------------------------------------------#
        # 创建4个小控件和函数
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()
        # self.stack1.setFrameShape(QListWidget.NoFrame)
        # self.stack2.setFrameShape(QListWidget.NoFrame)
        # self.stack3.setFrameShape(QListWidget.NoFrame)
        # self.stack4.setFrameShape(QListWidget.NoFrame)
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack4UI()

        # 在QStackedWidget对象中填充了4个子控件
        self.stack = QStackedWidget(self)
        self.main_layout.addWidget(self.stack)
        # self.stack.setMinimumSize(620,600)
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)
        self.stack.addWidget(self.stack4)

        self.LeftTabWidget.currentRowChanged.connect(self.display)  # 绑定

    def center(self):  # 设置窗口居中
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())

    # 热词分析
    def stack1UI(self):
        # 水平布局
        self.layout = QFormLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.logo = QPixmap('images\LOGO.jpg')
        self.l1 = QLabel(self)
        self.l1.setGeometry(0, 0, 150, 150)
        # lbl.setScaledContents (True)  # 让图片自适应label大小
        # self.l1.setStyleSheet("border: 2px solid blue")
        self.l1.setPixmap(self.logo)
        self.l2 = QLabel('请在右侧列表中选择你感兴趣的群组及时间段', self)
        self.l3 = QLabel('开启你的【热词分析】之旅~', self)
        self.layout.addWidget(self.l1)
        self.layout.addWidget(self.l2)
        self.layout.addWidget(self.l3)

        self.qunlist = QListWidget()

        self.layout.addWidget(self.qunlist)
        # lb2 = QLabel(self)
        # lb2.setGeometry(0, 250, 300, 200)
        # lb2.setPixmap(pix)
        # lb2.setStyleSheet("border: 2px solid red")
        # lb2.setScaledContents(True)

        # 在窗口w中，新建一个lable，名字叫做l1
        # self.l1=layout.addWidget(QLabel('x'))
        # self.logo = QPixmap('E:/pyprogram/1120-界面切换的研究/image/LOGO.jpg')
        # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
        # self.l1.setPix(self.logo)

        # 在窗口w中，新建一个lable，名字叫做l2
        # self.l2 = layout.addWidget(QLabel(self))
        # self.file = open('E:/pyprogram/1120-界面切换的研究/文本/热词介绍P1.txt')
        # self.reci=self.file.read()
        # self.l2.setText(self.reci)

        # 调整l1和l2的位置
        # self.l1.move(100, 20)
        # self.l2.move(140, 120)

        self.stack1.setLayout(self.layout)

    # 关键词提醒
    # --------未完工------------#
    def stack2UI(self):
        main_layout = QGridLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.stack2.resize(620, 600)
        self.stack2.setLayout(main_layout)
        buntton = QPushButton('新建关键词')
        # btn = QPushButton
        # btn.setFrameShape
        # buntton.setGeometry(0,300,100,40)
        # buntton.setStyleSheet('backgroud:rgb(33,33,33)'；)
        buntton.setStyleSheet('background: rgb(224，16，115);')
        buntton.setMinimumSize(620, 600)
        main_layout.addWidget(buntton)

    # 群发助手
    def stack3UI(self):
        # 水平布局
        layout = QHBoxLayout()
        # 添加控件到布局中
        layout.addWidget(QLabel('群发助手鸭'))
        self.stack3.setLayout(layout)

    # __________________单向好友检测___________________#
    def stack4UI(self):
        # 水平布局
        layout = QFormLayout()

        #图片
        self.logo = QPixmap('images\单向好友-logo.png')
        self.l1 = QLabel(self)
        self.l1.setGeometry(0, 0, 150, 150)
        # lbl.setScaledContents (True)  # 让图片自适应label大小
        # self.l1.setStyleSheet("border: 2px solid blue")
        self.l1.setPixmap(self.logo)

        #提示文字
        self.Warning1=QLabel('该功能有可能导致您的网页版微信被暂时封号！',self)
        self.Warning2=QLabel('请慎重使用!!!!!',self)
        self.l2 = QLabel('点击【开始检测】→扫描弹出的二维码登录您的微信→耐心等待几分钟', self)
        self.l3 = QLabel('即可在手机端确认您的单向好友！', self)

        # 检测按钮
        self.pushButton=QPushButton(self)
        self.pushButton.setIcon(QIcon(QPixmap('images\单向好友-按钮.png')))#icon
        self.pushButton.setText("开始检测")#text
        #self.pushButton.setShortcut('Ctrl+D')#shortcut key
        ##点击信号与槽函数进行连接，这一步实现：在控制台输出被点击的按钮
        self.pushButton.clicked.connect(lambda: self.whichbtn(self.pushButton))

        #实现单向好友检测
        self.pushButton.clicked.connect(lambda:self.testFriends(self.l2))
        self.pushButton.setToolTip("点击开始检测") #Tool tip

        #添加控件
        layout.addWidget(self.l1)
        layout.addWidget(self.Warning1)
        layout.addWidget(self.Warning2)
        layout.addWidget(self.l2)
        layout.addWidget(self.l3)
        layout.addWidget(self.pushButton)

        self.stack4.setLayout(layout)

    def testFriends(self, btn):
        single_friend_process = Process(target=singleFrinedTest, args=('test'))
        single_friend_process.start()

    def whichbtn(self,btn):
        #输出被点击的按钮
        print('clicked button is '+btn.text())
    # __________________单向好友检测___________________#


    def display(self, i):
        # 设置当前可见的选项卡的索引
        self.stack.setCurrentIndex(i)


# ----------------右边页面的类-------------#


# ---------------主函数------------------------#

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # style = open(r"D:\2018software\QssUI\StyleSheets\MetroUI.qss","r",encoding='utf-8')
    # style_str = style.read()
    # app.setStyleSheet(style_str)

    demo = Main_Window()
    demo.show()
    sys.exit(app.exec_())
