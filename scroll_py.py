# coding=utf-8
"""
热词分析群组初步构建
"""

import sys
import time
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QLabel, QApplication, QFrame,QPushButton
from PyQt5.QtCore import *
from scroll import Ui_Form


class GroupLogic(QFrame, Ui_Form):
    def __init__(self,groupname_list ,parent=None):
        super(GroupLogic, self).__init__(parent)
        """初始化函数"""
        self.setupUi(self)
        self.retranslateUi(self)
        """初始化list"""
        self.data=['a','b','c']
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

    def create_element(self,groupname_list):
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
            self.PB_group.clicked.connect(lambda: self.choose_group(self.sender().text()))

        self.SA_group.setWidget(self.topFiller)
        self.SA_group.setContentsMargins(0, 0, 0, 0)

    def choose_group(self, group_Name):
        """
        获取群名及时间段，并传给后端
        """
        #获取群名#
        #获取时间段#
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

        #将时间转为int#
        start_Time_Int=int(start_Time.strftime("%Y%m%d%H%M%S"))
        end_Time_Int=int(end_Time.strftime("%Y%m%d%H%M%S"))
        print(start_Time_Int)
        print(end_Time_Int)
        print(group_Name)



    def searchgroup(self):
        """
        搜索框搜索指定群组，并显示
        :return:
        """
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = GroupLogic()
    ui.show()
    sys.exit(app.exec_())
