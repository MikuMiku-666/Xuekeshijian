import pandas as pd

# 读取CSV文件
df = pd.read_csv('updated_douban_annime.csv')

# 检查id是否连续
expected_id = df['id'].min()
for index, row in df.iterrows():
    if row['id'] != expected_id:
        print(f"ID不连续，期望的ID是{expected_id}，但找到的是{row['id']}。")
        break
    expected_id += 1

# 检查year是否有缺失值
# 找出year列缺失值的id、title和douban_link
missing_rating_ids = df[df['rating'].isnull()][['id', 'title', 'douban_link']]

# 将这些id、title和douban_link写入一个新的CSV文件
missing_rating_ids.to_csv('missing_rating_ids.csv', index=False)

print(f"缺失年份的id、title和douban_link已写入文件：missing_rating_ids.csv")