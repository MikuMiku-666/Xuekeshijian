import pandas as pd

# 读取两个CSV文件
df1 = pd.read_csv('updated_file1.csv')
df2 = pd.read_csv('douban_annime_plus.csv')  

# 从df1中删除title列
# df1.drop(columns=['title'], inplace=True)

# 将df2中的title列插入到df1中
rows_count = df1.shape[0]
df1['title'] = df2['title'][0:rows_count]

# 将修改后的DataFrame保存回CSV文件
df1.to_csv('updated_file1.csv', index=False)