# coding=utf-8
"""
热词分析群组初步构建
"""

import sys
import time
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QLabel, QApplication,QFrame
from PyQt5.QtCore import *
from Barabove import Ui_Form

class BarLogic(QFrame,Ui_Form):
    def __init__(self, parent=None):
        super(BarLogic, self).__init__(parent)

        """初始化函数"""
        self.setupUi(self)
        self.retranslateUi(self)
        """初始化窗体"""
        self.setWindowFlags(Qt.FramelessWindowHint)  # 设置隐藏边框

        """初始化QSS"""
        self.setStyleSheet('QWidget{background-color: rgb(0,148,200)}'
                           'QPushButton{border:0px}'
                           'QPushButton#PB_close{image:url(./images/close-w.png)}'
                           'QPushButton#PB_zoom{image:url(./images/zoom-w.png)}'
                           'QPushButton#PB_shrink{image:url(./images/shrink-w.png)}')



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = BarLogic()
    ui.show()
    sys.exit(app.exec_())
