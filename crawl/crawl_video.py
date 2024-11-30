import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import re
import csv
import os

headers = {
     'Cookie':'ll="118201"; bid=8Kup7Gk9f00; douban-fav-remind=1; _pk_id.100001.8cb4=5adbc9b351b91729.1715861201.; __yadk_uid=Q73dFKTOnC05jf8IasiKRCa655dz8wlU; __utmv=30149280.28057; __gads=ID=dffbaf7dc05300a6:T=1715865462:RT=1716012761:S=ALNI_Ma8eoPPbar8Q6WwI4lgFsaks36ONg; __gpi=UID=00000e1ef803e720:T=1715865462:RT=1716012761:S=ALNI_MbyIf9n97ubP5oyqLLtEC2UpjHIgg; FCNEC=%5B%5B%22AKsRol-O-b9vBanLdQjAM_YoC0V1oPUx_3SibP8WOeftmmMLN6tV-6zcYlh8I38lg7XWZNJV-UPO1BNuHQsdXHr_5U5OTBkWJAOLFq6cW7ECU-27A7axXN4OxufKH5PND71dJEWdRK24f64cZtNerRGxUc4S90WgWg%3D%3D%22%5D%5D; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1732792526%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_ses.100001.8cb4=1; __utmc=30149280; ap_v=0,6.0; _vwo_uuid_v2=DEBF790C62063ACCA207B626B530FE6C3|ba9e3dab813746d4e4accc71f2a3bb37; viewed="37016658_30406322"; __utma=30149280.301038877.1711269045.1732792527.1732795784.14; __utmz=30149280.1732795784.14.12.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); dbcl2="280572489:hOQ0nmdq4+U"; ck=n5_2; push_noty_num=0; push_doumail_num=0; __utmb=30149280.6.10.1732795784',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}

# 读取 CSV 文件
df = pd.read_csv('updated_douban_annime.csv')

# 创建一个文件夹来保存图片
os.makedirs('images', exist_ok=True)

# 提取 douban_link 列
douban_links = df['douban_link'].tolist()[321:]

