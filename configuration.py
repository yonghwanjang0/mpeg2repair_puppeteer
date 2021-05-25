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


def check_multi_audio(info):
    value = False
    if len(info.tracks) > 4:
        if info.tracks[3].track_type == 'Audio':
            value = True

    return value


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


def get_path_and_option(raw_path_list):
    output = []
    for raw_line in raw_path_list:
        split = raw_line.split("|")
        if len(split) == 2:
            path, option = split[0], split[1]
        else:
            path, option = split[0], None
        output.append([path, option])

    return output


def make_file_list(paths):
    total_list = []
    for p in paths:
        path, option = p[0], p[1]
        if path:
            files_list = next(os.walk(path))[2]
            files_list = date_filter(files_list, option)
            tp_list = container_filter(files_list, '.tp')
        else:
            tp_list = []
        total_list.append(tp_list)

    return total_list


def container_filter(files_list, filter_string):
    length = len(filter_string)
    filtered_list = []
    for file_name in files_list:
        if file_name[-length:] == filter_string:
            filtered_list.append(file_name)

    return filtered_list


def date_filter(files_list, date_option):
    if not date_option:
        filtered_list = files_list
    else:
        filtered_list = []
        for file_name in files_list:
            split = file_name.split("_")
            passed = filtered_date_condition(int(split[0]), date_option)
            if passed:
                filtered_list.append(file_name)

    return filtered_list


def filtered_date_condition(file_date, option):
    value = False
    condition = option.split("-")
    if len(condition) == 1:
        if file_date == int(condition[0]):
            value = True
    else:
        if condition[0] and condition[1]:
            if int(min(condition)) <= file_date <= int(max(condition)):
                value = True
        elif condition[0]:
            if int(condition[0]) <= file_date:
                value = True
        elif condition[1]:
            if file_date <= int(condition[1]):
                value = True

    return value


def check_file_status(file_path):
    duration = None
    file_size = None
    multi_audio_track = False
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
        multi_audio_track = check_multi_audio(media_info)

    return good_status, duration, file_size, multi_audio_track
