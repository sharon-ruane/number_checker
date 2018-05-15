import os
import shutil

DIR = "/home/iolie/PycharmProjects/keras__practice/number_checker/lfw"
NEW_DIR = "/home/iolie/PycharmProjects/keras__practice/number_checker/lfw_mix"

for root, dirs, files in os.walk(DIR):  # replace the . with your starting directory
    for file in files:
        if file.endswith('.jpg'):
            path_file = os.path.join(root, file)
            shutil.copy2(path_file, NEW_DIR)