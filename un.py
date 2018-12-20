import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from untitled import Ui_Dialog


class SignupLogic(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(SignupLogic, self).__init__(parent)
        """初始化"""
        self.setupUi(self)
        self.retranslateUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)  # 去边框，不知道行不行
        timer = QTimer(self)
        timer.timeout.connect(self.close)
        timer.start(3000)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = SignupLogic()
    ui.show()
    sys.exit(app.exec_())
