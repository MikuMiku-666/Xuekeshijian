import faiss
import pandas as pd
import numpy as np

score_path = '/home/hadoop/workspace/Xuekeshijian/ALS/output.txt'
kanguo_path = '/home/hadoop/workspace/Xuekeshijian/ALS/kanguo.txt'

with open(kanguo_path, 'r') as file:
    lines = file.readlines()
    matrix1 = [list(map(float, line.split())) for line in lines]  # 将每行分割并转换为浮点数

matrix_kanguo = np.array(matrix1)
with open(score_path, 'r') as file:
    lines = file.readlines()
    matrix2 = [list(map(float, line.split())) for line in lines]  # 将每行分割并转换为浮点数

matrix_score = np.array(matrix2)
matrix_np = matrix_score*matrix_kanguo

row, col = matrix_np.shape  # 向量维度
print(row)
print(col)
index = faiss.IndexFlatL2(col)  # 创建索引

index.add(matrix_np)

# 保存索引到文件
faiss.write_index(index, "faiss_score.index")

Xq = matrix_np[0:1]
k = 4  # 返回最近邻的数量
D, I = index.search(Xq, k)  # D 是距离数组，I 是最近邻的索引数组
print(I)  # 打印最近邻的索引
print(D)  # 打印与最近邻的距离