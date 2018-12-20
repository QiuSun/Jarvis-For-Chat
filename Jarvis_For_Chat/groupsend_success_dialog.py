# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'groupsend_success_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Groupsend_Success_Dialog(object):
    def setupUi(self, Groupsend_Success_Dialog):
        Groupsend_Success_Dialog.setObjectName("Groupsend_Success_Dialog")
        Groupsend_Success_Dialog.resize(185, 137)
        self.label = QtWidgets.QLabel(Groupsend_Success_Dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 161, 71))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Groupsend_Success_Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 100, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Groupsend_Success_Dialog)
        self.pushButton.clicked.connect(Groupsend_Success_Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Groupsend_Success_Dialog)

    def retranslateUi(self, Groupsend_Success_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Groupsend_Success_Dialog.setWindowTitle(_translate("Groupsend_Success_Dialog", "群发成功"))
        self.label.setText(_translate("Groupsend_Success_Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">群发成功！</p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">请在您的手机上查看结果</p></body></html>"))
        self.pushButton.setText(_translate("Groupsend_Success_Dialog", "确定"))

