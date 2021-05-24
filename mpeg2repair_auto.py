from configuration import make_folder_tree, text_save, log_save_root, \
    make_folder
from multiprocessing import Process, Queue, freeze_support
from control import controller_method
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QWidget, QTextEdit, QLineEdit, QLabel,
                             QPushButton, QGridLayout, QVBoxLayout,
                             QMainWindow, QAction, QApplication)


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.qtxt1 = QTextEdit(self)
        self.qtxt1.setReadOnly(True)
        self.qtxt2 = QTextEdit(self)
        self.qtxt2.setReadOnly(True)
        self.qtxt3 = QTextEdit(self)
        self.qtxt3.setReadOnly(True)

        self.path_display1 = QLineEdit(self)
        self.path_display2 = QLineEdit(self)
        self.path_display3 = QLineEdit(self)

        self.option_display1 = QLineEdit(self)
        self.option_display2 = QLineEdit(self)
        self.option_display3 = QLineEdit(self)

        self.label1 = QLabel("Repair 1")
        self.label2 = QLabel("Repair 2")
        self.label3 = QLabel("Repair 3")
        self.path_label1 = QLabel("Input Path")
        self.path_label2 = QLabel("Input Path")
        self.path_label3 = QLabel("Input Path")
        self.option_label1 = QLabel("Input Option (optional)")
        self.option_label2 = QLabel("Input Option (optional)")
        self.option_label3 = QLabel("Input Option (optional)")

        self.btn1 = QPushButton("Start (F2)", self)
        self.btn1.setMinimumHeight(80)

        textbox_layout = QGridLayout()
        full_layout = QVBoxLayout()

        textbox_layout.addWidget(self.label1, 0, 0)
        textbox_layout.addWidget(self.label2, 0, 1)
        textbox_layout.addWidget(self.label3, 0, 2)
        textbox_layout.addWidget(self.qtxt1, 1, 0)
        textbox_layout.addWidget(self.qtxt2, 1, 1)
        textbox_layout.addWidget(self.qtxt3, 1, 2)

        textbox_layout.addWidget(self.path_label1, 2, 0)
        textbox_layout.addWidget(self.path_label2, 2, 1)
        textbox_layout.addWidget(self.path_label3, 2, 2)
        textbox_layout.addWidget(self.path_display1, 3, 0)
        textbox_layout.addWidget(self.path_display2, 3, 1)
        textbox_layout.addWidget(self.path_display3, 3, 2)

        textbox_layout.addWidget(self.option_label1, 4, 0)
        textbox_layout.addWidget(self.option_label2, 4, 1)
        textbox_layout.addWidget(self.option_label3, 4, 2)
        textbox_layout.addWidget(self.option_display1, 5, 0)
        textbox_layout.addWidget(self.option_display2, 5, 1)
        textbox_layout.addWidget(self.option_display3, 5, 2)

        full_layout.addLayout(textbox_layout)
        full_layout.addWidget(self.btn1)

        self.setLayout(full_layout)


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'MPEG2Repair Auto Checker v1.0.5.4'
        self.position = (620, 480, 1260, 660)
        self.cWidget = CentralWidget()
        self.setCentralWidget(self.cWidget)

        self.queue = Queue()
        self.controller = None
        self.finished_check_timer = QTimer()

        self.work_status = False
        self.work_start_time = None
        self.work_start_time_string = None

        self.path_list = [None, None, None]
        self.option_list = [None, None, None]
        self.current_log = ["", "", ""]

        # Function Setting
        get_start = QAction("&Start (F2)", self)
        get_start.setShortcut('F2')
        get_start.setStatusTip('Start')
        get_start.triggered.connect(self.program_start)
        self.cWidget.btn1.clicked.connect(self.program_start)

        self.statusBar()

        menubar = self.menuBar()
        filemenu = menubar.addMenu('&Menu')
        filemenu.addAction(get_start)

        # App Window setting
        self.setWindowTitle(self.title)
        self.setGeometry(
            self.position[0], self.position[1], self.position[2], self.position[3])

        self.show()

    def program_start(self):
        if not self.work_status:
            self.work_status = True
            self.work_start_time = time.localtime()
            self.work_start_time_string = time.strftime(
                "%Y%m%d-%H%M%S", self.work_start_time)
            self.get_folder_path()
            self.get_option()

            self.controller = Process(target=controller_method, args=(
                self.queue, self.path_list, self.option_list, ))
            self.controller.daemon = True
            self.controller.start()

            self.finished_check_timer.setInterval(1000)
            self.finished_check_timer.timeout.connect(self.finished_check)
            self.finished_check_timer.start()

    def get_attr_method(self, input_list, name_string):
        for index in range(0, len(input_list)):
            number = str(index + 1)
            name = name_string + number
            display_object = getattr(self.cWidget, name)

            if display_object.text():
                input_list[index] = display_object.text()

    def get_folder_path(self):
        self.get_attr_method(self.path_list, 'path_display')

    def get_option(self):
        self.get_attr_method(self.option_list, 'option_display')

    def clear_line_edit_by_before_worked(self):
        for index, value in enumerate(self.path_list):
            number = str(index + 1)
            path_object_name = 'path_display{}'.format(number)
            option_object_name = 'option_display{}'.format(number)

            path_display_object = getattr(self.cWidget, path_object_name)
            option_display_object = getattr(self.cWidget, option_object_name)

            if value:
                if path_display_object.text():
                    path_display_object.clear()
                if option_display_object.text():
                    option_display_object.clear()

    @staticmethod
    def log_update(msg, textbox):
        textbox.append(msg)

    def finished_check(self):
        if self.queue.qsize():
            result = self.queue.get()
            if result[0] != "finish":
                filename, thread_number = result[0], result[1]
                folder_path = make_folder_tree(
                    log_save_root, self.work_start_time,
                    self.work_start_time_string)
                make_folder(folder_path)
                log_file_name = "{0}-{1}.txt".format(
                    self.work_start_time_string, str(thread_number))

                if thread_number == 0:
                    textbox = self.cWidget.qtxt1
                elif thread_number == 1:
                    textbox = self.cWidget.qtxt2
                else:
                    textbox = self.cWidget.qtxt3

                self.log_update(filename, textbox)

                log_path = folder_path + log_file_name
                self.current_log[thread_number] += filename + "\n"
                text_save(log_path, self.current_log[thread_number])
            else:
                self.initialize()

    def initialize(self):
        self.finished_check_timer.stop()
        self.controller.join()

        self.work_status = False
        self.work_start_time = None
        self.work_start_time_string = None

        self.clear_line_edit_by_before_worked()
        self.path_list = [None, None, None]
        self.option_list = [None, None, None]
        self.current_log = ["", "", ""]


if __name__ == '__main__':
    freeze_support()
    import sys
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
