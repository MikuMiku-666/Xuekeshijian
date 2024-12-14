import pandas as pd
import os
import shutil

df = pd.read_csv("./crawl/updated_douban_annime.csv")

array = []

names = []
for name in df:
    array.append(df[name]) # 每一行是一个类别
    names.append(name)
# print(array)

tmp = []
for i in range(450):
    tmp.append(i)
    if (i+1) % 25 == 0:
        # print(i)
        num = ((i+1)//25) - 1
        if not os.path.exists("./divide/films/" + str(num) + "/imgs"):
            os.mkdir("./divide/films/" + str(num) + "/imgs")
        # num = ((i+1) // 25) - 1
        for j in tmp:
            shutil.copy("./crawl/images/" + str(j) + ".jpg", 
                        "./divide/films/" + str(num) + "/imgs/" + str(j) + ".jpg")
        tmp = []

