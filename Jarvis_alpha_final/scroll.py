# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scroll.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(270, 600)
        Form.setMinimumSize(QtCore.QSize(0, 0))
        Form.setMaximumSize(QtCore.QSize(270, 600))
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.SA_group = QtWidgets.QScrollArea(Form)
        self.SA_group.setMinimumSize(QtCore.QSize(70, 500))
        self.SA_group.setMaximumSize(QtCore.QSize(270, 600))
        self.SA_group.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SA_group.setMouseTracking(False)
        self.SA_group.setAutoFillBackground(False)
        self.SA_group.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SA_group.setLineWidth(1)
        self.SA_group.setWidgetResizable(True)
        self.SA_group.setObjectName("SA_group")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 270, 536))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setContentsMargins(0, 9, 9, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.SA_group.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.SA_group, 4, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.CBB_time = QtWidgets.QComboBox(Form)
        self.CBB_time.setMinimumSize(QtCore.QSize(20, 23))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.CBB_time.setFont(font)
        self.CBB_time.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CBB_time.setObjectName("CBB_time")
        self.CBB_time.addItem("")
        self.CBB_time.addItem("")
        self.CBB_time.addItem("")
        self.CBB_time.addItem("")
        self.horizontalLayout_3.addWidget(self.CBB_time)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LE_search = QtWidgets.QLineEdit(Form)
        self.LE_search.setMinimumSize(QtCore.QSize(20, 25))
        self.LE_search.setObjectName("LE_search")
        self.horizontalLayout.addWidget(self.LE_search)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.CBB_time.setItemText(0, _translate("Form", "过去6小时"))
        self.CBB_time.setItemText(1, _translate("Form", "过去24小时"))
        self.CBB_time.setItemText(2, _translate("Form", "过去三天"))
        self.CBB_time.setItemText(3, _translate("Form", "过去一周"))

