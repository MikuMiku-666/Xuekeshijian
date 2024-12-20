import os
import pandas as pd

with open('ALS/kanguo.txt', 'r') as file:
    # 读取所有行
    lines = file.readlines()
 
    # 初始化二维数组
    two_d_array = []
 
    # 遍历每一行
    for line in lines:
        # 去除行尾的换行符，并根据空格（或其他分隔符）分割字符串
        row = line.strip().split(' ')  # 如果是逗号分隔，则使用 split(',')
        
        # 将字符串列表转换为适当的数据类型，例如整数或浮点数
        # 这里假设数组元素是整数
        row = [float(x) for x in row]
        
        # 将转换后的行添加到二维数组中
        two_d_array.append(row)

def write_file(file_path, features):
    try:
        with open(file_path, 'w') as File:
            row_str = ' '.join(map(str, map(int, features)))
            File.writelines(row_str)
    except:
        print("Error!")   

arrary = two_d_array

for i in range(500):
    write_file("divide/users/" + str(i) + "/user_kanguo.txt", arrary[i])
    tmp = []
