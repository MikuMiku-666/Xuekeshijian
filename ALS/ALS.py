import numpy as np
import pandas as pd

input_file = 'output.txt'

# 初始化一个空列表来存储二维数组
array = []

# 打开文件以读取模式
with open(input_file, 'r') as f:
    # 遍历文件的每一行
    for line in f:
        # 去除行末的换行符，并按空格分隔字符串
        row = line.strip().split()
        # 将字符串列表转换为整数列表（假设数组中的元素是整数）
        row = list(map(int, row))
        # 将转换后的行添加到二维数组中
        array.append(row)

R = np.array(array)

print(R)

"""
@输入参数：
R：M*N 的评分矩阵
K：隐特征向量维度
max_iter: 最大迭代次数
alpha：步长
lamda：正则化系数

@输出：
分解之后的 P，Q
P：初始化用户特征矩阵M*K
Q：初始化物品特征矩阵N*K
"""

# 给定超参数
K = 10  # 隐特征向量维度
max_iter = 500  # 最大迭代次数
alpha = 0.0002  # 迭代步长
lamda = 0.004  # 正则化系数

# 核心算法
def LFM_grad_desc(R, K=10, max_iter=1000, alpha=0.0001, lamda=0.002):
    # 基本维度参数定义
    M = len(R)  # 行数
    N = len(R[0])  # 列数
    
    # P,Q初始值，随机生成 -> 随机梯度下降
    P = np.random.rand(M, K)  # 随机生成一个M*K的矩阵
    Q = np.random.rand(N, K)  # 随机生成一个N*K的矩阵
    Q = Q.T  # 将Q矩阵转置
    
    # 开始迭代
    for step in range(max_iter):
        # 对所有的用户u、物品i做遍历，对应的特征向量Pu、Qi梯度下降
        for u in range(M):
            for i in range(N):
                # 对于每一个大于0的评分，求出预测评分误差
                if R[u][i] > 0:
                    eui = np.dot(P[u,:], Q[:,i]) - R[u][i]  # 算出误差
                    
                    # 代入公式，按照梯度下降算法更新当前的Pu、Qi
                    for k in range(K):
                        P[u][k] = P[u][k] - alpha * (2 * eui * Q[k][i] + 2 * lamda * P[u][k])
                        Q[k][i] = Q[k][i] - alpha * (2 * eui * P[u][k] + 2 * lamda * Q[k][i])
        
        # u、i遍历完成，所有特征向量更新完成，可以得到P、Q，可以计算预测评分矩阵
        predR = np.dot(P, Q)
        
        # 计算当前损失函数
        cost = 0
        for u in range(M):
            for i in range(N):
                if R[u][i] > 0:
                    cost += (np.dot(P[u,:], Q[:,i]) - R[u][i]) ** 2
                    # 加上正则化项
                    for k in range(K):
                        cost += lamda * (P[u][k] ** 2 + Q[k][i] ** 2)
        if cost < 0.0001:
            break
        
    return P, Q.T, cost

P, Q, cost = LFM_grad_desc(R, K, max_iter, alpha, lamda)

print(P)
print(Q)
print(cost)

# 计算预测评分矩阵
predR = P.dot(Q.T)

print(R)
print(predR)

# 检验P和Q复原的矩阵与原矩阵的差距
def compute_reconstruction_error(R, predR):
    # 计算 Frobenius 范数的误差
    numerator = np.linalg.norm(R - predR)  # 分子，原矩阵与预测矩阵的 Frobenius 范数
    denominator = np.linalg.norm(R)  # 分母，原矩阵的 Frobenius 范数
    return numerator / denominator

reconstruction_error = compute_reconstruction_error(R, predR)
print(f"Reconstruction Error: {reconstruction_error:.4f}")

# 写入函数
def write_array(matrix, output_file):
    array = np.array(matrix)
    # 打开文件以写入模式
    with open(output_file, 'w') as f:
        # 遍历二维数组的每一行
        for row in array:
            # 将行中的元素转换为字符串，并使用空格连接
            line = ' '.join(map(str, row))
            # 写入文件并换行
            f.write(line + '\n')

write_array(P, "P_cpu.txt")
write_array(Q, "Q_cpu.txt")
