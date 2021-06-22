import sys
import os
import json

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect
import main_ui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QResizeEvent

point_size = 2
# half

class MainWindowClass(QMainWindow, main_ui.Ui_ZC_Label):
    def __init__(self, parent = None):

        super(MainWindowClass, self).__init__(parent)
        self.setupUi(self)
        self.menu_open_folder.triggered.connect(self.openfolder)

        self.image_window.mousePressEvent = self.action_press_on_image
        self.image_window.mouseReleaseEvent = self.action_release_on_image
        self.image_window.mouseMoveEvent = self.action_move_on_image
        self.image_window.paintEvent = self.user_paint_event

        self.Q_damuzhi.clicked.connect(self.Q_damuzhi_clicked)
        self.W_shizhi.clicked.connect(self.W_shizhi_clicked)
        self.E_bbox.clicked.connect(self.E_bbox_clicked)
        self.A_prev.clicked.connect(self.A_prev_clicked)
        self.D_next.clicked.connect(self.D_next_clicked)

        self.chosed_action = None
        self.label_cursor_coord = self.cursor_coord
        self.folder_directory = ""
        self.already_labeled = 0
        self.img_list = []
        self.img_num = 0
        self.img_now = 0
        self.label_now = {"Q":  [-1, -1],
                          "W":  [-1, -1],
                          "E1": [-1, -1],
                          "E2": [-1, -1]}
        self.scale_ratio = 1
        self.draw_rect = False
        self.raw_width = 0
        self.raw_height = 0
        self.raw_pixmap = None

        self.no_prev_msg_box = QMessageBox(QMessageBox.Warning, "错误", "已达第一张！")
        self.no_next_msg_box = QMessageBox(QMessageBox.Warning, "错误", "已达最后一张！")
        self.no_picture_in_dic = QMessageBox(QMessageBox.Warning, "错误", "文件夹下没有图片！")
        
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        if self.raw_width != 0:
            window_width = self.image_window.width()
            window_height = self.image_window.height()
            self.scale_ratio = window_width / self.raw_width
        self.update()
    
    def Q_damuzhi_clicked(self):
        self.chosed_action = "Q"

    def W_shizhi_clicked(self):
        self.chosed_action = "W"

    def E_bbox_clicked(self):
        self.chosed_action = "E1"

    def A_prev_clicked(self):
        if self.label_now["Q"][0] > 0:
            json_name = self.img_list[self.img_now][:-4] + ".json"
            if not os.path.exists(json_name):
                self.already_labeled += 1
                self.labeled_number.setText(str(self.already_labeled))
            with open(json_name, 'w') as json_file:
                json.dump(self.label_now, json_file)
        self.img_now -= 1 
        if self.img_now == -1:
            self.no_prev_msg_box.exec_()
            self.img_now = 0
        else:
            self.load_pic_show(self.img_list[self.img_now])
        # TODO

    def D_next_clicked(self):
        if self.label_now["Q"][0] != 0 or self.label_now["W"][0] != 0 or self.label_now["E1"][0] != 0:
            json_name = self.img_list[self.img_now][:-4] + ".json"
            if not os.path.exists(json_name):
                self.already_labeled += 1
                self.labeled_number.setText(str(self.already_labeled))
            with open(json_name, 'w') as json_file:
                json.dump(self.label_now, json_file)
        self.img_now += 1 
        if self.img_now == self.img_num:
            self.no_next_msg_box.exec_()
            self.img_now -= 1
        else:
            self.load_pic_show(self.img_list[self.img_now])
        # TODO
    
    def action_release_on_image(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.chosed_action == "E2":
            self.E2_point.move(x - point_size, y - point_size)
            self.label_now["E2"] = [x / self.scale_ratio, y / self.scale_ratio]
            self.D_next_clicked()
            self.chosed_action = "Q"
            self.draw_rect = False

    def action_move_on_image(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.label_cursor_coord.setText(str(x) + ", " + str(y))
        if self.chosed_action == "E2":
            self.E2_point.move(x - point_size, y - point_size)
        self.update()

    def action_press_on_image(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.chosed_action == "Q":
            self.Q_point.move(x - point_size, y - point_size)
            self.label_now["Q"] = [x / self.scale_ratio, y / self.scale_ratio]
            self.chosed_action = "W"
            return
        elif self.chosed_action == "W":
            self.W_point.move(x - point_size, y - point_size)
            self.label_now["W"] = [x / self.scale_ratio, y / self.scale_ratio]
            self.chosed_action = "E1"
            return
        elif self.chosed_action == "E1":
            self.E1_point.move(x - point_size, y - point_size)
            self.label_now["E1"] = [x / self.scale_ratio, y / self.scale_ratio]
            self.chosed_action = "E2"
            self.draw_rect = True
            return
            #next page
    
    def user_paint_event(self, event):
        painter = QPainter(self.image_window)
        '''
        if self.raw_pixmap != None:
            painter.drawPixmap(0, 0, int(self.raw_width * self.scale_ratio), int(self.raw_height * self.scale_ratio), self.raw_pixmap)
        if self.chosed_action == "E2" and self.draw_rect == True:
            rect = QRect(self.E1_point.x() + point_size, self.E1_point.y() + point_size, self.E2_point.x() - self.E1_point.x(), self.E2_point.y() - self.E1_point.y())
            painter.setPen(QPen(Qt.yellow, 4))
            painter.drawRect(rect)
        '''
        if self.raw_pixmap != None:
            painter.drawPixmap(0, 0, int(self.raw_width * self.scale_ratio), int(self.raw_height * self.scale_ratio), self.raw_pixmap)
            rect = QRect(int(self.label_now["E1"][0] * self.scale_ratio - point_size), int(self.label_now["E1"][1] * self.scale_ratio - point_size), int((self.label_now["E2"][0] - self.label_now["E1"][0]) * self.scale_ratio) + 2 * point_size, int((self.label_now["E2"][1] - self.label_now["E1"][1]) * self.scale_ratio) + 2 * point_size)
            painter.setPen(QPen(Qt.green, 4))
            painter.drawRect(int(self.label_now["W"][0] * self.scale_ratio - point_size), int(self.label_now["W"][1] * self.scale_ratio - point_size), point_size * 2, point_size * 2)
            painter.setPen(QPen(Qt.red, 4))
            painter.drawRect(int(self.label_now["Q"][0] * self.scale_ratio - point_size), int(self.label_now["Q"][1] * self.scale_ratio - point_size), point_size * 2, point_size * 2)
            painter.setPen(QPen(Qt.yellow, 4))
            painter.drawRect(rect)

    def load_pic_show(self, imgName):
        self.raw_pixmap = QtGui.QPixmap(imgName)
        self.file_name.setText(imgName)
        self.file_name.setStyleSheet("color:red;")
        self.raw_width = self.raw_pixmap.width()
        self.raw_height = self.raw_pixmap.height()
        window_width = self.image_window.width()
        window_height = self.image_window.height()
        self.scale_ratio = window_width / self.raw_width
        json_name = imgName[:-4] + ".json"
        if os.path.isfile(json_name):
            self.file_name.setStyleSheet("color:green;")
            with open(json_name, 'r') as json_file:
                self.label_now = json.load(json_file)
        else:
            self.label_now = {"Q":  [-1, -1],
                              "W":  [-1, -1],
                              "E1": [-1, -1],
                              "E2": [-1, -1]}
            self.Q_point.move(1360, 350)
            self.W_point.move(1360, 380)
            self.E1_point.move(1360, 410)
            self.E2_point.move(1360, 440)
        self.chosed_action = "Q"
        self.update()
    
    def openfolder(self):
        self.img_list = []
        self.img_num = 0
        self.img_now = 0
        self.folder_directory = QFileDialog.getExistingDirectory(self, "打开文件夹（请打开子文件夹）", "./")
        self.already_labeled = 0
        if self.folder_directory == '' :
            return
        for file_path in os.listdir(self.folder_directory):
            if file_path.endswith(".bmp"):
                file_path = os.path.join(self.folder_directory, file_path)
                self.img_list.append(file_path)
                self.img_num += 1
            if file_path.endswith(".json"):
                self.already_labeled += 1
        if self.img_num != 0:
            self.load_pic_show(self.img_list[self.img_now])
        else:
            self.no_picture_in_dic.exec_()
        self.labeled_number.setText(str(self.already_labeled))
        return
        # TODO


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindowClass()
    main_window.show()
    sys.exit(app.exec_())