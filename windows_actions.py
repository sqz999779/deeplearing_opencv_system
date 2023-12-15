import sys

from PyQt5.QtGui import QIcon

import windows
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox, QTabWidget
from PyQt5 import QtWidgets


# 业务类需要继承两个类，一个设计的主界面，另一个是QMainWindow
class AnotherWindowActions(windows.Example):
    def __init__(self):
        """
         特别注意（最容易出错）：
         1.派生新类访问基类需要super(),同时它的参数是基类文件下的类及“ui_home_window.py中的
           Ui_MainWindow类”，
        """

        super(windows.Example, self).__init__()
        self.setWindowTitle('深度学习模型预测')
        self.resize(1200, 800)
        self.setWindowIcon(QIcon("yolov5/images/UI/main.png"))
        self.initUI()

