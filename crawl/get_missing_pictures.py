import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import re
import csv
import os

headers = {
    'Referer':'',
    'Priority':'u=0, i',
    'sec-ch-ua-platform':'"Windows"',
    'accept-encoding':'gzip, deflate, br, zstd',
    'upgrade-insecure-requests':'1',
    'sec-ch-ua':'"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74."
}

# 读取 CSV 文件
df = pd.read_csv('updated_file1.csv')
df2 = pd.read_csv('missing_files.csv')
missing_numbers = df2['Missing File Numbers'].tolist()
for id in missing_numbers:
    image_url = df.loc[df['id'] == id, 'image'].values[0]
    headers['Referer'] = image_url
    try:
            response = requests.get(image_url)
            response.raise_for_status()  # 确保请求成功
            # 获取图像文件名
            image_name = f"images/{id}.jpg"  # 使用索引作为文件名
            with open(image_name, 'wb') as file:
                file.write(response.content)  # 写入图像内容
            print(f"Downloaded: {image_name}")
    except requests.exceptions.RequestException as e:
            print(f"{id}")
            print(f"Failed to download {image_url}: {e}")