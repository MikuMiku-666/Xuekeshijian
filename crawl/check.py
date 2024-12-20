import os
import csv

# 指定目录路径
directory = 'images'

# 获取目录下所有的.jpg文件
files = [f for f in os.listdir(directory) if f.endswith('.jpg')]

# 将文件名排序
files.sort()

# 检查文件名是否连续
expected_files = [str(i) + '.jpg' for i in range(7760)]  # 从0到6506
missing_files = [f for f in expected_files if f not in files]

# 输出结果
if missing_files:
    print("以下文件缺失:")
    for missing_file in missing_files:
        print(missing_file)
else:
    print("所有文件都存在，没有缺失。")

# 如果你还想检查是否有多余的文件
extra_files = [f for f in files if f not in expected_files]
if extra_files:
    print("\n以下文件是多余的:")
    for extra_file in extra_files:
        print(extra_file)

# 将缺失的文件序号提取到一个列表中
missing_numbers = [int(f.split('.')[0]) for f in missing_files]

# 将缺失的文件序号写入 CSV 文件
csv_filename = 'missing_files.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Missing File Numbers'])  # 写入标题
    # 将缺失文件序号转换为单个列表，每个序号作为一行
    for number in missing_numbers:
        writer.writerow([number])  # 写入缺失文件序号

print(f"\n缺失文件序号已写入 {csv_filename}")