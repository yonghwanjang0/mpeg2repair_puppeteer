from pywinauto import application
from configuration import time_converter, m2r_path


class MPEG2Repair:
    def __init__(self):
        self.app = application.Application(backend='uia').start(m2r_path)
        self.window = self.app.window(title='MPEG2Repair')
        self.object = self.window.wrapper_object()
        self.position = ((50, 50), (605, 50), (50, 450), (605, 450))
        self.progress = self.window.child_window(
            auto_id="1022", control_type="Text")
        self.finished = False
        self.remain_time = None
        self.file_name_list = None
        self.default_folder = False

    def position_set(self, count):
        self.object.iface_transform.Move(self.position[count][0],
                                         self.position[count][1])

    @staticmethod
    def set_folder_path(path):
        output = ""
        split = path.split("/")
        for value in split:
            if bool(value):
                output += value + "\\"

        return output

    def set_default_folder(self, path):
        self.window['파일 이름(N):Edit'].set_text(self.set_folder_path(path))
        self.window['열기(O)'].type_keys("{ENTER}")
        self.default_folder = True

    def open_select_file(self):
        if self.window['Finished Processing File.'].exists():
            self.finished_popup_close()

        if self.window['Warning:Dialog'].exists():
            self.cancel_overwrite_popup()

        dialog_button = self.window['...button0']
        dialog_button.set_focus()
        dialog_button.type_keys("{ENTER}")

        active_dialog = self.window['찾는 위치(I):Static'].exists()
        if not active_dialog:
            self.open_select_file()

    def file_open(self, filename, folder_path):
        self.open_select_file()
        if not self.default_folder:
            self.set_default_folder(folder_path)
        self.window['파일 이름(N):Edit'].set_text(filename)
        self.window['열기(O)'].type_keys("{ENTER}")
        self.finished = False
        self.remain_time = None

    def find_pid(self):
        self.window["Find PID'sButton"].type_keys("{ENTER}")

    def checkbox_click(self):
        self.window['Log ErrorsCheckBox'].type_keys("{SPACE}")

    def error_check_start(self):
        self.window['StartButton'].type_keys("{ENTER}")

    def get_text(self):
        try:
            text = self.progress.window_text()
        except Exception as e:
            print(str(e))
            text = self.get_text()

        return text

    def progress_status(self):
        text = self.get_text()
        percent = text[:text.find(" % Completed")]
        remain_time = text[text.find("Remaining: ") + len("Remaining: "):]
        if percent == "100":
            self.finished = True
        self.remain_time = time_converter(remain_time)

    def finished_popup_close(self):
        self.window['확인Button'].set_focus()
        self.window['확인Button'].type_keys("{ENTER}")
        self.window.type_keys("{TAB}")
        self.window.type_keys("{TAB}")

    def cancel_overwrite_popup(self):
        self.window['아니요(N)Button'].set_focus()
        self.window['아니요(N)Button'].type_keys("{ENTER}")
        self.window.type_keys("{TAB}")
        self.window.type_keys("{TAB}")

    def close(self):
        self.app.kill()
