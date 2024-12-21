import csv
import chardet

def is_valid_utf8(string):
    try:
        string.encode('utf-8')
    except UnicodeEncodeError:
        return False
    return True

def clean_invalid_utf8(data):
    cleaned_data = []
    for row in data:
        new_row = []
        for item in row:
            if isinstance(item, bytes) and not is_valid_utf8(item.decode('utf-8', 'ignore')):
                # 尝试修复无效的UTF-8字符
                cleaned_item = item.decode('utf-8', 'ignore')
                new_row.append(cleaned_item)
            else:
                new_row.append(item)
        cleaned_data.append(new_row)
    return cleaned_data

# 读取CSV文件并检测编码
with open('cleaned_file.csv', 'rb') as file:
    result = chardet.detect(file.read(10000))  # 读取前10000字节进行编码检测
    file.seek(0)  # 重置文件指针

# 根据检测到的编码读取CSV文件
encoding = result['encoding']
with open('cleaned_file.csv', 'r', encoding=encoding) as file:
    reader = csv.reader(file)
    data = list(reader)

# 清理无效的UTF-8字符
cleaned_data = clean_invalid_utf8(data)

# 保存清理后的数据到新的CSV文件
with open('cleaned_file2.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(cleaned_data)

print("CSV文件已清理并保存为 'cleaned_file2.csv'")