import csv

def find_max_lengths(input_file):
    with open(input_file, 'r', newline='') as file:
        reader = csv.reader(file)
        
        # 初始化一个列表，用于存储每个字段的最大长度，初始值为0
        max_lengths = [0] * len(next(reader))  # 假设第一行是标题行，获取字段数量

        # 遍历CSV文件的每一行
        for row in reader:
            # 检查当前行是否有足够的字段
            if len(row) != len(max_lengths):
                print(f"Warning: Row with unexpected number of fields. Expected {len(max_lengths)}, got {len(row)}.")
                continue
            
            # 对于每个字段，更新最大长度
            for i, field in enumerate(row):
                # 移除字段值两端的双引号（如果有）
                stripped_field = field.strip('"')
                # 更新该字段的最大长度
                max_lengths[i] = max(max_lengths[i], len(stripped_field))

    return max_lengths

# 调用函数计算每个字段的最大长度
input_csv = '/home/hadoop/workspace/Xuekeshijian/crawl/updated_douban_annime.csv'  # 输入文件名
max_lengths = find_max_lengths(input_csv)

# 打印每个字段的最大长度
print("Maximum lengths for each field:")
for i, length in enumerate(max_lengths):
    print(f"Field {i+1}: {length}")