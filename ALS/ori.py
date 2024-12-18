# 生成 450 个用户打分的结果
import pandas as pd
import math
import numpy as np

# 读取 CSV 文件
df = pd.read_csv('/data/lizheyan/Workspace/Xuekeshijian/crawl/updated_douban_annime.csv')
total_people = 500
# 获取 rating 列
rating_column = df['rating']
print(rating_column)
matrix = np.random.randint(0, 1, size=(total_people, 450))

# 假设的均值和标准差
std_dev_score = 1
 
# 生成符合正态分布的随机打分
np.random.seed(0)  # 设置随机种子以获得可重复的结果 

for i in range(len(rating_column)):
    mean_score = rating_column[i]
    scores = np.random.normal(loc=mean_score, scale=std_dev_score, size=total_people)
    # 将打分四舍五入到最接近的整数，并限制在 0 到 10 的范围内
    scores = np.clip(np.round(scores), 0, 10)
    # print(len(scores))
    for j in range(len(scores)):
        matrix[j][i] = scores[j]
cols = 450
for i in range(len(scores)):
    num_zeros = int(cols * 0.7)
    zero_indices = np.random.choice(cols, num_zeros, replace=False)
    matrix[i, zero_indices] = 0

matrix1 = matrix
for i in range(len(scores)):
    for j in range(len(matrix1[i])):
        if matrix1[i][j] != 0:
            matrix1[i][j] = 1

array1 = np.array(matrix1)

print(len(matrix))
print(len(matrix[0]))
print(len(rating_column))

for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if matrix[i][j] == 0:
            matrix[i][j] = rating_column[j]
# 假设你有一个二维数组
array = np.array(matrix)
print(array)
# 指定输出文件的名称
output_file = 'output.txt'
 
# 打开文件以写入模式
def writefile(output_file, array):
    with open(output_file, 'w') as f:
        # 遍历二维数组的每一行
        for row in array:
            # 将行中的元素转换为字符串，并使用空格连接
            line = ' '.join(map(str, row))
            # 写入文件并换行
            f.write(line + '\n')
writefile(output_file, array)
writefile("kanguo.txt", array1)
print(f"数组已成功写入到 {output_file} 文件中。")