# douban_links = ["https://movie.douban.com/subject/7152908/"]
# 初始化新列 video_url
# df['video_url'] = ''
# df['summary'] = ''
# df['country'] = ''
# df['language'] = ''
# df['episode_duration'] = ''
# df['episode_count'] = ''
# df['director'] = ''
# df['scriptwriter'] = ''
# df['cast'] = ''
# df['official_website'] = ''
# df['also_known_as'] = ''
# df['genre'] = ''
# df.drop(columns=['creator', 'tags'], inplace=True)      
# 打印所有链接
i = 321
# print(df.iloc[i])
for link in douban_links:
    # df.at[i,'id'] = i
    try:
        response = requests.get(link, headers=headers)
        response.encoding = "utf-8"
        # # print(response.status_code)
        # # print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        # # with open('soup.txt', 'w', encoding='utf-8') as file:
        # #         file.write(soup.prettify())
        # info = soup.find('div', id='info',recursive=True)
        # director = info.find('span', string='导演')
        # if director:
        #     df.at[i,'director'] = [a.get_text(strip=True) for a in director.find_next_sibling().find_all('a')]
        # # print(df.at[i,'director'] )
        # scriptwriter = info.find('span', string='编剧')
        # if scriptwriter:
        #     df.at[i,'scriptwriter'] = [a.get_text(strip=True) for a in scriptwriter.find_next_sibling().find_all('a')]
        # # print(df.at[i,'scriptwriter']) 
        # cast = info.find('span', string='主演')
        # if cast :
        #     df.at[i,'cast'] = [a.get_text(strip=True) for a in cast.find_next_sibling().find_all('a')]
        # # print(df.at[i,'cast'])
        # genre = info.find('span', string='类型:')
        # if genre:
        #     df.at[i,'genre'] = [span.get_text(strip=True) for span in  genre.find_all_next('span', property='v:genre')]
        # # print(df.at[i,'genre'])
        # official_website_link = info.find('span', string='官方网站:')
        # if official_website_link:  # 确保找到了 a 标签
        #     df.at[0, 'official_website'] = official_website_link.get_text(strip=True)
        # # print(df.at[i,'official_website'])
        # country = info.find('span', string='制片国家/地区:')
        # if country:
        #     df.at[i,'country'] = country.find_next_sibling(string=True).text.strip()
        # # print(df.at[i,'country'])
        # language = info.find('span', string='语言:')
        # if language:
        #     df.at[i,'language'] =  language.find_next_sibling(string=True).get_text(strip=True)
        # # print(df.at[i,'language'])
        # episode = info.find('span', string='集数:')
        # if episode:
        #     df.at[i,'episode_count'] = episode.find_next_sibling(string=True).get_text(strip=True)
        # # print(df.at[i,'episode_count'])
        # length = info.find('span', string='单集片长:')
        # if length:
        #     df.at[i,'episode_duration'] = length.find_next_sibling(string=True).get_text(strip=True)
        # length = info.find('span', string='片长:')
        # if length:
        #     df.at[i,'episode_duration'] = length.find_next_sibling(string=True).get_text(strip=True)
        # # print(df.at[i,'episode_duration'])
        # alias = info.find('span', string='又名:')
        # if alias:
        #     df.at[i,'also_known_as'] = alias.find_next_sibling(string=True).get_text(strip=True)
        # # print(df.at[i,'also_known_as'])
        summary = soup.find('span',property ='v:summary')
        # print(summary)
        if summary:
            df.at[i, 'summary'] = summary.get_text(strip=True)
        # print(df.at[i, 'summary'])
    #     # print(df.at[i, 'summary'])
    #     # print(df.iloc[i])
    #     # 查找所有 <script> 标签
    #     script_tags = soup.find_all('script')

    #     # 提取包含 reportTrack 函数的 <script> 标签内容
    #     for script in script_tags:
    #         if script.string and re.search(r'function reportTrack\(url\)', script.string):
    #             report_track_code = script.string
    #     sources = []
    #     if report_track_code:
    #         script_content = report_track_code
    #         # 使用正则表达式提取sources[1]和sources[8]
    #         sources_pattern = r'sources\[(\d+)\] = (\[.*?\]);'
    #         matches = re.findall(sources_pattern, script_content, re.DOTALL)
    #         # print(f"matches:{matches}")
    #         for index,value in matches:
    #             source_link = re.search(r'{play_link: "(.*?)", ep: "(\d+)"}', value, re.DOTALL)
    #             # print(f"value:{value}")
    #             # print(f"source_link:{source_link}")
    #             sources.append(source_link.group(1))
    #     df.at[i, 'video_url'] = sources
    #     # print(df.iloc[i])
        print('获取成功')
        df.to_csv('updated_douban_annime.csv', index=False)
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}，链接: {link}")
        df.at[i, 'video_url'] = None  # 或者其他适当的处理方式

    except Exception as e:
        print(f"发生错误: {e}，链接: {link}")
        df.at[i, 'video_url'] = None  # 或者其他适当的处理方式
    # image_url = df.at[i,'image']
    # try:
    #     response = requests.get(image_url)
    #     response.raise_for_status()  # 确保请求成功
    #     # 获取图像文件名
    #     image_name = f"images/{i}.jpg"  # 使用索引作为文件名
    #     with open(image_name, 'wb') as file:
    #         file.write(response.content)  # 写入图像内容
    #     print(f"Downloaded: {image_name}")
    # except requests.exceptions.RequestException as e:
    #     print(f"Failed to download {image_url}: {e}")
    i += 1

# 保存更新后的 DataFrame 到新的 CSV 文件
df.to_csv('updated_douban_annime.csv', index=False)