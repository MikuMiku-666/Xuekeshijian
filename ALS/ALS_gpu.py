import torch

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

# 将二维列表转换为PyTorch张量，并移到GPU上
R = torch.tensor(array, dtype=torch.float32).cuda()

print(R)
print(R.shape)

# 给定超参数
K = 20 # 隐特征向量维度
max_iter = 200 # 最大迭代次数
alpha = 0.00002 # 迭代步长
lamda = 0.004 # 正则化系数

# 核心算法
def LFM_grad_desc(R, K=1000, max_iter = 10, alpha = 10, lamda = 10):
    M, N = R.shape  # 获取矩阵的维度
    
    # P, Q 初始化
    P = torch.rand(M, K, device=R.device, dtype=torch.float32)  # 随机生成一个M*K的矩阵
    Q = torch.rand(N, K, device=R.device, dtype=torch.float32)  # 随机生成一个N*K的矩阵
    Q = Q.T  # 将Q矩阵转置

    # 开始迭代
    for step in range(max_iter):
        # 计算预测评分矩阵
        predR = torch.mm(P, Q)

        # 计算误差矩阵
        eR = (predR - R) * (R > 0).float()  # 只考虑评分矩阵中大于0的部分
        
        # 更新P和Q的梯度
        P_grad = torch.mm(eR, Q.T) + 2 * lamda * P  # P的梯度, L1正则化
        Q_grad = torch.mm(eR.T, P) + 2 * lamda * Q.T  # Q的梯度, L1正则化
        
        # 更新P和Q
        P -= alpha * P_grad
        Q -= alpha * Q_grad.T  # Q矩阵要转置回来

        # 计算当前损失函数（包括正则化）
        cost = (eR ** 2).sum() + lamda * (P ** 2).sum() + lamda * (Q ** 2).sum()
        
        if cost < 0.0001:
            break

    return P, Q.T, cost

P, Q, cost = LFM_grad_desc(R, K, max_iter, alpha, lamda)

print(P)
print(Q)
print(cost)

# 计算预测评分矩阵
predR = torch.mm(P, Q.T)

print(R.cpu())  # 将矩阵移回CPU进行显示
print(predR.cpu())

# 计算P和Q乘回去后的误差
reconstruction_error = torch.norm(R - predR) / torch.norm(R)  # 使用范数来计算误差

print(f'Reconstruction error: {reconstruction_error.item():.4f}')

# 写入函数
def write_array(matrix, output_file):
    array = matrix.cpu().numpy()  # 将矩阵移回CPU并转为NumPy数组
    with open(output_file, 'w') as f:
        for row in array:
            line = ' '.join(map(str, row))
            f.write(line + '\n')

write_array(P, "P.txt")
write_array(Q, "Q.txt")
