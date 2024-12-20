import numpy as np
import csv

P_path = '/home/hadoop/workspace/Xuekeshijian/ALS/P.txt'
with open(P_path, 'r') as file:
    lines = file.readlines()
    matrix = [list(map(float, line.split())) for line in lines]  # 将每行分割并转换为浮点数

matrix_np = np.array(matrix)
filename = "user_feature.csv"
with open(filename, 'w', newline='') as csvfile:
    # 创建一个csv写入器
    writer = csv.writer(csvfile)

    writer.writerow(['feature'])

    for i in range(500):
        writer.writerow([matrix_np])