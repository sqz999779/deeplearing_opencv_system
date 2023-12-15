# 中北大学
# 造次
# 功能：
# 时间：2023/10/16 19:01
import os
import shutil
import sys
import threading
import os.path as osp
from pathlib import Path

import cv2
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from subprocess import call


FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


class Example(QTabWidget):

    def __init__(self):
        super(Example,self).__init__()
        self.setWindowTitle('图像处理应用')
        self.resize(1200, 800)
        self.setWindowIcon(QIcon("yolov5/images/UI/main.png"))
        self.output_size = 480
        self.img2predict = ""
        self.vid_source = '0'  # 初始设置为摄像头
        self.stopEvent = threading.Event()
        self.webcam = True
        self.stopEvent.clear()
        self.initUI()
        self.reset_vid()

    def initUI(self):
        # 图片检测子界面
        font_title = QFont('楷体', 16)
        font_main = QFont('楷体', 14)
        # 图片识别界面, 两个按钮，上传图片和显示结果
        img_detection_widget = QWidget()
        img_detection_layout = QVBoxLayout()
        img_detection_title = QLabel("三色图处理")
        img_detection_title.setFont(font_title)
        mid_img_widget = QWidget()
        mid_img_layout = QHBoxLayout()
        self.left_img = QLabel()
        self.right_img = QLabel()
        self.left_img.setPixmap(QPixmap("./yolov5/images/UI/up.png"))
        self.right_img.setPixmap(QPixmap("./yolov5/images/UI/right.png"))
        self.left_img.setAlignment(Qt.AlignCenter)
        self.right_img.setAlignment(Qt.AlignCenter)
        mid_img_layout.addWidget(self.left_img)
        mid_img_layout.addStretch(0)
        mid_img_layout.addWidget(self.right_img)
        mid_img_widget.setLayout(mid_img_layout)
        up_img_button = QPushButton("上传图片")
        det_img_button = QPushButton("开始运行")
        show_img_button = QPushButton("显示结果")
        up_img_button.clicked.connect(self.upload_img)
        det_img_button.clicked.connect(self.detect_img)
        show_img_button.clicked.connect(self.show_result_image)
        up_img_button.setFont(font_main)
        det_img_button.setFont(font_main)
        show_img_button.setFont(font_main)
        up_img_button.setStyleSheet("QPushButton{color:white}"
                                    "QPushButton:hover{background-color: rgb(2,110,180);}"
                                    "QPushButton{background-color:rgb(48,124,208)}"
                                    "QPushButton{border:2px}"
                                    "QPushButton{border-radius:5px}"
                                    "QPushButton{padding:5px 5px}"
                                    "QPushButton{margin:5px 5px}")
        det_img_button.setStyleSheet("QPushButton{color:white}"
                                     "QPushButton:hover{background-color: rgb(2,110,180);}"
                                     "QPushButton{background-color:rgb(48,124,208)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:5px}"
                                     "QPushButton{padding:5px 5px}"
                                     "QPushButton{margin:5px 5px}")
        show_img_button.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        img_detection_layout.addWidget(img_detection_title, alignment=Qt.AlignCenter)
        img_detection_layout.addWidget(mid_img_widget, alignment=Qt.AlignCenter)
        img_detection_layout.addWidget(up_img_button)
        img_detection_layout.addWidget(det_img_button)
        img_detection_layout.addWidget(show_img_button)
        img_detection_widget.setLayout(img_detection_layout)
        # up_img_button.clicked.connect(self.run_script)

        # # todo 边缘填充界面
        img_detection_widget1 = QWidget()
        img_detection_layout1 = QVBoxLayout()
        img_detection_title1 = QLabel("图像边缘填充处理")
        img_detection_title1.setFont(font_title)
        mid_img_widget1 = QWidget()
        mid_img_layout1 = QHBoxLayout()
        self.left_img1 = QLabel()
        self.right_img1 = QLabel()
        self.left_img1.setPixmap(QPixmap("./yolov5/images/UI/up1.png"))
        self.right_img1.setPixmap(QPixmap("./yolov5/images/UI/right1.png"))
        self.left_img1.setAlignment(Qt.AlignCenter)
        self.right_img1.setAlignment(Qt.AlignCenter)
        mid_img_layout1.addWidget(self.left_img1)
        mid_img_layout1.addStretch(0)
        mid_img_layout1.addWidget(self.right_img1)
        mid_img_widget1.setLayout(mid_img_layout1)
        up_img_button1 = QPushButton("上传图片")
        det_img_button1 = QPushButton("开始运行")
        show_img_button1 = QPushButton("显示结果")
        up_img_button1.clicked.connect(self.upload_img1)
        det_img_button1.clicked.connect(self.detect_img1)
        show_img_button1.clicked.connect(self.show_result_image1)
        up_img_button1.setFont(font_main)
        det_img_button1.setFont(font_main)
        show_img_button1.setFont(font_main)
        up_img_button1.setStyleSheet("QPushButton{color:white}"
                                     "QPushButton:hover{background-color: rgb(2,110,180);}"
                                     "QPushButton{background-color:rgb(48,124,208)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:5px}"
                                     "QPushButton{padding:5px 5px}"
                                     "QPushButton{margin:5px 5px}")
        det_img_button1.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        show_img_button1.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        img_detection_layout1.addWidget(img_detection_title1, alignment=Qt.AlignCenter)
        img_detection_layout1.addWidget(mid_img_widget1, alignment=Qt.AlignCenter)
        img_detection_layout1.addWidget(up_img_button1)
        img_detection_layout1.addWidget(det_img_button1)
        img_detection_layout1.addWidget(show_img_button1)
        img_detection_widget1.setLayout(img_detection_layout1)

        # # todo 图像融合界面
        img_detection_widget2 = QWidget()
        img_detection_layout2 = QVBoxLayout()
        img_detection_title2 = QLabel("图像融合处理")
        img_detection_title2.setFont(font_title)
        mid_img_widget2 = QWidget()
        mid_img_layout2 = QHBoxLayout()
        self.left_img2 = QLabel()
        self.right_img2 = QLabel()
        self.left_img2.setPixmap(QPixmap("./yolov5/images/UI/up2.png"))
        self.right_img2.setPixmap(QPixmap("./yolov5/images/UI/right2.png"))
        self.left_img2.setAlignment(Qt.AlignCenter)
        self.right_img2.setAlignment(Qt.AlignCenter)
        mid_img_layout2.addWidget(self.left_img2)
        mid_img_layout2.addStretch(0)
        mid_img_layout2.addWidget(self.right_img2)
        mid_img_widget2.setLayout(mid_img_layout2)
        up_img_button2 = QPushButton("上传图片")
        det_img_button2 = QPushButton("开始运行")
        show_img_button2 = QPushButton("显示结果")
        up_img_button2.clicked.connect(self.upload_img2)
        det_img_button2.clicked.connect(self.detect_img2)
        show_img_button2.clicked.connect(self.show_result_image2)
        up_img_button2.setFont(font_main)
        det_img_button2.setFont(font_main)
        show_img_button2.setFont(font_main)
        up_img_button2.setStyleSheet("QPushButton{color:white}"
                                     "QPushButton:hover{background-color: rgb(2,110,180);}"
                                     "QPushButton{background-color:rgb(48,124,208)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:5px}"
                                     "QPushButton{padding:5px 5px}"
                                     "QPushButton{margin:5px 5px}")
        det_img_button2.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        show_img_button2.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        img_detection_layout2.addWidget(img_detection_title2, alignment=Qt.AlignCenter)
        img_detection_layout2.addWidget(mid_img_widget2, alignment=Qt.AlignCenter)
        img_detection_layout2.addWidget(up_img_button2)
        img_detection_layout2.addWidget(det_img_button2)
        img_detection_layout2.addWidget(show_img_button2)
        img_detection_widget2.setLayout(img_detection_layout2)
        # # todo 颜色空间转换处理界面
        img_detection_widget3 = QWidget()
        img_detection_layout3 = QVBoxLayout()
        img_detection_title3 = QLabel("颜色空间转换处理")
        img_detection_title3.setFont(font_title)
        mid_img_widget3 = QWidget()
        mid_img_layout3 = QHBoxLayout()
        self.left_img3 = QLabel()
        self.right_img3 = QLabel()
        self.left_img3.setPixmap(QPixmap("./yolov5/images/UI/up3.png"))
        self.right_img3.setPixmap(QPixmap("./yolov5/images/UI/right3.png"))
        self.left_img3.setAlignment(Qt.AlignCenter)
        self.right_img3.setAlignment(Qt.AlignCenter)
        mid_img_layout3.addWidget(self.left_img3)
        mid_img_layout3.addStretch(0)
        mid_img_layout3.addWidget(self.right_img3)
        mid_img_widget3.setLayout(mid_img_layout3)
        up_img_button3 = QPushButton("上传图片")
        det_img_button3 = QPushButton("开始运行")
        show_img_button3 = QPushButton("显示结果")
        up_img_button3.clicked.connect(self.upload_img3)
        det_img_button3.clicked.connect(self.detect_img3)
        show_img_button3.clicked.connect(self.show_result_image3)
        up_img_button3.setFont(font_main)
        det_img_button3.setFont(font_main)
        show_img_button3.setFont(font_main)
        up_img_button3.setStyleSheet("QPushButton{color:white}"
                                     "QPushButton:hover{background-color: rgb(2,110,180);}"
                                     "QPushButton{background-color:rgb(48,124,208)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:5px}"
                                     "QPushButton{padding:5px 5px}"
                                     "QPushButton{margin:5px 5px}")
        det_img_button3.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        show_img_button3.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        img_detection_layout3.addWidget(img_detection_title3, alignment=Qt.AlignCenter)
        img_detection_layout3.addWidget(mid_img_widget3, alignment=Qt.AlignCenter)
        img_detection_layout3.addWidget(up_img_button3)
        img_detection_layout3.addWidget(det_img_button3)
        img_detection_layout3.addWidget(show_img_button3)
        img_detection_widget3.setLayout(img_detection_layout3)
        # # todo 图像阈值处理界面
        img_detection_widget4 = QWidget()
        img_detection_layout4 = QVBoxLayout()
        img_detection_title4 = QLabel("图像阈值处理")
        img_detection_title4.setFont(font_title)
        mid_img_widget4 = QWidget()
        mid_img_layout4 = QHBoxLayout()
        self.left_img4 = QLabel()
        self.right_img41 = QLabel()
        self.right_img42 = QLabel()
        self.left_img4.setPixmap(QPixmap("./yolov5/images/UI/up4.png"))
        self.right_img41.setPixmap(QPixmap("./yolov5/images/UI/right4.png"))
        self.right_img42.setPixmap(QPixmap("./yolov5/images/UI/right4.png"))
        self.left_img4.setAlignment(Qt.AlignCenter)
        self.right_img41.setAlignment(Qt.AlignCenter)
        self.right_img42.setAlignment(Qt.AlignCenter)
        mid_img_layout4.addWidget(self.left_img4)
        mid_img_layout4.addStretch(0)
        mid_img_layout4.addWidget(self.right_img41)
        mid_img_layout4.addWidget(self.right_img42)
        mid_img_widget4.setLayout(mid_img_layout4)
        up_img_button4 = QPushButton("上传图片")
        det_img_button4 = QPushButton("开始运行")
        show_img_button4 = QPushButton("显示结果")
        up_img_button4.clicked.connect(self.upload_img4)
        det_img_button4.clicked.connect(self.detect_img4)
        show_img_button4.clicked.connect(self.show_result_image4)
        up_img_button4.setFont(font_main)
        det_img_button4.setFont(font_main)
        show_img_button4.setFont(font_main)
        up_img_button4.setStyleSheet("QPushButton{color:white}"
                                     "QPushButton:hover{background-color: rgb(2,110,180);}"
                                     "QPushButton{background-color:rgb(48,124,208)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:5px}"
                                     "QPushButton{padding:5px 5px}"
                                     "QPushButton{margin:5px 5px}")
        det_img_button4.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        show_img_button4.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        img_detection_layout4.addWidget(img_detection_title4, alignment=Qt.AlignCenter)
        img_detection_layout4.addWidget(mid_img_widget4, alignment=Qt.AlignCenter)
        img_detection_layout4.addWidget(up_img_button4)
        img_detection_layout4.addWidget(det_img_button4)
        img_detection_layout4.addWidget(show_img_button4)
        img_detection_widget4.setLayout(img_detection_layout4)

        # # todo 滤波处理界面
        img_detection_widget5 = QWidget()
        img_detection_layout5 = QVBoxLayout()
        img_detection_title5 = QLabel("图像滤波处理")
        img_detection_title5.setFont(font_title)
        mid_img_widget5 = QWidget()
        mid_img_layout5 = QHBoxLayout()
        self.left_img5 = QLabel()
        self.right_img5 = QLabel()
        self.left_img5.setPixmap(QPixmap("./yolov5/images/UI/up5.png"))
        self.right_img5.setPixmap(QPixmap("./yolov5/images/UI/right5.png"))
        self.left_img5.setAlignment(Qt.AlignCenter)
        self.right_img5.setAlignment(Qt.AlignCenter)
        mid_img_layout5.addWidget(self.left_img5)
        mid_img_layout5.addStretch(0)
        mid_img_layout5.addWidget(self.right_img5)
        mid_img_widget5.setLayout(mid_img_layout5)
        up_img_button5 = QPushButton("上传图片")
        det_img_button5 = QPushButton("开始运行")
        show_img_button5 = QPushButton("显示结果")
        up_img_button5.clicked.connect(self.upload_img5)
        det_img_button5.clicked.connect(self.detect_img5)
        show_img_button5.clicked.connect(self.show_result_image5)
        up_img_button5.setFont(font_main)
        det_img_button5.setFont(font_main)
        show_img_button5.setFont(font_main)
        up_img_button5.setStyleSheet("QPushButton{color:white}"
                                     "QPushButton:hover{background-color: rgb(2,110,180);}"
                                     "QPushButton{background-color:rgb(48,124,208)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:5px}"
                                     "QPushButton{padding:5px 5px}"
                                     "QPushButton{margin:5px 5px}")
        det_img_button5.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        show_img_button5.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        img_detection_layout5.addWidget(img_detection_title5, alignment=Qt.AlignCenter)
        img_detection_layout5.addWidget(mid_img_widget5, alignment=Qt.AlignCenter)
        img_detection_layout5.addWidget(up_img_button5)
        img_detection_layout5.addWidget(det_img_button5)
        img_detection_layout5.addWidget(show_img_button5)
        img_detection_widget5.setLayout(img_detection_layout5)
        # # todo 腐蚀与膨胀界面
        img_detection_widget6 = QWidget()
        img_detection_layout6 = QVBoxLayout()
        img_detection_title6 = QLabel("腐蚀与膨胀处理")
        img_detection_title6.setFont(font_title)
        mid_img_widget6 = QWidget()
        mid_img_layout6 = QHBoxLayout()
        self.left_img6 = QLabel()
        self.right_img6 = QLabel()
        self.left_img6.setPixmap(QPixmap("./yolov5/images/UI/up6.png"))
        self.right_img6.setPixmap(QPixmap("./yolov5/images/UI/right61.png"))
        self.left_img6.setAlignment(Qt.AlignCenter)
        self.right_img6.setAlignment(Qt.AlignCenter)
        mid_img_layout6.addWidget(self.left_img6)
        mid_img_layout6.addStretch(0)
        mid_img_layout6.addWidget(self.right_img6)
        mid_img_widget6.setLayout(mid_img_layout6)
        up_img_button6 = QPushButton("上传图片")
        det_img_button6 = QPushButton("开始运行")
        show_img_button6 = QPushButton("显示结果")
        up_img_button6.clicked.connect(self.upload_img6)
        det_img_button6.clicked.connect(self.detect_img6)
        show_img_button6.clicked.connect(self.show_result_image6)
        up_img_button6.setFont(font_main)
        det_img_button6.setFont(font_main)
        show_img_button6.setFont(font_main)
        up_img_button6.setStyleSheet("QPushButton{color:white}"
                                     "QPushButton:hover{background-color: rgb(2,110,180);}"
                                     "QPushButton{background-color:rgb(48,124,208)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:5px}"
                                     "QPushButton{padding:5px 5px}"
                                     "QPushButton{margin:5px 5px}")
        det_img_button6.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        show_img_button6.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        img_detection_layout6.addWidget(img_detection_title6, alignment=Qt.AlignCenter)
        img_detection_layout6.addWidget(mid_img_widget6, alignment=Qt.AlignCenter)
        img_detection_layout6.addWidget(up_img_button6)
        img_detection_layout6.addWidget(det_img_button6)
        img_detection_layout6.addWidget(show_img_button6)
        img_detection_widget6.setLayout(img_detection_layout6)
        # # todo 形态学界面
        img_detection_widget7 = QWidget()
        img_detection_layout7 = QVBoxLayout()
        img_detection_title7 = QLabel("形态学变化处理")
        img_detection_title7.setFont(font_title)
        mid_img_widget7 = QWidget()
        mid_img_layout7 = QHBoxLayout()
        self.left_img7 = QLabel()
        self.right_img7 = QLabel()
        self.left_img7.setPixmap(QPixmap("./yolov5/images/UI/up.png"))
        self.right_img7.setPixmap(QPixmap("./yolov5/images/UI/right.png"))
        self.left_img7.setAlignment(Qt.AlignCenter)
        self.right_img7.setAlignment(Qt.AlignCenter)
        mid_img_layout7.addWidget(self.left_img7)
        mid_img_layout7.addStretch(0)
        mid_img_layout7.addWidget(self.right_img7)
        mid_img_widget7.setLayout(mid_img_layout7)
        up_img_button7 = QPushButton("上传图片")
        det_img_button7 = QPushButton("开始运行")
        show_img_button7 = QPushButton("显示结果")
        up_img_button7.clicked.connect(self.upload_img7)
        det_img_button7.clicked.connect(self.detect_img7)
        show_img_button7.clicked.connect(self.show_result_image7)
        up_img_button7.setFont(font_main)
        det_img_button7.setFont(font_main)
        show_img_button7.setFont(font_main)
        up_img_button7.setStyleSheet("QPushButton{color:white}"
                                     "QPushButton:hover{background-color: rgb(2,110,180);}"
                                     "QPushButton{background-color:rgb(48,124,208)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:5px}"
                                     "QPushButton{padding:5px 5px}"
                                     "QPushButton{margin:5px 5px}")
        det_img_button7.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        show_img_button7.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        img_detection_layout7.addWidget(img_detection_title7, alignment=Qt.AlignCenter)
        img_detection_layout7.addWidget(mid_img_widget7, alignment=Qt.AlignCenter)
        img_detection_layout7.addWidget(up_img_button7)
        img_detection_layout7.addWidget(det_img_button7)
        img_detection_layout7.addWidget(show_img_button7)
        img_detection_widget7.setLayout(img_detection_layout7)
        # # todo 边缘检测处理界面
        img_detection_widget8 = QWidget()
        img_detection_layout8 = QVBoxLayout()
        img_detection_title8 = QLabel("边缘检测处理")
        img_detection_title8.setFont(font_title)
        mid_img_widget8 = QWidget()
        mid_img_layout8 = QHBoxLayout()
        self.left_img8 = QLabel()
        self.right_img81 = QLabel()
        self.right_img82 = QLabel()
        self.right_img83 = QLabel()
        self.left_img8.setPixmap(QPixmap("./yolov5/images/UI/upp.png"))
        self.right_img81.setPixmap(QPixmap("./yolov5/images/UI/rightt.png"))
        self.right_img82.setPixmap(QPixmap("./yolov5/images/UI/rightt.png"))
        self.right_img83.setPixmap(QPixmap("./yolov5/images/UI/rightt.png"))
        self.left_img8.setAlignment(Qt.AlignCenter)
        self.right_img81.setAlignment(Qt.AlignCenter)
        self.right_img82.setAlignment(Qt.AlignCenter)
        self.right_img83.setAlignment(Qt.AlignCenter)
        mid_img_layout8.addWidget(self.left_img8)
        mid_img_layout8.addStretch(0)
        mid_img_layout8.addWidget(self.right_img81)
        mid_img_layout8.addWidget(self.right_img82)
        mid_img_layout8.addWidget(self.right_img83)
        mid_img_widget8.setLayout(mid_img_layout8)
        up_img_button8 = QPushButton("上传图片")
        det_img_button8 = QPushButton("开始运行")
        show_img_button8 = QPushButton("显示结果")
        up_img_button8.clicked.connect(self.upload_img8)
        det_img_button8.clicked.connect(self.detect_img8)
        show_img_button8.clicked.connect(self.show_result_image8)
        up_img_button8.setFont(font_main)
        det_img_button8.setFont(font_main)
        show_img_button8.setFont(font_main)
        up_img_button8.setStyleSheet("QPushButton{color:white}"
                                     "QPushButton:hover{background-color: rgb(2,110,180);}"
                                     "QPushButton{background-color:rgb(48,124,208)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:5px}"
                                     "QPushButton{padding:5px 5px}"
                                     "QPushButton{margin:5px 5px}")
        det_img_button8.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        show_img_button8.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        img_detection_layout8.addWidget(img_detection_title8, alignment=Qt.AlignCenter)
        img_detection_layout8.addWidget(mid_img_widget8, alignment=Qt.AlignCenter)
        img_detection_layout8.addWidget(up_img_button8)
        img_detection_layout8.addWidget(det_img_button8)
        img_detection_layout8.addWidget(show_img_button8)
        img_detection_widget8.setLayout(img_detection_layout8)
        # # todo 图像金字塔处理界面
        img_detection_widget9 = QWidget()
        img_detection_layout9 = QVBoxLayout()
        img_detection_title9 = QLabel("图像金字塔处理")
        img_detection_title9.setFont(font_title)
        mid_img_widget9 = QWidget()
        mid_img_layout9 = QHBoxLayout()
        self.left_img9 = QLabel()
        self.right_img9 = QLabel()
        self.left_img9.setPixmap(QPixmap("./yolov5/images/UI/up1.png"))
        self.right_img9.setPixmap(QPixmap("./yolov5/images/UI/right1.png"))
        self.left_img9.setAlignment(Qt.AlignCenter)
        self.right_img9.setAlignment(Qt.AlignCenter)
        mid_img_layout9.addWidget(self.left_img9)
        mid_img_layout9.addStretch(0)
        mid_img_layout9.addWidget(self.right_img9)
        mid_img_widget9.setLayout(mid_img_layout9)
        up_img_button9 = QPushButton("上传图片")
        det_img_button9 = QPushButton("开始运行")
        show_img_button9 = QPushButton("显示结果")
        up_img_button9.clicked.connect(self.upload_img9)
        det_img_button9.clicked.connect(self.detect_img9)
        show_img_button9.clicked.connect(self.show_result_image9)
        up_img_button9.setFont(font_main)
        det_img_button9.setFont(font_main)
        show_img_button9.setFont(font_main)
        up_img_button9.setStyleSheet("QPushButton{color:white}"
                                     "QPushButton:hover{background-color: rgb(2,110,180);}"
                                     "QPushButton{background-color:rgb(48,124,208)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:5px}"
                                     "QPushButton{padding:5px 5px}"
                                     "QPushButton{margin:5px 5px}")
        det_img_button9.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        show_img_button9.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        img_detection_layout9.addWidget(img_detection_title9, alignment=Qt.AlignCenter)
        img_detection_layout9.addWidget(mid_img_widget9, alignment=Qt.AlignCenter)
        img_detection_layout9.addWidget(up_img_button9)
        img_detection_layout9.addWidget(det_img_button9)
        img_detection_layout9.addWidget(show_img_button9)
        img_detection_widget9.setLayout(img_detection_layout9)
        # # todo 图像轮廓检测处理界面
        img_detection_widget10 = QWidget()
        img_detection_layout10 = QVBoxLayout()
        img_detection_title10 = QLabel("图像轮廓检测处理")
        img_detection_title10.setFont(font_title)
        mid_img_widget10 = QWidget()
        mid_img_layout10 = QHBoxLayout()
        self.left_img10 = QLabel()
        self.right_img10 = QLabel()
        self.left_img10.setPixmap(QPixmap("./yolov5/images/UI/up2.png"))
        self.right_img10.setPixmap(QPixmap("./yolov5/images/UI/right2.png"))
        self.left_img10.setAlignment(Qt.AlignCenter)
        self.right_img10.setAlignment(Qt.AlignCenter)
        mid_img_layout10.addWidget(self.left_img10)
        mid_img_layout10.addStretch(0)
        mid_img_layout10.addWidget(self.right_img10)
        mid_img_widget10.setLayout(mid_img_layout10)
        up_img_button10 = QPushButton("上传图片")
        det_img_button10 = QPushButton("开始运行")
        show_img_button10 = QPushButton("显示结果")
        up_img_button10.clicked.connect(self.upload_img10)
        det_img_button10.clicked.connect(self.detect_img10)
        show_img_button10.clicked.connect(self.show_result_image10)
        up_img_button10.setFont(font_main)
        det_img_button10.setFont(font_main)
        show_img_button10.setFont(font_main)
        up_img_button10.setStyleSheet("QPushButton{color:white}"
                                     "QPushButton:hover{background-color: rgb(2,110,180);}"
                                     "QPushButton{background-color:rgb(48,124,208)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:5px}"
                                     "QPushButton{padding:5px 5px}"
                                     "QPushButton{margin:5px 5px}")
        det_img_button10.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        show_img_button10.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        img_detection_layout10.addWidget(img_detection_title10, alignment=Qt.AlignCenter)
        img_detection_layout10.addWidget(mid_img_widget10, alignment=Qt.AlignCenter)
        img_detection_layout10.addWidget(up_img_button10)
        img_detection_layout10.addWidget(det_img_button10)
        img_detection_layout10.addWidget(show_img_button10)
        img_detection_widget10.setLayout(img_detection_layout10)
        # # todo 模板匹配处理界面
        img_detection_widget11 = QWidget()
        img_detection_layout11 = QVBoxLayout()
        img_detection_title11 = QLabel("图像模板匹配处理")
        img_detection_title11.setFont(font_title)
        mid_img_widget11 = QWidget()
        mid_img_layout11 = QHBoxLayout()
        self.left_img11 = QLabel()
        self.right_img11 = QLabel()
        self.left_img11.setPixmap(QPixmap("./yolov5/images/UI/up3.png"))
        self.right_img11.setPixmap(QPixmap("./yolov5/images/UI/right3.png"))
        self.left_img11.setAlignment(Qt.AlignCenter)
        self.right_img11.setAlignment(Qt.AlignCenter)
        mid_img_layout11.addWidget(self.left_img11)
        mid_img_layout11.addStretch(0)
        mid_img_layout11.addWidget(self.right_img11)
        mid_img_widget11.setLayout(mid_img_layout11)
        up_img_button11 = QPushButton("上传图片")
        det_img_button11 = QPushButton("开始运行")
        show_img_button11 = QPushButton("显示结果")
        up_img_button11.clicked.connect(self.upload_img11)
        det_img_button11.clicked.connect(self.detect_img11)
        show_img_button11.clicked.connect(self.show_result_image11)
        up_img_button11.setFont(font_main)
        det_img_button11.setFont(font_main)
        show_img_button11.setFont(font_main)
        up_img_button11.setStyleSheet("QPushButton{color:white}"
                                     "QPushButton:hover{background-color: rgb(2,110,180);}"
                                     "QPushButton{background-color:rgb(48,124,208)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:5px}"
                                     "QPushButton{padding:5px 5px}"
                                     "QPushButton{margin:5px 5px}")
        det_img_button11.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        show_img_button11.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        img_detection_layout11.addWidget(img_detection_title11, alignment=Qt.AlignCenter)
        img_detection_layout11.addWidget(mid_img_widget11, alignment=Qt.AlignCenter)
        img_detection_layout11.addWidget(up_img_button11)
        img_detection_layout11.addWidget(det_img_button11)
        img_detection_layout11.addWidget(show_img_button11)
        img_detection_widget11.setLayout(img_detection_layout11)

        # # todo 图像频域处理界面
        img_detection_widget12 = QWidget()
        img_detection_layout12 = QVBoxLayout()
        img_detection_title12 = QLabel("图像频域处理")
        img_detection_title12.setFont(font_title)
        mid_img_widget12 = QWidget()
        mid_img_layout12 = QHBoxLayout()
        self.left_img12 = QLabel()
        self.right_img12 = QLabel()
        self.left_img12.setPixmap(QPixmap("./yolov5/images/UI/up4.png"))
        self.right_img12.setPixmap(QPixmap("./yolov5/images/UI/right4.png"))
        self.left_img12.setAlignment(Qt.AlignCenter)
        self.right_img12.setAlignment(Qt.AlignCenter)
        mid_img_layout12.addWidget(self.left_img12)
        mid_img_layout12.addStretch(0)
        mid_img_layout12.addWidget(self.right_img12)
        mid_img_widget12.setLayout(mid_img_layout12)
        up_img_button12 = QPushButton("上传图片")
        det_img_button12 = QPushButton("开始运行")
        show_img_button12 = QPushButton("显示结果")
        up_img_button12.clicked.connect(self.upload_img12)
        det_img_button12.clicked.connect(self.detect_img12)
        show_img_button12.clicked.connect(self.show_result_image12)
        up_img_button12.setFont(font_main)
        det_img_button12.setFont(font_main)
        show_img_button12.setFont(font_main)
        up_img_button12.setStyleSheet("QPushButton{color:white}"
                                     "QPushButton:hover{background-color: rgb(2,110,180);}"
                                     "QPushButton{background-color:rgb(48,124,208)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:5px}"
                                     "QPushButton{padding:5px 5px}"
                                     "QPushButton{margin:5px 5px}")
        det_img_button12.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        show_img_button12.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        img_detection_layout12.addWidget(img_detection_title12, alignment=Qt.AlignCenter)
        img_detection_layout12.addWidget(mid_img_widget12, alignment=Qt.AlignCenter)
        img_detection_layout12.addWidget(up_img_button12)
        img_detection_layout12.addWidget(det_img_button12)
        img_detection_layout12.addWidget(show_img_button12)
        img_detection_widget12.setLayout(img_detection_layout12)

        # # todo 角点检测处理界面
        img_detection_widget13 = QWidget()
        img_detection_layout13 = QVBoxLayout()
        img_detection_title13 = QLabel("图像角点检测处理")
        img_detection_title13.setFont(font_title)
        mid_img_widget13 = QWidget()
        mid_img_layout13 = QHBoxLayout()
        self.left_img13 = QLabel()
        self.right_img131 = QLabel()
        self.right_img132 = QLabel()
        self.left_img13.setPixmap(QPixmap("./yolov5/images/UI/up5.png"))
        self.right_img131.setPixmap(QPixmap("./yolov5/images/UI/right5.png"))
        self.right_img132.setPixmap(QPixmap("./yolov5/images/UI/right5.png"))
        self.left_img13.setAlignment(Qt.AlignCenter)
        self.right_img131.setAlignment(Qt.AlignCenter)
        self.right_img132.setAlignment(Qt.AlignCenter)
        mid_img_layout13.addWidget(self.left_img13)
        mid_img_layout13.addStretch(0)
        mid_img_layout13.addWidget(self.right_img131)
        mid_img_layout13.addWidget(self.right_img132)
        mid_img_widget13.setLayout(mid_img_layout13)
        up_img_button13 = QPushButton("上传图片")
        det_img_button13 = QPushButton("开始运行")
        show_img_button13 = QPushButton("显示结果")
        up_img_button13.clicked.connect(self.upload_img13)
        det_img_button13.clicked.connect(self.detect_img13)
        show_img_button13.clicked.connect(self.show_result_image13)
        up_img_button13.setFont(font_main)
        det_img_button13.setFont(font_main)
        show_img_button13.setFont(font_main)
        up_img_button13.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        det_img_button13.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        show_img_button13.setStyleSheet("QPushButton{color:white}"
                                        "QPushButton:hover{background-color: rgb(2,110,180);}"
                                        "QPushButton{background-color:rgb(48,124,208)}"
                                        "QPushButton{border:2px}"
                                        "QPushButton{border-radius:5px}"
                                        "QPushButton{padding:5px 5px}"
                                        "QPushButton{margin:5px 5px}")
        img_detection_layout13.addWidget(img_detection_title13, alignment=Qt.AlignCenter)
        img_detection_layout13.addWidget(mid_img_widget13, alignment=Qt.AlignCenter)
        img_detection_layout13.addWidget(up_img_button13)
        img_detection_layout13.addWidget(det_img_button13)
        img_detection_layout13.addWidget(show_img_button13)
        img_detection_widget13.setLayout(img_detection_layout13)

        # # todo sift特征检测界面
        img_detection_widget14 = QWidget()
        img_detection_layout14 = QVBoxLayout()
        img_detection_title14 = QLabel("SIFT和ORB图像特征检测处理")
        img_detection_title14.setFont(font_title)
        mid_img_widget14 = QWidget()
        mid_img_layout14 = QHBoxLayout()
        self.left_img14 = QLabel()
        self.right_img141 = QLabel()
        self.right_img142 = QLabel()
        self.left_img14.setPixmap(QPixmap("./yolov5/images/UI/up6.png"))
        self.right_img141.setPixmap(QPixmap("./yolov5/images/UI/right61.png"))
        self.right_img142.setPixmap(QPixmap("./yolov5/images/UI/right61.png"))
        self.left_img14.setAlignment(Qt.AlignCenter)
        self.right_img141.setAlignment(Qt.AlignCenter)
        self.right_img142.setAlignment(Qt.AlignCenter)
        mid_img_layout14.addWidget(self.left_img14)
        mid_img_layout14.addStretch(0)
        mid_img_layout14.addWidget(self.right_img141)
        mid_img_layout14.addWidget(self.right_img142)
        mid_img_widget14.setLayout(mid_img_layout14)
        up_img_button14 = QPushButton("上传图片")
        det_img_button14 = QPushButton("开始运行")
        show_img_button14 = QPushButton("显示结果")
        up_img_button14.clicked.connect(self.upload_img14)
        det_img_button14.clicked.connect(self.detect_img14)
        show_img_button14.clicked.connect(self.show_result_image14)
        up_img_button14.setFont(font_main)
        det_img_button14.setFont(font_main)
        show_img_button14.setFont(font_main)
        up_img_button14.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        det_img_button14.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        show_img_button14.setStyleSheet("QPushButton{color:white}"
                                        "QPushButton:hover{background-color: rgb(2,110,180);}"
                                        "QPushButton{background-color:rgb(48,124,208)}"
                                        "QPushButton{border:2px}"
                                        "QPushButton{border-radius:5px}"
                                        "QPushButton{padding:5px 5px}"
                                        "QPushButton{margin:5px 5px}")
        img_detection_layout14.addWidget(img_detection_title14, alignment=Qt.AlignCenter)
        img_detection_layout14.addWidget(mid_img_widget14, alignment=Qt.AlignCenter)
        img_detection_layout14.addWidget(up_img_button14)
        img_detection_layout14.addWidget(det_img_button14)
        img_detection_layout14.addWidget(show_img_button14)
        img_detection_widget14.setLayout(img_detection_layout14)
        # # todo 图像缩放+镜像+平移+旋转+仿射变换+透视变换界面
        img_detection_widget15 = QWidget()
        img_detection_layout15 = QVBoxLayout()
        img_detection_title15 = QLabel("图像变换处理")
        img_detection_title15.setFont(font_title)
        mid_img_widget15 = QWidget()
        mid_img_layout15 = QHBoxLayout()
        self.left_img15 = QLabel()
        self.right_img15 = QLabel()
        self.left_img15.setPixmap(QPixmap("./yolov5/images/UI/up7.png"))
        self.right_img15.setPixmap(QPixmap("./yolov5/images/UI/right7.png"))
        self.left_img15.setAlignment(Qt.AlignCenter)
        self.right_img15.setAlignment(Qt.AlignCenter)
        mid_img_layout15.addWidget(self.left_img15)
        mid_img_layout15.addStretch(0)
        mid_img_layout15.addWidget(self.right_img15)
        mid_img_widget15.setLayout(mid_img_layout15)
        up_img_button15 = QPushButton("上传图片")
        det_img_button15 = QPushButton("开始运行")
        show_img_button15 = QPushButton("显示结果")
        up_img_button15.clicked.connect(self.upload_img15)
        det_img_button15.clicked.connect(self.detect_img15)
        show_img_button15.clicked.connect(self.show_result_image15)
        up_img_button15.setFont(font_main)
        det_img_button15.setFont(font_main)
        show_img_button15.setFont(font_main)
        up_img_button15.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        det_img_button15.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        show_img_button15.setStyleSheet("QPushButton{color:white}"
                                        "QPushButton:hover{background-color: rgb(2,110,180);}"
                                        "QPushButton{background-color:rgb(48,124,208)}"
                                        "QPushButton{border:2px}"
                                        "QPushButton{border-radius:5px}"
                                        "QPushButton{padding:5px 5px}"
                                        "QPushButton{margin:5px 5px}")
        img_detection_layout15.addWidget(img_detection_title15, alignment=Qt.AlignCenter)
        img_detection_layout15.addWidget(mid_img_widget15, alignment=Qt.AlignCenter)
        img_detection_layout15.addWidget(up_img_button15)
        img_detection_layout15.addWidget(det_img_button15)
        img_detection_layout15.addWidget(show_img_button15)
        img_detection_widget15.setLayout(img_detection_layout15)
        # # todo 暴力特征匹配界面
        img_detection_widget16 = QWidget()
        img_detection_layout16 = QVBoxLayout()
        img_detection_title16 = QLabel("暴力特征匹配处理")
        img_detection_title16.setFont(font_title)
        mid_img_widget16 = QWidget()
        mid_img_layout16 = QHBoxLayout()
        self.left_img16 = QLabel()
        self.right_img16 = QLabel()
        self.left_img16.setPixmap(QPixmap("./yolov5/images/UI/up8.png"))
        self.right_img16.setPixmap(QPixmap("./yolov5/images/UI/right8.png"))
        self.left_img16.setAlignment(Qt.AlignCenter)
        self.right_img16.setAlignment(Qt.AlignCenter)
        mid_img_layout16.addWidget(self.left_img16)
        mid_img_layout16.addStretch(0)
        mid_img_layout16.addWidget(self.right_img16)
        mid_img_widget16.setLayout(mid_img_layout16)
        up_img_button16 = QPushButton("上传图片")
        det_img_button16 = QPushButton("开始运行")
        show_img_button16 = QPushButton("显示结果")
        up_img_button16.clicked.connect(self.upload_img16)
        det_img_button16.clicked.connect(self.detect_img16)
        show_img_button16.clicked.connect(self.show_result_image16)
        up_img_button16.setFont(font_main)
        det_img_button16.setFont(font_main)
        show_img_button16.setFont(font_main)
        up_img_button16.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        det_img_button16.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        show_img_button16.setStyleSheet("QPushButton{color:white}"
                                        "QPushButton:hover{background-color: rgb(2,110,180);}"
                                        "QPushButton{background-color:rgb(48,124,208)}"
                                        "QPushButton{border:2px}"
                                        "QPushButton{border-radius:5px}"
                                        "QPushButton{padding:5px 5px}"
                                        "QPushButton{margin:5px 5px}")
        img_detection_layout16.addWidget(img_detection_title16, alignment=Qt.AlignCenter)
        img_detection_layout16.addWidget(mid_img_widget16, alignment=Qt.AlignCenter)
        img_detection_layout16.addWidget(up_img_button16)
        img_detection_layout16.addWidget(det_img_button16)
        img_detection_layout16.addWidget(show_img_button16)
        img_detection_widget16.setLayout(img_detection_layout16)
        # # todo 添加噪声处理界面
        img_detection_widget17 = QWidget()
        img_detection_layout17 = QVBoxLayout()
        img_detection_title17 = QLabel("图像添加噪声处理")
        img_detection_title17.setFont(font_title)
        mid_img_widget17 = QWidget()
        mid_img_layout17 = QHBoxLayout()
        self.left_img17 = QLabel()
        self.right_img171 = QLabel()
        self.right_img172 = QLabel()
        self.left_img17.setPixmap(QPixmap("./yolov5/images/UI/upp.png"))
        self.right_img171.setPixmap(QPixmap("./yolov5/images/UI/rightt.png"))
        self.right_img172.setPixmap(QPixmap("./yolov5/images/UI/rightt.png"))
        self.left_img17.setAlignment(Qt.AlignCenter)
        self.right_img171.setAlignment(Qt.AlignCenter)
        self.right_img172.setAlignment(Qt.AlignCenter)
        mid_img_layout17.addWidget(self.left_img17)
        mid_img_layout17.addStretch(0)
        mid_img_layout17.addWidget(self.right_img171)
        mid_img_layout17.addWidget(self.right_img172)
        mid_img_widget17.setLayout(mid_img_layout17)
        up_img_button17 = QPushButton("上传图片")
        det_img_button17 = QPushButton("开始运行")
        show_img_button17 = QPushButton("显示结果")
        up_img_button17.clicked.connect(self.upload_img17)
        det_img_button17.clicked.connect(self.detect_img17)
        show_img_button17.clicked.connect(self.show_result_image17)
        up_img_button17.setFont(font_main)
        det_img_button17.setFont(font_main)
        show_img_button17.setFont(font_main)
        up_img_button17.setStyleSheet("QPushButton{color:white}"
                                     "QPushButton:hover{background-color: rgb(2,110,180);}"
                                     "QPushButton{background-color:rgb(48,124,208)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:5px}"
                                     "QPushButton{padding:5px 5px}"
                                     "QPushButton{margin:5px 5px}")
        det_img_button17.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        show_img_button17.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        img_detection_layout17.addWidget(img_detection_title17, alignment=Qt.AlignCenter)
        img_detection_layout17.addWidget(mid_img_widget17, alignment=Qt.AlignCenter)
        img_detection_layout17.addWidget(up_img_button17)
        img_detection_layout17.addWidget(det_img_button17)
        img_detection_layout17.addWidget(show_img_button17)
        img_detection_widget17.setLayout(img_detection_layout17)
        # # todo 图像直方图处理界面
        img_detection_widget18 = QWidget()
        img_detection_layout18 = QVBoxLayout()
        img_detection_title18 = QLabel("图像直方图处理")
        img_detection_title18.setFont(font_title)
        mid_img_widget18 = QWidget()
        mid_img_layout18 = QHBoxLayout()
        self.left_img18 = QLabel()
        self.right_img181 = QLabel()
        self.right_img182 = QLabel()
        self.right_img183 = QLabel()
        self.left_img18.setPixmap(QPixmap("./yolov5/images/UI/uppp.png"))
        self.right_img181.setPixmap(QPixmap("./yolov5/images/UI/righttt.png"))
        self.right_img182.setPixmap(QPixmap("./yolov5/images/UI/righttt.png"))
        self.right_img183.setPixmap(QPixmap("./yolov5/images/UI/righttt.png"))
        self.left_img18.setAlignment(Qt.AlignCenter)
        self.right_img181.setAlignment(Qt.AlignCenter)
        self.right_img182.setAlignment(Qt.AlignCenter)
        self.right_img183.setAlignment(Qt.AlignCenter)
        mid_img_layout18.addWidget(self.left_img18)
        mid_img_layout18.addStretch(0)
        mid_img_layout18.addWidget(self.right_img181)
        mid_img_layout18.addWidget(self.right_img182)
        mid_img_layout18.addWidget(self.right_img183)
        mid_img_widget18.setLayout(mid_img_layout18)
        up_img_button18 = QPushButton("上传图片")
        det_img_button18 = QPushButton("开始运行")
        show_img_button18 = QPushButton("显示结果")
        up_img_button18.clicked.connect(self.upload_img18)
        det_img_button18.clicked.connect(self.detect_img18)
        show_img_button18.clicked.connect(self.show_result_image18)
        up_img_button18.setFont(font_main)
        det_img_button18.setFont(font_main)
        show_img_button18.setFont(font_main)
        up_img_button18.setStyleSheet("QPushButton{color:white}"
                                     "QPushButton:hover{background-color: rgb(2,110,180);}"
                                     "QPushButton{background-color:rgb(48,124,208)}"
                                     "QPushButton{border:2px}"
                                     "QPushButton{border-radius:5px}"
                                     "QPushButton{padding:5px 5px}"
                                     "QPushButton{margin:5px 5px}")
        det_img_button18.setStyleSheet("QPushButton{color:white}"
                                      "QPushButton:hover{background-color: rgb(2,110,180);}"
                                      "QPushButton{background-color:rgb(48,124,208)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:5px}"
                                      "QPushButton{padding:5px 5px}"
                                      "QPushButton{margin:5px 5px}")
        show_img_button18.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton:hover{background-color: rgb(2,110,180);}"
                                       "QPushButton{background-color:rgb(48,124,208)}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:5px 5px}"
                                       "QPushButton{margin:5px 5px}")
        img_detection_layout18.addWidget(img_detection_title18, alignment=Qt.AlignCenter)
        img_detection_layout18.addWidget(mid_img_widget18, alignment=Qt.AlignCenter)
        img_detection_layout18.addWidget(up_img_button18)
        img_detection_layout18.addWidget(det_img_button18)
        img_detection_layout18.addWidget(show_img_button18)
        img_detection_widget18.setLayout(img_detection_layout18)

        self.left_img.setAlignment(Qt.AlignCenter)
        self.left_img1.setAlignment(Qt.AlignCenter)
        self.left_img2.setAlignment(Qt.AlignCenter)
        self.left_img3.setAlignment(Qt.AlignCenter)
        self.left_img4.setAlignment(Qt.AlignCenter)
        self.left_img5.setAlignment(Qt.AlignCenter)
        self.left_img6.setAlignment(Qt.AlignCenter)
        self.left_img7.setAlignment(Qt.AlignCenter)
        self.left_img8.setAlignment(Qt.AlignCenter)
        self.left_img9.setAlignment(Qt.AlignCenter)
        self.left_img10.setAlignment(Qt.AlignCenter)
        self.left_img11.setAlignment(Qt.AlignCenter)
        self.left_img12.setAlignment(Qt.AlignCenter)
        self.left_img13.setAlignment(Qt.AlignCenter)
        self.left_img14.setAlignment(Qt.AlignCenter)
        self.left_img15.setAlignment(Qt.AlignCenter)
        self.left_img16.setAlignment(Qt.AlignCenter)
        self.left_img17.setAlignment(Qt.AlignCenter)
        self.left_img18.setAlignment(Qt.AlignCenter)
        #
        self.addTab(img_detection_widget, '三色图')
        self.addTab(img_detection_widget1, '边缘填充')
        self.addTab(img_detection_widget2, '融合')
        self.addTab(img_detection_widget3, '颜色空间转换')
        self.addTab(img_detection_widget4, '阈值')
        self.addTab(img_detection_widget5, '滤波')
        self.addTab(img_detection_widget6, '腐蚀与膨胀')
        self.addTab(img_detection_widget7, '形态学')
        self.addTab(img_detection_widget18, '直方图')
        self.addTab(img_detection_widget8, '边缘检测')
        self.addTab(img_detection_widget9, '金字塔')
        self.addTab(img_detection_widget10, '轮廓检测')
        self.addTab(img_detection_widget11, '模块匹配')
        self.addTab(img_detection_widget12, '频域处理')
        self.addTab(img_detection_widget13, '角点检测')
        self.addTab(img_detection_widget14, '图像特征检测')
        self.addTab(img_detection_widget15, '图像变化')
        self.addTab(img_detection_widget16, '暴力特征匹配')
        self.addTab(img_detection_widget17, '添加噪声')

        self.setTabIcon(0, QIcon('./yolov5/images/UI/yolov7.png'))
        self.setTabIcon(1, QIcon('./yolov5/images/UI/vgg16.png'))
        self.setTabIcon(2, QIcon('./yolov5/images/UI/resnet18.png'))
        self.setTabIcon(3, QIcon('./yolov5/images/UI/unet.png'))
        self.setTabIcon(4, QIcon('./yolov5/images/UI/fcn.png'))
        self.setTabIcon(5, QIcon('./yolov5/images/UI/rcnn.png'))
        self.setTabIcon(6, QIcon('./yolov5/images/UI/dcgan.png'))
        self.setTabIcon(7, QIcon('./yolov5/images/UI/1.png'))
        self.setTabIcon(8, QIcon('./yolov5/images/UI/10.png'))
        self.setTabIcon(9, QIcon('./yolov5/images/UI/2.png'))
        self.setTabIcon(10, QIcon('./yolov5/images/UI/3.png'))
        self.setTabIcon(11, QIcon('./yolov5/images/UI/4.png'))
        self.setTabIcon(12, QIcon('./yolov5/images/UI/5.png'))
        self.setTabIcon(13, QIcon('./yolov5/images/UI/6.png'))
        self.setTabIcon(14, QIcon('./yolov5/images/UI/7.png'))
        self.setTabIcon(15, QIcon('./yolov5/images/UI/8.png'))
        self.setTabIcon(16, QIcon('./yolov5/images/UI/9.png'))
        self.setTabIcon(17, QIcon('./yolov5/images/UI/10.png'))
        self.setTabIcon(18, QIcon('./yolov5/images/UI/3.png'))
    def detect_img(self):
        call(['python', 'opencv_imageApply/image_process1/BGR.py'])

    def show_result_image(self):
        # output_size = self.output_size
        im0 = cv2.imread('opencv_imageApply/image_process1/test.png')
        resize_scale = 480 / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/opencv/process1/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img.setPixmap(QPixmap("images_upload/opencv/process1/single_result.jpg"))

    def detect_img1(self):
        call(['python', 'opencv_imageApply/image_process2/edgeFill.py'])

    def show_result_image1(self):
        output_size = 480
        im0 = cv2.imread('opencv_imageApply/image_process2/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/opencv/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img1.setPixmap(QPixmap("images_upload/opencv/single_result.jpg"))

    def detect_img2(self):
        call(['python', 'opencv_imageApply/image_process3/imageFusion.py'])

    def show_result_image2(self):
        output_size = 480
        im0 = cv2.imread('opencv_imageApply/image_process3/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/opencv/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img2.setPixmap(QPixmap("images_upload/opencv/single_result.jpg"))

    def detect_img3(self):
        call(['python', 'opencv_imageApply/image_process4/cvtColor.py'])

    def show_result_image3(self):
        output_size = 480
        im0 = cv2.imread('opencv_imageApply/image_process4/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/opencv/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img3.setPixmap(QPixmap("images_upload/opencv/single_result.jpg"))

    def detect_img4(self):
        call(['python', 'opencv_imageApply/image_process5/threshold.py'])

    def show_result_image4(self):
        output_size = 480
        im01 = cv2.imread('opencv_imageApply/image_process5/test1.png')
        im02 = cv2.imread('opencv_imageApply/image_process5/test2.png')
        resize_scale1 = output_size / im01.shape[0]
        resize_scale2 = output_size / im01.shape[0]
        im01 = cv2.resize(im01, (0, 0), fx=resize_scale1, fy=resize_scale1)
        im02 = cv2.resize(im02, (0, 0), fx=resize_scale2, fy=resize_scale2)
        cv2.imwrite("images_upload/opencv/process2/single_result1.jpg", im01)
        cv2.imwrite("images_upload/opencv/process2/single_result2.jpg", im02)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img41.setPixmap(QPixmap("images_upload/opencv/process2/single_result1.jpg"))
        self.right_img42.setPixmap(QPixmap("images_upload/opencv/process2/single_result2.jpg"))

    def detect_img5(self):
        call(['python', 'opencv_imageApply/image_process6/filter.py'])

    def show_result_image5(self):
        output_size = 540
        im0 = cv2.imread('opencv_imageApply/image_process6/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/opencv/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img5.setPixmap(QPixmap("images_upload/opencv/single_result.jpg"))

    def detect_img6(self):
        call(['python', 'opencv_imageApply/image_process7/erodeDilate.py'])

    def show_result_image6(self):
        output_size = 480
        im0 = cv2.imread('opencv_imageApply/image_process7/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/opencv/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img6.setPixmap(QPixmap("images_upload/opencv/single_result.jpg"))
    def detect_img7(self):
        call(['python', 'opencv_imageApply/image_process8/morphology.py'])

    def show_result_image7(self):
        output_size = 480
        im0 = cv2.imread('opencv_imageApply/image_process8/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/opencv/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img7.setPixmap(QPixmap("images_upload/opencv/single_result.jpg"))
    def detect_img8(self):
        call(['python', 'opencv_imageApply/image_process9/edgeDetection.py'])

    def show_result_image8(self):
        output_size = 330
        im01 = cv2.imread('opencv_imageApply/image_process9/test1.png')
        im02 = cv2.imread('opencv_imageApply/image_process9/test2.png')
        im03 = cv2.imread('opencv_imageApply/image_process9/test3.png')
        resize_scale1 = output_size / im01.shape[0]
        resize_scale2 = output_size / im02.shape[0]
        resize_scale3 = output_size / im03.shape[0]
        im01 = cv2.resize(im01, (0, 0), fx=resize_scale1, fy=resize_scale1)
        im02 = cv2.resize(im02, (0, 0), fx=resize_scale2, fy=resize_scale2)
        im03 = cv2.resize(im03, (0, 0), fx=resize_scale3, fy=resize_scale3)
        cv2.imwrite("images_upload/opencv/process3/single_result1.jpg", im01)
        cv2.imwrite("images_upload/opencv/process3/single_result2.jpg", im02)
        cv2.imwrite("images_upload/opencv/process3/single_result3.jpg", im03)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img81.setPixmap(QPixmap("images_upload/opencv/process3/single_result1.jpg"))
        self.right_img82.setPixmap(QPixmap("images_upload/opencv/process3/single_result2.jpg"))
        self.right_img83.setPixmap(QPixmap("images_upload/opencv/process3/single_result3.jpg"))
    def detect_img9(self):
        call(['python', 'opencv_imageApply/image_process10/pyramid.py'])

    def show_result_image9(self):
        output_size = 480
        im0 = cv2.imread('opencv_imageApply/image_process10/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/opencv/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img9.setPixmap(QPixmap("images_upload/opencv/single_result.jpg"))

    def detect_img10(self):
        call(['python', 'opencv_imageApply/image_process11/contourDetection.py'])
    def show_result_image10(self):
        output_size = 480
        im0 = cv2.imread('opencv_imageApply/image_process11/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/opencv/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img10.setPixmap(QPixmap("images_upload/opencv/single_result.jpg"))

    def detect_img11(self):
        call(['python', 'opencv_imageApply/image_process12/templateMatch.py'])
    def show_result_image11(self):
        output_size = 480
        im0 = cv2.imread('opencv_imageApply/image_process12/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/opencv/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img11.setPixmap(QPixmap("images_upload/opencv/single_result.jpg"))
    def detect_img12(self):
        call(['python', 'opencv_imageApply/image_process13/frequency.py'])
    def show_result_image12(self):
        output_size = 480
        im0 = cv2.imread('opencv_imageApply/image_process13/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/opencv/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img12.setPixmap(QPixmap("images_upload/opencv/single_result.jpg"))
    def detect_img13(self):
        call(['python', 'opencv_imageApply/image_process14/corner.py'])
    def show_result_image13(self):
        output_size = 480
        im01 = cv2.imread('opencv_imageApply/image_process14/test.png')
        im02 = cv2.imread('opencv_imageApply/image_process14/test1.png')
        resize_scale1 = output_size / im01.shape[0]
        resize_scale2 = output_size / im02.shape[0]
        im01 = cv2.resize(im01, (0, 0), fx=resize_scale1, fy=resize_scale1)
        im02 = cv2.resize(im02, (0, 0), fx=resize_scale2, fy=resize_scale2)
        cv2.imwrite("images_upload/opencv/single_result.jpg", im01)
        cv2.imwrite("images_upload/opencv/single_result1.jpg", im02)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img131.setPixmap(QPixmap("images_upload/opencv/single_result.jpg"))
        self.right_img132.setPixmap(QPixmap("images_upload/opencv/single_result1.jpg"))
    def detect_img14(self):
        call(['python', 'opencv_imageApply/image_process15/sift_orb.py'])
    def show_result_image14(self):
        output_size = 440
        im01 = cv2.imread('opencv_imageApply/image_process15/test.png')
        im02 = cv2.imread('opencv_imageApply/image_process15/test1.png')
        resize_scale1 = output_size / im01.shape[0]
        resize_scale2 = output_size / im02.shape[0]
        im01 = cv2.resize(im01, (0, 0), fx=resize_scale1, fy=resize_scale1)
        im02 = cv2.resize(im02, (0, 0), fx=resize_scale2, fy=resize_scale2)
        cv2.imwrite("images_upload/opencv/single_result.jpg", im01)
        cv2.imwrite("images_upload/opencv/single_result1.jpg", im02)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img141.setPixmap(QPixmap("images_upload/opencv/single_result.jpg"))
        self.right_img142.setPixmap(QPixmap("images_upload/opencv/single_result1.jpg"))
    def detect_img15(self):
        call(['python', 'opencv_imageApply/image_process17/imageReshape.py'])
    def show_result_image15(self):
        output_size = 480
        im0 = cv2.imread('opencv_imageApply/image_process17/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/opencv/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img15.setPixmap(QPixmap("images_upload/opencv/single_result.jpg"))
    def detect_img16(self):
        call(['python', 'opencv_imageApply/image_process16/BFMatcher.py'])
    def show_result_image16(self):
        output_size = 480
        im0 = cv2.imread('opencv_imageApply/image_process16/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/opencv/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img16.setPixmap(QPixmap("images_upload/opencv/single_result.jpg"))
    def detect_img17(self):
        call(['python', 'opencv_imageApply/image_process18/addNoise.py'])
    def show_result_image17(self):
        output_size = 420
        im01 = cv2.imread('opencv_imageApply/image_process18/test1.png')
        im02 = cv2.imread('opencv_imageApply/image_process18/test2.png')
        resize_scale1 = output_size / im01.shape[0]
        resize_scale2 = output_size / im02.shape[0]
        im01 = cv2.resize(im01, (0, 0), fx=resize_scale1, fy=resize_scale1)
        im02 = cv2.resize(im02, (0, 0), fx=resize_scale2, fy=resize_scale2)
        cv2.imwrite("images_upload/opencv/process4/single_result1.jpg", im01)
        cv2.imwrite("images_upload/opencv/process4/single_result2.jpg", im02)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img171.setPixmap(QPixmap("images_upload/opencv/process4/single_result1.jpg"))
        self.right_img172.setPixmap(QPixmap("images_upload/opencv/process4/single_result2.jpg"))
    def detect_img18(self):
        call(['python', 'opencv_imageApply/image_process20/histogram.py'])

    def show_result_image18(self):
        output_size = 380
        im01 = cv2.imread('opencv_imageApply/image_process20/test1.png')
        im02 = cv2.imread('opencv_imageApply/image_process20/test2.png')
        im03 = cv2.imread('opencv_imageApply/image_process20/test3.png')
        resize_scale1 = output_size / im01.shape[0]
        resize_scale2 = output_size / im02.shape[0]
        resize_scale3 = output_size / im03.shape[0]
        im01 = cv2.resize(im01, (0, 0), fx=resize_scale1, fy=resize_scale1)
        im02 = cv2.resize(im02, (0, 0), fx=resize_scale2, fy=resize_scale2)
        im03 = cv2.resize(im03, (0, 0), fx=resize_scale3, fy=resize_scale3)
        cv2.imwrite("images_upload/opencv/process5/single_result1.jpg", im01)
        cv2.imwrite("images_upload/opencv/process5/single_result2.jpg", im02)
        cv2.imwrite("images_upload/opencv/process5/single_result3.jpg", im03)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img181.setPixmap(QPixmap("images_upload/opencv/process5/single_result1.jpg"))
        self.right_img182.setPixmap(QPixmap("images_upload/opencv/process5/single_result2.jpg"))
        self.right_img183.setPixmap(QPixmap("images_upload/opencv/process5/single_result3.jpg"))
    '''
    ***上传图片***
    '''

    def upload_img(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("C:/Users/Administrator/Desktop/deep_learning/images_upload/opencv/process1", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("C:/Users/Administrator/Desktop/deep_learning/images_upload/opencv/process1/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img.setPixmap(QPixmap("C:/Users/Administrator/Desktop/deep_learning/images_upload/opencv/process1/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img.setPixmap(QPixmap("yolov5/images/UI/right.png"))

    def upload_img1(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img1.setPixmap(QPixmap("images_upload/opencv/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img1.setPixmap(QPixmap("yolov5/images/UI/right1.png"))

    def upload_img2(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            print(1)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img2.setPixmap(QPixmap("images_upload/opencv/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img2.setPixmap(QPixmap("yolov5/images/UI/right2.png"))

    def upload_img3(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            print(1)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img3.setPixmap(QPixmap("images_upload/opencv/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img3.setPixmap(QPixmap("yolov5/images/UI/right3.png"))

    def upload_img4(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv/process2", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/process2/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img4.setPixmap(QPixmap("images_upload/opencv/process2/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img41.setPixmap(QPixmap("yolov5/images/UI/right4.png"))
            self.right_img42.setPixmap(QPixmap("yolov5/images/UI/right4.png"))

    def upload_img5(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img5.setPixmap(QPixmap("images_upload/opencv/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img5.setPixmap(QPixmap("yolov5/images/UI/right5.png"))
    def upload_img6(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img6.setPixmap(QPixmap("images_upload/opencv/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img6.setPixmap(QPixmap("yolov5/images/UI/right61.png"))
    def upload_img7(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img7.setPixmap(QPixmap("images_upload/opencv/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img7.setPixmap(QPixmap("yolov5/images/UI/right.png"))
    def upload_img8(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv/process3", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 140 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/process3/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img8.setPixmap(QPixmap("images_upload/opencv/process3/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img81.setPixmap(QPixmap("yolov5/images/UI/rightt.png"))
            self.right_img82.setPixmap(QPixmap("yolov5/images/UI/rightt.png"))
            self.right_img83.setPixmap(QPixmap("yolov5/images/UI/rightt.png"))
    def upload_img9(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img9.setPixmap(QPixmap("images_upload/opencv/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img9.setPixmap(QPixmap("yolov5/images/UI/right1.png"))
    def upload_img10(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 330 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img10.setPixmap(QPixmap("images_upload/opencv/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img10.setPixmap(QPixmap("yolov5/images/UI/right2.png"))
    def upload_img11(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 330 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img11.setPixmap(QPixmap("images_upload/opencv/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img11.setPixmap(QPixmap("yolov5/images/UI/right3.png"))
    def upload_img12(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 330 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img12.setPixmap(QPixmap("images_upload/opencv/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img12.setPixmap(QPixmap("yolov5/images/UI/right4.png"))
    def upload_img13(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img13.setPixmap(QPixmap("images_upload/opencv/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img131.setPixmap(QPixmap("yolov5/images/UI/right5.png"))
            self.right_img132.setPixmap(QPixmap("yolov5/images/UI/right5.png"))
    def upload_img14(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 440 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/upload_show_result.jpg", im0)
            self.img2predict = fileName
            self.left_img14.setPixmap(QPixmap("images_upload/opencv/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img141.setPixmap(QPixmap("yolov5/images/UI/right61.png"))
            self.right_img142.setPixmap(QPixmap("yolov5/images/UI/right61.png"))
    def upload_img15(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img15.setPixmap(QPixmap("images_upload/opencv/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img15.setPixmap(QPixmap("yolov5/images/UI/right7.png"))
    def upload_img16(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img16.setPixmap(QPixmap("images_upload/opencv/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img16.setPixmap(QPixmap("yolov5/images/UI/right8.png"))
    def upload_img17(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv/process4", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 330 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/process4/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img17.setPixmap(QPixmap("images_upload/opencv/process4/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img171.setPixmap(QPixmap("yolov5/images/UI/rightt.png"))
            self.right_img172.setPixmap(QPixmap("yolov5/images/UI/rightt.png"))
    def upload_img18(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/opencv/process5", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 220 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/opencv/process5/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img18.setPixmap(QPixmap("images_upload/opencv/process5/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img181.setPixmap(QPixmap("yolov5/images/UI/righttt.png"))
            self.right_img182.setPixmap(QPixmap("yolov5/images/UI/righttt.png"))
            self.right_img183.setPixmap(QPixmap("yolov5/images/UI/righttt.png"))
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

    def reset_vid(self):
        # self.webcam_detection_btn.setEnabled(True)
        # self.mp4_detection_btn.setEnabled(True)
        # self.vid_img.setPixmap(QPixmap("yolov5/images/UI/up.jpeg"))
        self.vid_source = '0'
        self.webcam = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
