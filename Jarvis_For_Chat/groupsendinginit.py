# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'groupsendinginit.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(550, 600)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(30, 30, 321, 192))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(30, 280, 150, 100))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(200, 280, 150, 101))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(370, 280, 150, 100))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(410, 110, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(30, 410, 150, 100))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(200, 410, 150, 100))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(370, 410, 150, 100))
        self.pushButton_7.setObjectName("pushButton_7")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(370, 160, 151, 81))
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "#XX#，圣诞节快乐！"))
        self.pushButton_2.setText(_translate("Form", "#XX#，元旦节快乐！"))
        self.pushButton_3.setText(_translate("Form", "#XX#，新年快乐！"))
        self.pushButton_4.setText(_translate("Form", "确认群发"))
        self.pushButton_5.setText(_translate("Form", "#XX#，平安夜快乐！"))
        self.pushButton_6.setText(_translate("Form", "#XX#，元宵节快乐！"))
        self.pushButton_7.setText(_translate("Form", "#XX#，反正祝你快乐！"))
        self.label.setText(_translate("Form",
                                      "<html><head/><body><p align=\"center\">群发模板编辑完毕后</p><p align=\"center\">请在右侧选择群发对象~</p><p align=\"center\">并点击确认群发</p></body></html>"))

