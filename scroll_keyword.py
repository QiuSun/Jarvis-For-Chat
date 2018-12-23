# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scroll_keyword.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Gkeyword_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(270, 600)
        Form.setMinimumSize(QtCore.QSize(0, 0))
        Form.setMaximumSize(QtCore.QSize(270, 600))
        
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.PB_confirmgroup = QtWidgets.QPushButton(Form)
        self.PB_confirmgroup.setMinimumSize(QtCore.QSize(240, 40))
        
    
        self.PB_confirmgroup.setObjectName("PB_confirmgroup")
        self.horizontalLayout_2.addWidget(self.PB_confirmgroup)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 7, 0, 1, 1)
        self.SA_group = QtWidgets.QScrollArea(Form)
        self.SA_group.setMinimumSize(QtCore.QSize(70, 490))
        self.SA_group.setMaximumSize(QtCore.QSize(270, 600))
        self.SA_group.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SA_group.setMouseTracking(False)
        self.SA_group.setAutoFillBackground(False)
        self.SA_group.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SA_group.setLineWidth(1)
        self.SA_group.setWidgetResizable(True)
        self.SA_group.setObjectName("SA_group")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 270, 519))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setContentsMargins(0, 9, 9, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.SA_group.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.SA_group, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        
        self.LE_search = QtWidgets.QLineEdit(Form)
        self.LE_search.setMinimumSize(QtCore.QSize(20, 25))
        self.LE_search.setObjectName("LE_search")
        self.horizontalLayout.addWidget(self.LE_search)
        spacerItem1 = QtWidgets.QSpacerItem(18, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.PB_confirmgroup.setText(_translate("Form", "确定"))

