from threading import Thread, Lock
import time
from configuration import *
from MPEG2Repair import MPEG2Repair


def make_mpeg2repair(worker_count):
    program_list = []
    for i in range(worker_count):
        program_list.append(MPEG2Repair())

    return program_list


def set_position(program_list):
    for index, worker in enumerate(program_list):
        worker.position_set(index)


def set_worker_number():
    folder_list = input_path()
    if len(folder_list) >= 3:
        number = 3
    else:
        number = len(folder_list)

    return number


def set_stream_files_list(worker, files_list):
    worker.file_name_list = files_list[:]


def set_folder_and_files(program_list):
    folder_list = input_path()
    files_list = make_file_list(folder_list)
    for index, worker in enumerate(program_list):
        set_stream_files_list(worker, files_list[index])

    return folder_list


def start_mpeg2repair(mpeg2repair, filename, path):
    mpeg2repair.window.set_focus()
    time.sleep(0.1)
    mpeg2repair.file_open(filename, path)
    mpeg2repair.find_pid()
    mpeg2repair.checkbox_click()
    mpeg2repair.error_check_start()


def finish_mpeg2repair(mpeg2repair):
    mpeg2repair.window.click_input()
    mpeg2repair.finished_popup_close()


def run_thread(mpeg2repair, queue, lock, index, folder_path):
    for filename in mpeg2repair.file_name_list:
        file_status = check_file_status(folder_path + filename)
        good_file = file_status[0]
        if good_file:
            duration, file_size, unit = (
                file_status[1], file_status[2][0], file_status[2][1])

            finish_popup_exists = mpeg2repair.window[
                'Finished Processing File.'].exists()
            with lock:
                if finish_popup_exists:
                    finish_mpeg2repair(mpeg2repair)
                start_mpeg2repair(mpeg2repair, filename, folder_path)

            mpeg2repair.progress_status()
            if not mpeg2repair.finished:
                time.sleep(mpeg2repair.remain_time)

            while True:
                mpeg2repair.progress_status()
                if mpeg2repair.finished:
                    with lock:
                        finish_mpeg2repair(mpeg2repair)
                    log_text = "{0} / {1} / {2} {3}".format(
                        filename, duration, file_size, unit)
                    queue.put([log_text, index])
                    break
                else:
                    time.sleep(3)
        else:
            log_text = filename + " / bad file"
            queue.put([log_text, index])


def controller_method(queue):
    thread_list = []
    lock = Lock()
    worker_count = set_worker_number()
    program_list = make_mpeg2repair(worker_count)
    set_position(program_list)
    folder_list = set_folder_and_files(program_list)

    for index in range(0, worker_count):
        thread_list.append(Thread(target=run_thread,
                                  args=(program_list[index], queue, lock, index, folder_list[index], )))

    for thread in thread_list:
        thread.daemon = True
        thread.start()

    for thread in thread_list:
        thread.join()

    for program in program_list:
        program.close()
