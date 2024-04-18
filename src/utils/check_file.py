import os


def check_file_exist(path):
    if not os.path.isdir(path):
        os.makedirs(path)
