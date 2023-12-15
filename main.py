import sys
import index
import windows_actions
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox
from PyQt5 import QtWidgets


# 注意这里定义的第一个界面的后端代码类需要继承两个类
import windows_actions1


class FirstWindowActions(index.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(index.Ui_MainWindow, self).__init__()
        # 创建界面
        self.setupUi(self)
        # 绑定槽函数
        self.pushButton.clicked.connect(self.open_btn_clicked)
        self.pushButton1.clicked.connect(self.open_btn_clicked1)

    # 核心代码
    # 定义一个按钮的槽函数
    def open_btn_clicked(self):
        """点击相应按钮，跳转到第二个界面"""
        # 实例化第二个界面的后端类，并对第二个界面进行显示
        # 通过派生新类去访问类
        self.another_window = windows_actions.AnotherWindowActions()
        self.another_window.show()
    def open_btn_clicked1(self):
        """点击相应按钮，跳转到第二个界面"""
        # 实例化第二个界面的后端类，并对第二个界面进行显示
        # 通过派生新类去访问类
        self.another_window = windows_actions1.AnotherWindowActions()
        self.another_window.show()


# 主程序入口
if __name__ == '__main__':
    # 这里是界面的入口，在这里需要定义QApplication对象，之后界面跳转时不用再重新定义，只需要调用show()函数即可
    app = QApplication(sys.argv)

    # 实例化
    demo_window = FirstWindowActions()

    # 显示
    demo_window.show()

    sys.exit(app.exec_())
