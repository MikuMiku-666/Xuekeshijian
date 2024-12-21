import pandas as pd
import ast

# 读取CSV文件
genre_dict = {}
genre_v = []
df = pd.read_csv('cleaned_file_int_year.csv')
i = 0
for genre_str in df['genre']:
    if type(genre_str) == float:
        continue
    genre = ast.literal_eval(genre_str)
    for name in genre:
        if genre_dict.get(name) == None:
            genre_dict[name] = 1
            genre_v.append(name)
with open('genre_list.txt', 'w') as f:
    for item in genre_v:
        f.write(f'{item}\n')