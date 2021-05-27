import sys
import os

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import main_ui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

class MainWindowClass(QMainWindow, main_ui.Ui_ZC_Label):
    def __init__(self, parent = None):

        super(MainWindowClass, self).__init__(parent)
        self.setupUi(self)
        self.actionopen_pic.triggered.connect(self.openimage)
        self.actionopen_folder.triggered.connect(self.openfolder)
        self.image_window.mousePressEvent = self.action_press_on_image

        self.Q_damuzhi.clicked.connect(self.Q_damuzhi_clicked)
        self.W_shizhi.clicked.connect(self.W_shizhi_clicked)
        self.E_bbox.clicked.connect(self.E_bbox_clicked)
        self.A_prev.clicked.connect(self.A_prev_clicked)
        self.D_next.clicked.connect(self.D_next_clicked)

        self.chosed_action = None
        self.img_list = []
        self.img_num = 0
        self.img_now = 0

        self.no_prev_msg_box = QMessageBox(QMessageBox.Warning, "错误", "已达第一张！")
        self.no_next_msg_box = QMessageBox(QMessageBox.Warning, "错误", "已达最后一张！")



        
    def Q_damuzhi_clicked(self):
        self.chosed_action = "Q"
    def W_shizhi_clicked(self):
        self.chosed_action = "W"
    def E_bbox_clicked(self):
        self.chosed_action = "E1"
    def A_prev_clicked(self):
        self.img_now -= 1 
        if self.img_now == -1:
            self.no_prev_msg_box.exec_()
            self.img_now = 0
        else:
            self.load_pic_show(self.img_list[self.img_now])
        # TODO

    def D_next_clicked(self):
        self.img_now += 1 
        if self.img_now == self.img_num:
            self.no_next_msg_box.exec_()
            self.img_now -= 1
        else:
            self.load_pic_show(self.img_list[self.img_now])
        # TODO

    def action_press_on_image(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.chosed_action == "Q":
            self.Q_point.move(x - 10, y - 10)
            self.chosed_action = "W"
            return
        elif self.chosed_action == "W":
            self.W_point.move(x - 10, y - 10)
            self.chosed_action = "E1"
            return
        elif self.chosed_action == "E1":
            self.E1_point.move(x - 10, y - 10)
            self.chosed_action = "E2"
            return
        elif self.chosed_action == "E2":
            self.E2_point.move(x - 10, y - 10)
            self.chosed_action = "Q"
            #next page
    
    def load_pic_show(self, imgName):
        raw_jpg = QtGui.QPixmap(imgName)
        raw_width = raw_jpg.width()
        raw_height = raw_jpg.height()
        window_width = self.image_window.width()
        window_height = self.image_window.height()
        scale_ratio = window_width / raw_width
        jpg = QtGui.QPixmap(imgName).scaled(int(scale_ratio * raw_width), int(scale_ratio * raw_height))
        self.image_window.setPixmap(jpg)


    def openimage(self):
        imgName, _ = QFileDialog.getOpenFileName(self, "打开图片", "", "*.bmp;;*.png;;*.jpg;;All files(*.*)")
        self.img_list = []
        self.img_list.append(imgName)
        self.img_num = 1
        self.img_now = 0
        self.load_pic_show(self.img_list[self.img_now])
    
    def openfolder(self):
        self.img_list = []
        self.img_num = 0
        self.img_now = 0
        folder_directory = QFileDialog.getExistingDirectory(self, "打开文件夹", "./")
        for file_path in os.listdir(folder_directory):
            if file_path.endswith(".bmp"):
                file_path = os.path.join(folder_directory, file_path)
                print(file_path)
                self.img_list.append(file_path)
                self.img_num += 1
        self.load_pic_show(self.img_list[self.img_now])
        return
        # TODO


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindowClass()
    main_window.show()
    sys.exit(app.exec_())