# 中北大学
# 造次
# 功能：
# 时间：2023/10/9 21:01
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
        self.setWindowTitle('深度学习模型预测')
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
        img_detection_title = QLabel("用yolov7进行识别")
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
        det_img_button = QPushButton("开始识别")
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

        # # todo vgg16界面
        img_detection_widget1 = QWidget()
        img_detection_layout1 = QVBoxLayout()
        img_detection_title1 = QLabel("用vgg16进行预测")
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
        det_img_button1 = QPushButton("开始检测")
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

        # # todo resnet18界面
        img_detection_widget2 = QWidget()
        img_detection_layout2 = QVBoxLayout()
        img_detection_title2 = QLabel("用resnet18进行预测")
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
        det_img_button2 = QPushButton("开始检测")
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
        # # todo unet界面
        img_detection_widget3 = QWidget()
        img_detection_layout3 = QVBoxLayout()
        img_detection_title3 = QLabel("用unet进行分割")
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
        # # todo fcn界面
        img_detection_widget4 = QWidget()
        img_detection_layout4 = QVBoxLayout()
        img_detection_title4 = QLabel("用fcn进行分割")
        img_detection_title4.setFont(font_title)
        mid_img_widget4 = QWidget()
        mid_img_layout4 = QHBoxLayout()
        self.left_img4 = QLabel()
        self.right_img4 = QLabel()
        self.left_img4.setPixmap(QPixmap("./yolov5/images/UI/up4.png"))
        self.right_img4.setPixmap(QPixmap("./yolov5/images/UI/right4.png"))
        self.left_img4.setAlignment(Qt.AlignCenter)
        self.right_img4.setAlignment(Qt.AlignCenter)
        mid_img_layout4.addWidget(self.left_img4)
        mid_img_layout4.addStretch(0)
        mid_img_layout4.addWidget(self.right_img4)
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

        # # todo rcnn界面
        img_detection_widget5 = QWidget()
        img_detection_layout5 = QVBoxLayout()
        img_detection_title5 = QLabel("用rcnn进行识别")
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
        det_img_button5 = QPushButton("开始识别")
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
        # # todo dcgan界面
        img_detection_widget6 = QWidget()
        img_detection_layout6 = QVBoxLayout()
        img_detection_title6 = QLabel("用dcgan进行生成")
        img_detection_title6.setFont(font_title)
        mid_img_widget6 = QWidget()
        mid_img_layout6 = QHBoxLayout()
        self.left_img61 = QLabel()
        self.right_img61 = QLabel()
        self.left_img62 = QLabel()
        self.right_img62 = QLabel()
        self.left_img63 = QLabel()
        self.right_img63 = QLabel()
        self.left_img64 = QLabel()
        self.right_img64 = QLabel()
        self.left_img65 = QLabel()
        self.right_img65 = QLabel()
        self.right_img61.setPixmap(QPixmap("./yolov5/images/UI/right6.png"))
        self.right_img61.setMaximumSize(200, 200)
        self.left_img61.setPixmap(QPixmap("./yolov5/images/UI/right6.png"))
        self.left_img61.setMaximumSize(200, 200)
        self.right_img62.setPixmap(QPixmap("./yolov5/images/UI/right6.png"))
        self.right_img62.setMaximumSize(200, 200)
        self.left_img62.setPixmap(QPixmap("./yolov5/images/UI/right6.png"))
        self.left_img62.setMaximumSize(200, 200)
        self.right_img63.setPixmap(QPixmap("./yolov5/images/UI/right6.png"))
        self.right_img63.setMaximumSize(200, 200)
        self.left_img63.setPixmap(QPixmap("./yolov5/images/UI/right6.png"))
        self.left_img63.setMaximumSize(200, 200)
        self.right_img64.setPixmap(QPixmap("./yolov5/images/UI/right6.png"))
        self.right_img64.setMaximumSize(200, 200)
        self.left_img64.setPixmap(QPixmap("./yolov5/images/UI/right6.png"))
        self.left_img64.setMaximumSize(200, 200)
        self.right_img65.setPixmap(QPixmap("./yolov5/images/UI/right6.png"))
        self.right_img65.setMaximumSize(200, 200)
        self.left_img65.setPixmap(QPixmap("./yolov5/images/UI/right6.png"))
        self.left_img65.setMaximumSize(200, 200)
        self.left_img61.setAlignment(Qt.AlignCenter)
        self.right_img61.setAlignment(Qt.AlignCenter)
        self.left_img62.setAlignment(Qt.AlignCenter)
        self.right_img62.setAlignment(Qt.AlignCenter)
        self.left_img63.setAlignment(Qt.AlignCenter)
        self.right_img63.setAlignment(Qt.AlignCenter)
        self.left_img64.setAlignment(Qt.AlignCenter)
        self.right_img64.setAlignment(Qt.AlignCenter)
        self.left_img65.setAlignment(Qt.AlignCenter)
        self.right_img65.setAlignment(Qt.AlignCenter)
        mid_img_layout6.addWidget(self.left_img61)
        mid_img_layout6.addWidget(self.left_img62)
        mid_img_layout6.addWidget(self.left_img63)
        mid_img_layout6.addWidget(self.left_img64)
        mid_img_layout6.addWidget(self.left_img65)
        mid_img_layout6.addStretch(0)
        mid_img_layout6.addWidget(self.right_img61)
        mid_img_layout6.addWidget(self.right_img62)
        mid_img_layout6.addWidget(self.right_img63)
        mid_img_layout6.addWidget(self.right_img64)
        mid_img_layout6.addWidget(self.right_img65)
        mid_img_widget6.setLayout(mid_img_layout6)
        det_img_button6 = QPushButton("开始识别")
        show_img_button6 = QPushButton("显示结果")
        det_img_button6.clicked.connect(self.detect_img6)
        show_img_button6.clicked.connect(self.show_result_image6)
        det_img_button6.setFont(font_main)
        show_img_button6.setFont(font_main)
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
        img_detection_layout6.addWidget(det_img_button6)
        img_detection_layout6.addWidget(show_img_button6)
        img_detection_widget6.setLayout(img_detection_layout6)
        # # todo ddpm界面
        img_detection_widget7 = QWidget()
        img_detection_layout7 = QVBoxLayout()
        img_detection_title7 = QLabel("用ddpm进行生成")
        img_detection_title7.setFont(font_title)
        mid_img_widget7 = QWidget()
        mid_img_layout7 = QHBoxLayout()
        self.left_img7 = QLabel()
        self.right_img7 = QLabel()
        self.left_img7.setPixmap(QPixmap("./yolov5/images/UI/right8.png"))
        self.right_img7.setPixmap(QPixmap("./yolov5/images/UI/right8.png"))
        self.left_img7.setAlignment(Qt.AlignCenter)
        self.right_img7.setAlignment(Qt.AlignCenter)
        mid_img_layout7.addWidget(self.left_img7)
        mid_img_layout7.addStretch(0)
        mid_img_layout7.addWidget(self.right_img7)
        mid_img_widget7.setLayout(mid_img_layout7)
        det_img_button7 = QPushButton("开始识别")
        show_img_button7 = QPushButton("显示结果")
        det_img_button7.clicked.connect(self.detect_img7)
        show_img_button7.clicked.connect(self.show_result_image7)
        det_img_button7.setFont(font_main)
        show_img_button7.setFont(font_main)
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
        img_detection_layout7.addWidget(det_img_button7)
        img_detection_layout7.addWidget(show_img_button7)
        img_detection_widget7.setLayout(img_detection_layout7)


        self.left_img.setAlignment(Qt.AlignCenter)
        self.left_img1.setAlignment(Qt.AlignCenter)
        self.left_img2.setAlignment(Qt.AlignCenter)
        self.left_img3.setAlignment(Qt.AlignCenter)
        self.left_img4.setAlignment(Qt.AlignCenter)
        self.left_img5.setAlignment(Qt.AlignCenter)
        #
        self.addTab(img_detection_widget, 'yolov7')
        self.addTab(img_detection_widget1, 'vgg16')
        self.addTab(img_detection_widget2, 'resnet18')
        self.addTab(img_detection_widget3, 'unet')
        self.addTab(img_detection_widget4, 'fcn')
        self.addTab(img_detection_widget5, 'rcnn')
        self.addTab(img_detection_widget6, 'dcgan')
        self.addTab(img_detection_widget7, 'ddpm')
        self.setTabIcon(0, QIcon('./yolov5/images/UI/yolov7.png'))
        self.setTabIcon(1, QIcon('./yolov5/images/UI/vgg16.png'))
        self.setTabIcon(2, QIcon('./yolov5/images/UI/resnet18.png'))
        self.setTabIcon(3, QIcon('./yolov5/images/UI/unet.png'))
        self.setTabIcon(4, QIcon('./yolov5/images/UI/fcn.png'))
        self.setTabIcon(5, QIcon('./yolov5/images/UI/rcnn.png'))
        self.setTabIcon(6, QIcon('./yolov5/images/UI/dcgan.png'))
        self.setTabIcon(7, QIcon('./yolov5/images/UI/2.png'))
    def detect_img(self):
        call(['python', 'yolov7/yolo_predict.py'])

    def show_result_image(self):
        # output_size = self.output_size
        im0 = cv2.imread('yolov7/test.png')
        resize_scale = 480 / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/yolov7/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img.setPixmap(QPixmap("images_upload/yolov7/single_result.jpg"))

    def detect_img1(self):
        call(['python', 'vgg16/vgg_predict.py'])

    def show_result_image1(self):
        output_size = 480
        im0 = cv2.imread('vgg16/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/vgg16/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img1.setPixmap(QPixmap("images_upload/vgg16/single_result.jpg"))

    def detect_img2(self):
        call(['python', 'resnet18/res_predict.py'])

    def show_result_image2(self):
        output_size = 480
        im0 = cv2.imread('resnet18/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/resnet18/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img2.setPixmap(QPixmap("images_upload/resnet18/single_result.jpg"))

    def detect_img3(self):
        call(['python', 'unet/unet_predict.py'])

    def show_result_image3(self):
        output_size = 480
        im0 = cv2.imread('unet/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/unet/single_result.tif", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img3.setPixmap(QPixmap("images_upload/unet/single_result.tif"))

    def detect_img4(self):
        call(['python', 'fcn/fcn_predict.py'])

    def show_result_image4(self):
        output_size = 480
        im0 = cv2.imread('fcn/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/fcn/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img4.setPixmap(QPixmap("images_upload/fcn/single_result.jpg"))

    def detect_img5(self):
        call(['python', 'faster_rcnn/rcnn_predict.py'])

    def show_result_image5(self):
        output_size = 480
        im0 = cv2.imread('faster_rcnn/test.png')
        resize_scale = output_size / im0.shape[0]
        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        cv2.imwrite("images_upload/rcnn/single_result.jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img5.setPixmap(QPixmap("images_upload/rcnn/single_result.jpg"))

    def detect_img6(self):
        call(['python', 'dcgan/inference.py'])

    def show_result_image6(self):
        # output_size = self.output_size
        # im0 = cv2.imread('dcgan/results/'+i+'.png')
        # resize_scale = output_size / im0.shape[0]
        # im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
        # cv2.imwrite("images_upload/dcgan/"+i+".jpg", im0)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.right_img61.setPixmap(QPixmap('dcgan/results/0.png'))
        self.left_img61.setPixmap(QPixmap('dcgan/results/1.png'))
        self.right_img62.setPixmap(QPixmap('dcgan/results/2.png'))
        self.left_img62.setPixmap(QPixmap('dcgan/results/3.png'))
        self.right_img63.setPixmap(QPixmap('dcgan/results/4.png'))
        self.left_img63.setPixmap(QPixmap('dcgan/results/5.png'))
        self.right_img64.setPixmap(QPixmap('dcgan/results/6.png'))
        self.left_img64.setPixmap(QPixmap('dcgan/results/7.png'))
        self.right_img65.setPixmap(QPixmap('dcgan/results/8.png'))
        self.left_img65.setPixmap(QPixmap('dcgan/results/9.png'))
    def detect_img7(self):
        call(['python', 'ddpm/Main.py'])

    def show_result_image7(self):
        output_size = 480
        im01 = cv2.imread('ddpm/SampledImgs/NoisyNoGuidenceImgs.png')
        im02 = cv2.imread('ddpm/SampledImgs/SampledNoGuidenceImgs.png')
        resize_scale = output_size / im01.shape[0]
        resize_scale1 = output_size / im02.shape[0]
        im01 = cv2.resize(im01, (0, 0), fx=resize_scale, fy=resize_scale)
        im02 = cv2.resize(im02, (0, 0), fx=resize_scale1, fy=resize_scale1)
        cv2.imwrite("images_upload/ddpm/single_result.jpg", im01)
        cv2.imwrite("images_upload/ddpm/single_result1.jpg", im02)
        # 目前的情况来看，应该只是ubuntu下会出问题，但是在windows下是完整的，所以继续
        self.left_img7.setPixmap(QPixmap('images_upload/ddpm/single_result.jpg'))
        self.right_img7.setPixmap(QPixmap('images_upload/ddpm/single_result1.jpg'))
    '''
    ***上传图片***
    '''

    def upload_img(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("C:/Users/Administrator/Desktop/deep_learning/images_upload/yolov7", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("C:/Users/Administrator/Desktop/deep_learning/images_upload/yolov7/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img.setPixmap(QPixmap("C:/Users/Administrator/Desktop/deep_learning/images_upload/yolov7/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img.setPixmap(QPixmap("yolov5/images/UI/right.png"))

    def upload_img1(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/vgg16", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            print(1)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/vgg16/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img1.setPixmap(QPixmap("images_upload/vgg16/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img1.setPixmap(QPixmap("yolov5/images/UI/right1.png"))

    def upload_img2(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/resnet18", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            print(1)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/resnet18/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img2.setPixmap(QPixmap("images_upload/resnet18/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img2.setPixmap(QPixmap("yolov5/images/UI/right2.png"))

    def upload_img3(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/unet", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            print(1)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/unet/upload_show_result.tif", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img3.setPixmap(QPixmap("images_upload/unet/upload_show_result.tif"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img3.setPixmap(QPixmap("yolov5/images/UI/right3.png"))

    def upload_img4(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/fcn", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/fcn/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img4.setPixmap(QPixmap("images_upload/fcn/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img4.setPixmap(QPixmap("yolov5/images/UI/right4.png"))

    def upload_img5(self):
        # 选择录像文件进行读取
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose file', '', '*.jpg *.png *.tif *.jpeg')
        if fileName:
            suffix = fileName.split(".")[-1]
            save_path = osp.join("images_upload/rcnn", "tmp_upload." + suffix)
            shutil.copy(fileName, save_path)
            # 应该调整一下图片的大小，然后统一防在一起
            im0 = cv2.imread(save_path)
            resize_scale = 480 / im0.shape[0]
            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
            cv2.imwrite("./images_upload/rcnn/upload_show_result.jpg", im0)
            # self.right_img.setPixmap(QPixmap("images/tmp/single_result.jpg"))
            self.img2predict = fileName
            self.left_img5.setPixmap(QPixmap("images_upload/rcnn/upload_show_result.jpg"))
            # todo 上传图片之后右侧的图片重置，
            self.right_img5.setPixmap(QPixmap("yolov5/images/UI/right5.png"))

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
