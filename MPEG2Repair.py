from pywinauto import application
import time
from configuration import time_converter, m2r_path


class MPEG2Repair:
    def __init__(self):
        self.app = application.Application(backend='uia').start(m2r_path)
        self.window = self.app.window(title='MPEG2Repair')
        self.object = self.window.wrapper_object()
        self.position = ((50, 50), (605, 50), (50, 450), (605, 450))
        self.progress = self.window.child_window(auto_id="1022", control_type="Text")
        self.finished = False
        self.remain_time = None
        self.file_name_list = None
        self.default_folder = False

    def position_set(self, count):
        self.object.iface_transform.Move(self.position[count][0],
                                         self.position[count][1])

    def set_folder_path(self, path):
        output = ""
        split = path.split("/")
        for value in split:
            if bool(value):
                output += value + "\\"

        return output

    def set_default_folder(self, path):
        self.window['파일 이름(N):Edit'].set_text(self.set_folder_path(path))
        time.sleep(0.1)
        self.window['열기(O)'].click_input()
        time.sleep(0.1)
        self.default_folder = True

    def open_select_file(self):
        self.window['...Button'].click_input()
        time.sleep(0.1)

    def file_open(self, filename, folder_path):
        self.open_select_file()
        if not self.default_folder:
            self.set_default_folder(folder_path)
        self.window['파일 이름(N):Edit'].set_text(filename)
        time.sleep(0.1)
        self.window['열기(O)'].click_input()
        self.finished = False
        self.remain_time = None

    def find_pid(self):
        self.window["Find PID'sButton"].click_input()

    def checkbox_click(self):
        self.window['Log ErrorsCheckBox'].click_input()

    def error_check_start(self):
        self.window['StartButton'].click_input()

    def progress_status(self):
        text = self.progress.window_text()
        percent = text[:text.find(" % Completed")]
        remain_time = text[text.find("Remaining: ") + len("Remaining: "):]
        if percent == "100":
            self.finished = True
        self.remain_time = time_converter(remain_time)

    def finished_popup_close(self):
        self.window['확인Button'].click_input()

    def close(self):
        self.app.kill()
