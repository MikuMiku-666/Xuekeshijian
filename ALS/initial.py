import faiss
import pandas as pd
import numpy as np

Q_path = '/home/hadoop/workspace/Xuekeshijian/ALS/kanguo.txt'

with open(Q_path, 'r') as file:
    lines = file.readlines()
    matrix = [list(map(float, line.split())) for line in lines]  # 将每行分割并转换为浮点数

matrix_np = np.array(matrix)

row, col = matrix_np.shape  # 向量维度
print(col)
index = faiss.IndexFlatL2(col)  # 创建索引

index.add(matrix_np)

# 保存索引到文件
faiss.write_index(index, "faiss_kanguo.index")

Xq = matrix_np[0:1]
k = 4  # 返回最近邻的数量
D, I = index.search(Xq, k)  # D 是距离数组，I 是最近邻的索引数组
print(I)  # 打印最近邻的索引
print(D)  # 打印与最近邻的距离