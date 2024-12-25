import faiss
import pandas as pd
import numpy as np


# 从文件加载索引
index = faiss.read_index("faiss_original.index")
print(index.reconstruct(0))
# Xq = matrix_np[0:1]
# k = 4  # 返回最近邻的数量
# D, I = index.search(Xq, k)  # D 是距离数组，I 是最近邻的索引数组
# print(I)  # 打印最近邻的索引
# print(D)  # 打印与最近邻的距离