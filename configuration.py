import os
from pymediainfo import MediaInfo


path_txt_file = "path.txt"
log_save_root = "log/"

m2r_path_text = "exe_path.txt"
with open(m2r_path_text, mode='r') as ff:
    m2r_path = ff.read()


def time_converter(string):
    time_str = string.split(":")
    second = ((int(time_str[0]) * 3600) + (int(time_str[1]) * 60)
              + int(time_str[2]))

    return second


def convert_duration(duration):
    duration = float(duration)
    hour = duration // 3600000
    hour_string = str(int(hour))
    remain_time = duration % 3600000

    minute = remain_time // 60000
    minute_string = str(int(minute)).zfill(2)
    remain_time = remain_time % 60000

    second = remain_time // 1000
    second_string = str(int(second)).zfill(2)

    under_second = remain_time % 1000
    under_second_string = str(int(under_second)).zfill(3)

    if hour >= 1:
        output = "{0}:{1}:{2}.{3}".format(
            hour_string, minute_string, second_string, under_second_string)
    elif minute >= 1:
        output = "{0}:{1}.{2}".format(
            minute_string, second_string, under_second_string)
    elif second >= 1:
        output = "{0}.{1}".format(second_string, under_second_string)
    else:
        output = "0.{}".format(under_second_string)

    return output


def convert_file_size(file_size):
    convert = file_size / 1024**3
    unit = "GB"
    if convert < 1:
        convert = file_size / 1024**2
        unit = "MB"

    convert = round(convert, 3)

    return str(convert), unit


def convert_path(origin):
    output = ""
    split = origin.split("/")
    for value in split:
        if bool(value):
            output += value + "\\"


def make_folder(folder_path):
    folder_check = os.path.isdir(folder_path)
    if folder_check is False:
        os.makedirs(folder_path)


def make_folder_tree(root, time_object, time_string):
    year = str(time_object.tm_year)
    month = str(time_object.tm_mon).zfill(2)
    first_folder_name = year + "y_" + month

    if root[-1] == "/":
        output = "{0}{1}/{2}/".format(root, first_folder_name, time_string)
    else:
        output = "{0}/{1}/{2}/".format(root, first_folder_name, time_string)

    return output


def text_save(path, value):
    with open(path, mode='w') as t:
        t.write(value)


def input_path():
    with open(path_txt_file, mode='r') as f:
        file_read = f.read()
    path_list = file_read.split("\n")

    return path_list


def make_file_list(paths):
    total_list = []
    for p in paths:
        files_list = next(os.walk(p))[2]
        tp_list = files_filter(files_list, '.tp')
        total_list.append(tp_list)

    return total_list


def files_filter(files_list, filter_string):
    length = len(filter_string)
    filtered_list = []
    for file_name in files_list:
        if file_name[-length:] == filter_string:
            filtered_list.append(file_name)

    return filtered_list


def check_file_status(file_path):
    duration = None
    file_size = None
    media_info = MediaInfo.parse(file_path)
    try:
        if "MPEG-TS" in media_info.tracks[0].format:
            good_status = True
        else:
            good_status = False
    except Exception as e:
        a = str(e)
        good_status = False

    if good_status:
        duration = convert_duration(media_info.tracks[0].duration)
        file_size = convert_file_size(media_info.tracks[0].file_size)

    return good_status, duration, file_size
