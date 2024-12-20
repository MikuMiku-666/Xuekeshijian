import pandas as pd

# 读取CSV文件
df = pd.read_csv('updated_file1.csv')

# 检查id是否连续
expected_id = df['id'].min()
for index, row in df.iterrows():
    if row['id'] != expected_id:
        print(f"ID不连续，期望的ID是{expected_id}，但找到的是{row['id']}。")
        break
    expected_id += 1

# 检查rating是否有缺失值
# 找出rating列缺失值的id
missing_rating_ids = df[df['rating'].isnull()]['id']

# 将这些id写入一个新的CSV文件
missing_rating_ids.to_csv('missing_rating_ids.csv', index=False)

print(f"缺失rating值的id已写入文件：missing_rating_ids.csv")

# 如果需要，可以将检查结果保存到新的CSV文件
# df.to_csv('checked_file.csv', index=False)