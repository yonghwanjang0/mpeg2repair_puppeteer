from pywinauto import application
from configuration import time_converter, m2r_path


class MPEG2Repair:
    def __init__(self):
        self.app = application.Application(backend='uia').start(m2r_path)
        self.window = self.app.window(title='MPEG2Repair')
        self.object = self.window.wrapper_object()
        self.position = ((50, 50), (605, 50), (50, 450), (605, 450))

        # child window object (button, dialog, field, progress)
        self.progress = self.window.child_window(
            auto_id="1022", control_type="Text")
        self.file_dialog = self.window.child_window(
            auto_id="1091", control_type="Text")
        self.filename_field = self.window.child_window(
            auto_id="1148", control_type="Edit")
        self.open_button = self.window.child_window(
            auto_id="1", control_type="Button")
        self.done_button = self.window.child_window(
            auto_id="2", control_type="Button")
        self.no_button = self.window.child_window(
            auto_id="7", control_type="Button")

        self.finished = False
        self.remain_time = None
        self.file_name_list = None
        self.default_folder = False
        self.loop_stack = 0

    def position_set(self, count):
        self.object.iface_transform.Move(self.position[count][0],
                                         self.position[count][1])

    def set_default_folder(self, path):
        self.filename_field.set_text(path)
        self.open_button.type_keys("{ENTER}")

        self.default_folder = True

    def open_select_file(self, multi_audio):
        if self.window['Warning:Dialog'].exists():
            self.loop_stack += 1
            if self.window['Finished Processing File.'].exists():
                self.finished_popup_close(loop=True)
            self.cancel_overwrite_popup()

        dialog_button = self.window['...button0']
        if multi_audio:
            dialog_button.click_input()
        else:
            if self.loop_stack <= 2:
                dialog_button.set_focus()
                dialog_button.type_keys("{ENTER}")
            else:
                dialog_button.click_input()

        active_dialog = self.file_dialog.exists()
        if not active_dialog:
            self.open_select_file(multi_audio)

    def file_open(self, filename, folder_path, multi_audio):
        self.open_select_file(multi_audio)
        if not self.default_folder:
            self.set_default_folder(folder_path)
        self.filename_field.set_text(filename)
        self.open_button.type_keys("{ENTER}")
        self.loop_stack = 0
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

    def finished_popup_close(self, loop=False):
        self.done_button.set_focus()
        if loop:
            self.done_button.click_input()
        else:
            self.done_button.type_keys("{ENTER}")

    def cancel_overwrite_popup(self):
        self.no_button.set_focus()
        self.no_button.type_keys("{ENTER}")

    def close(self):
        self.app.kill()
