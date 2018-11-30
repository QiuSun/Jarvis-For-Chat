# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Login.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(340, 500)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 340, 500))
        self.widget.setObjectName("widget")
        self.LBP_password = QtWidgets.QLabel(self.widget)
        self.LBP_password.setGeometry(QtCore.QRect(40, 236, 40, 43))
        self.LBP_password.setText("")
        self.LBP_password.setObjectName("LBP_password")
        self.LB_logo = QtWidgets.QLabel(self.widget)
        self.LB_logo.setGeometry(QtCore.QRect(40, 40, 265, 111))
        self.LB_logo.setText("")
        self.LB_logo.setObjectName("LB_logo")
        self.PB_login = QtWidgets.QPushButton(self.widget)
        self.PB_login.setGeometry(QtCore.QRect(40, 312, 265, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.PB_login.setFont(font)
        self.PB_login.setObjectName("PB_login")
        self.LE_password = QtWidgets.QLineEdit(self.widget)
        self.LE_password.setGeometry(QtCore.QRect(80, 236, 225, 43))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.LE_password.setFont(font)
        self.LE_password.setObjectName("LE_password")
        self.PB_close = QtWidgets.QPushButton(self.widget)
        self.PB_close.setGeometry(QtCore.QRect(315, 0, 25, 25))
        self.PB_close.setText("")
        self.PB_close.setObjectName("PB_close")
        self.LE_username = QtWidgets.QLineEdit(self.widget)
        self.LE_username.setGeometry(QtCore.QRect(40, 190, 265, 43))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.LE_username.setFont(font)
        self.LE_username.setObjectName("LE_username")
        self.LBP_username = QtWidgets.QLabel(self.widget)
        self.LBP_username.setGeometry(QtCore.QRect(48, 198, 24, 27))
        self.LBP_username.setText("")
        self.LBP_username.setObjectName("LBP_username")
        self.LB_note = QtWidgets.QLabel(self.widget)
        self.LB_note.setGeometry(QtCore.QRect(120, 285, 161, 16))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.LB_note.setFont(font)
        self.LB_note.setText("")
        self.LB_note.setObjectName("LB_note")
        self.PB_reset = QtWidgets.QPushButton(self.widget)
        self.PB_reset.setGeometry(QtCore.QRect(245, 353, 61, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setUnderline(True)
        self.PB_reset.setFont(font)
        self.PB_reset.setObjectName("PB_reset")
        self.PB_tosignup = QtWidgets.QPushButton(self.widget)
        self.PB_tosignup.setGeometry(QtCore.QRect(233, 373, 71, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setUnderline(True)
        self.PB_tosignup.setFont(font)
        self.PB_tosignup.setObjectName("PB_tosignup")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "login_Dialog"))
        self.PB_login.setText(_translate("Dialog", "登录"))
        self.PB_reset.setText(_translate("Dialog", "忘记密码"))
        self.PB_tosignup.setText(_translate("Dialog", "  还没注册？"))

