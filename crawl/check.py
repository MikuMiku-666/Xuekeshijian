import os

# 指定目录路径
directory = 'images'

# 获取目录下所有的.jpg文件
files = [f for f in os.listdir(directory)]

# 将文件名排序
files.sort()

# 检查文件名是否连续
expected_files = [str(i) + '.jpg' for i in range(2293)]  # 从0到2092
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