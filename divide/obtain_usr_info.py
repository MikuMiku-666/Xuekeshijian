import os
import pandas as pd


def write_file(file_path, usrname, psd):
    with open(file_path, 'w') as File:
        row_str = ' '.join([usrname, psd])
        File.writelines(row_str)

for i in range(500):
    usrname = "testusr" + str(i)
    psd = "abc123"
    write_file("divide/users/" + str(i) + "/userinfo.txt", usrname, psd)
    tmp = []
