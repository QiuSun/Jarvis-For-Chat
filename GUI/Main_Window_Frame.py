import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
class Main_Window(QWidget):
    def __init__(self):
#--------------------------主窗体--------------------------------------#        
        super(Main_Window, self).__init__()        
        #self.setGeometry(0, 0, 800, 600
        self.resize(800,600)# 设置窗口初始位置和大小
        self.center()# 设置窗口居中       
        self.setWindowTitle('Jarvis For Chat 主界面框架')# 设置窗口标题
        #主窗网格布局，基底
        self.main_layout = QGridLayout(self,spacing=0)
        
        self.main_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.main_layout)
    #------------------------左边菜单栏--------------------------------------#
        self.LeftTabWidget = QListWidget()        
        self.LeftTabWidget.setFixedWidth(180)
        self.LeftTabWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.LeftTabWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.LeftTabWidget.setFrameShape(QListWidget.NoFrame)        
        #左侧组件设置
        self.left_layout = QVBoxLayout()    
        self.LeftTabWidget.setLayout(self.left_layout) #将左侧布局（垂直）绑定到左侧组件上
        #左侧布局
        self.main_layout.addWidget(self.LeftTabWidget,2,0)
        
        self.LeftTabWidget.currentRowChanged.connect(self.display) #绑定
        list_str = ['热点分析','关键词提醒','群发助手','单项好友删除']
        for i in range(4):
            self.item = QListWidgetItem(list_str[i],self.LeftTabWidget)   #左侧选项的添加
            self.item.setSizeHint(QSize(180,80))
            #self.item.set(0,(i+1)*180)
            self.item.setTextAlignment(Qt.AlignCenter)                  #居中显示
        
    #--------------------左侧菜单栏头像------------------------------------------#
        self.avatar_layout = QGridLayout()
        self.main_layout.addLayout(self.avatar_layout,0,0)

        self.avatar = QtWidgets.QPushButton()
        self.avatar.setFixedSize(QSize(90,90))
        self.avatar.setIcon(QIcon(r'D:\Jarvis-For-Chat\Resource\images\avatar1.png'))
        self.avatar.setIconSize(QSize(90,90))
        self.avatar_layout.addWidget(self.avatar,0,0,3,3)
        #self.avatar_layout.setAlignment(self.avatar_layout,Qt.AlignRight)

        self.weixin = QtWidgets.QPushButton()
        self.weixin.setFixedSize(QSize(45,45))
        self.weixin.setIcon(QIcon(r'D:\Jarvis-For-Chat\Resource\images\weixin1.png'))
        self.avatar_layout.addWidget(self.weixin,2,4,1,1)
        self.avatar_layout.setAlignment(self.weixin,Qt.AlignRight)
        self.avatar_layout.setAlignment(self.weixin,Qt.AlignBottom)
               
    #--------------------------右边页面-------------------------------------------#       
        # 在QStackedWidget对象中填充了4个子控件
        self.stack = QStackedWidget(self)
        self.right_layout = QGridLayout()
        #self.main_layout.addLayout(self.right_layout,0,5)
        self.stack.setLayout(self.right_layout)
        self.main_layout.addWidget(self.stack,0,1,14,14)
        #self.stack.setMinimumSize(620,600)
        
        # 创建4个小控件和函数
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()
       
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack4UI()

        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)
        self.stack.addWidget(self.stack4)

    def center(self):# 设置窗口居中
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())

    #热词分析
    def stack1UI(self):
        # 水平布局
        self.layout=QGridLayout()
        self.layout.setContentsMargins(0,0,0,0)
        
        self.l1=QLabel(self)
        self.l2 = QLabel('请在右侧列表中选择你感兴趣的群组及时间段', self)
        self.l3 = QLabel('开启你的【热词分析】之旅~', self)
        self.layout.addWidget(self.l1)
        self.layout.addWidget(self.l2)
        self.layout.addWidget(self.l3)
        self.qunlist = QListWidget()
        self.layout.addWidget(self.qunlist)
        
        self.stack1.setLayout(self.layout)

    #关键词提醒
    #--------未完工------------#
    def stack2UI(self):
    
        main_layout = QGridLayout()
        main_layout.setContentsMargins(0,0,0,0)
        self.stack2.resize(620,600)
        self.stack2.setLayout(main_layout)
        buntton = QPushButton('新建关键词')
        #btn = QPushButton
        #btn.setFrameShape
        #buntton.setGeometry(0,300,100,40)
        #buntton.setStyleSheet('backgroud:rgb(33,33,33)'；)
        buntton.setStyleSheet('background: rgb(19,60,85);')
        buntton.setMinimumSize(620,600)
        main_layout.addWidget(buntton)
        
   
    #群发助手
    def stack3UI(self):
        # 水平布局
        layout = QHBoxLayout()
        # 添加控件到布局中
        layout.addWidget(QLabel('群发助手鸭'))
        self.stack3.setLayout(layout)

    #单向好友检测
    def stack4UI(self):
        # 水平布局
        layout = QHBoxLayout()
        # 添加控件到布局中
        layout.addWidget(QPushButton('开始检测'))
        
        self.stack4.setLayout(layout)

    def display(self, i):
        # 设置当前可见的选项卡的索引
        self.stack.setCurrentIndex(i)

#----------------右边页面的类-------------#


#---------------主函数------------------------#

if __name__ == '__main__':
    app = QApplication(sys.argv)
    style = open(r"..\QSS\MetroUI.qss","r",encoding='utf-8')
    style_str = style.read()
    #app.setStyleSheet(style_str)

    demo = Main_Window()
    demo.show()
    sys.exit(app.exec_())
