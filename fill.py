import pandas as pd

# 指定 CSV 文件路径
file_path = r'/home/hadoop/workspace/Xuekeshijian/crawl/cleaned_file_int_year.csv'

# 读取 CSV 文件
df = pd.read_csv(file_path)

# 检查 'episode_count' 列中是否有空值，并用 0 填充
df['episode_count'] = df['episode_count'].fillna(0)

# 将修改后的 DataFrame 保存回 CSV 文件
df.to_csv(file_path, index=False)