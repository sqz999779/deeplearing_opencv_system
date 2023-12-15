# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("深度学习模型与图像处理应用")
        MainWindow.resize(558, 483)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        # self.centralwidget.setObjectName("深度学习模型与图像处理应用")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(180, 100, 191, 51))
        self.pushButton.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(180, 300, 191, 51))
        self.pushButton1.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton1.setFont(font)
        self.pushButton1.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 558, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.retranslateUi1(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("deepLearning", "深度学习模型与图像处理应用"))
        MainWindow.setWindowIcon(QIcon("yolov5/images/UI/main.png"))
        self.pushButton.setText(_translate("MainWindow", "深度学习模型"))
    def retranslateUi1(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("imageApply", "深度学习模型与图像处理应用"))
        self.pushButton1.setText(_translate("MainWindow", "图像处理应用"))
    '''
    ### 界面关闭事件 ### 
    '''

    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                     '退出',
                                     "确定要退出吗?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            event.accept()
        else:
            event.ignore()
