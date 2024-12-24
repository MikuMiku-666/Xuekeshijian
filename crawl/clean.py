import pandas as pd

# 读取CSV文件
df = pd.read_csv('/home/hadoop/workspace/Xuekeshijian/crawl/updated_douban_annime.csv')

# 检查年份和单集时长列，删除缺失的行
df_cleaned = df.dropna(subset=['year', 'rating'])
df_cleaned.to_csv('cleaned_file.csv', index=False)

