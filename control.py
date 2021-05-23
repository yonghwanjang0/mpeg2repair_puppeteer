from threading import Thread, Lock
import time
from configuration import input_path, get_path_and_option, \
    make_file_list, check_file_status
from MPEG2Repair import MPEG2Repair


def check_api_input_path(qt_path_list):
    value = False
    for path in qt_path_list:
        if path is not None:
            value = True
            break

    return value


def make_mpeg2repair(need_to_create_list):
    program_list = []
    for create in need_to_create_list:
        if create:
            program_list.append(MPEG2Repair())
        else:
            program_list.append(None)

    return program_list


def set_position(program_list):
    for index, worker in enumerate(program_list):
        if worker:
            worker.position_set(index)


def set_worker_number():
    max_number = 3
    folder_list = input_path()
    if len(folder_list) >= max_number:
        number = max_number
    else:
        number = len(folder_list)

    return number


def set_stream_files_list(worker, files_list):
    worker.file_name_list = files_list[:]


def set_folder_and_files(program_list, path_and_option_list):
    files_list = make_file_list(path_and_option_list)
    for index, worker in enumerate(program_list):
        if worker:
            set_stream_files_list(worker, files_list[index])

    path_list = []
    for data in path_and_option_list:
        path_list.append(data[0])

    return path_list


def make_path_and_option_list_by_api(path_list, option_list):
    path_and_option_list = []
    for index in range(len(path_list)):
        if path_list[index]:
            path, option = path_list[index], option_list[index]
        else:
            path, option = None, None
        path_and_option_list.append([path, option])

    return path_and_option_list


def make_path_and_option_list_by_text():
    raw_list = input_path()
    path_and_option_list = get_path_and_option(raw_list)

    return path_and_option_list


def start_mpeg2repair(mpeg2repair, filename, path):
    mpeg2repair.file_open(filename, path)
    mpeg2repair.find_pid()
    mpeg2repair.checkbox_click()
    mpeg2repair.error_check_start()


def finish_mpeg2repair(mpeg2repair):
    mpeg2repair.finished_popup_close()


def run_thread(*args):
    input_queue_first_time = True
    check_waiting_time = 1
    mpeg2repair, queue, lock, index, folder_path = (
        args[0], args[1], args[2], args[3], args[4])

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

            if unit == "GB":
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
                    break
                else:
                    time.sleep(check_waiting_time)
        else:
            log_text = filename + " / bad file"

        if input_queue_first_time:
            queue.put([folder_path, index])
            queue.put(["=" * 50, index])
            input_queue_first_time = False
        queue.put([log_text, index])

    mpeg2repair.close()


def controller_method(queue, folder_list, option_list):
    thread_list = []
    lock = Lock()

    api_input = check_api_input_path(folder_list)
    # api input path
    if api_input:
        program_list = make_mpeg2repair(folder_list)
        path_and_option_list = make_path_and_option_list_by_api(
            folder_list, option_list)

    # text file input path
    else:
        worker_count = set_worker_number()
        need_to_create_list = [True for count in range(worker_count)]
        program_list = make_mpeg2repair(need_to_create_list)
        path_and_option_list = make_path_and_option_list_by_text()

    set_position(program_list)
    folder_list = set_folder_and_files(program_list, path_and_option_list)

    for index, program in enumerate(program_list):
        if program:
            thread_list.append(Thread(target=run_thread,
                                      args=(program, queue, lock, index,
                                            folder_list[index], )))
        else:
            thread_list.append(None)

    for thread in thread_list:
        if thread:
            thread.daemon = True
            thread.start()

    for thread in thread_list:
        if thread:
            thread.join()

    queue.put(["finish"])
