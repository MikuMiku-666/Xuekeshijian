import pandas as pd
import os

df = pd.read_csv("./crawl/updated_douban_annime.csv")
df1 = df

array = []

names = []
for name in df:
    array.append(df[name]) # 每一行是一个类别
    names.append(name)
# print(array)

tmp = [[] for _ in range(len(array))]
for i in range(450):
    for j in range(len(names)):
        tmp[j].append(array[j][i])
    if (i+1) % 25 == 0:
        # print(i)
        num = ((i+1) // 25) - 1
        newcsv_name = "annimedata" + str(num) + ".csv"
        dir = {}
        for j, name in enumerate(names):
            dir[name] = tmp[j]
        dir = pd.DataFrame(dir)
        dir.to_csv("./divide/films/" + str(num) + "/" + newcsv_name, index=False, encoding="utf-8")

        tmp = [[] for _ in range(len(array))]
        
    
# print(tmp)

