import pandas as pd

# 读取CSV文件
df = pd.read_csv('cleaned_file2.csv')

# 检查'year'列的数据类型
print("原始数据类型:", df['year'].dtype)

# 将'year'列转换为整数类型
df['year'] = df['year'].astype(int)

# 再次检查'year'列的数据类型
print("转换后数据类型:", df['year'].dtype)

# 将修改后的数据保存为新的CSV文件
df.to_csv('cleaned_file_int_year.csv', index=False)

print("'year'字段的值已成功转换为整数，并保存到'cleaned_file_int_year.csv'")