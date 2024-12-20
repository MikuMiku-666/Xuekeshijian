import pandas as pd

# 读取CSV文件
df = pd.read_csv('/home/hadoop/workspace/Xuekeshijian/crawl/updated_douban_annime.csv')

# 检查年份和单集时长列，删除缺失的行
# 这里假设年份和单集时长的缺失值被表示为NaN或者空字符串
df_cleaned = df.dropna(subset=['year', 'rating'])

# 也可以使用更严格的条件来检查，比如确保年份是数字类型
# df_cleaned = df[pd.to_numeric(df['year'], errors='coerce').notnull() & pd.to_numeric(df['episode_duration'], errors='coerce').notnull()]

# 将清洗后的数据保存回CSV文件
df_cleaned.to_csv('cleaned_file.csv', index=False)