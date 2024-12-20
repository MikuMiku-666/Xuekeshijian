import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import re
import csv
import os

headers = {
     'Cookie': 'bid=SQRXXLHP2qI; douban-fav-remind=1; _ga=GA1.1.1129136344.1710157192; _ga_RXNMP372GL=GS1.1.1710242014.4.1.1710243611.60.0.0; ll="118205"; _vwo_uuid_v2=DAEF8F79E67FAEF1E6571F43B06683CB0|421eca74481511ea5bd8bf0effdef23b; __yadk_uid=Ofz1wM91cegnNJRzYCNr2KsnXCqGf5em; dbcl2="278998371:iFI2iBp5cDU"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.27899; ck=kPhF; ap_v=0,6.0; __utma=30149280.1129136344.1710157192.1734169991.1734609532.3; __utmc=30149280; __utmz=30149280.1734609532.3.2.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.6 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
}

# 读取 CSV 文件
df = pd.read_csv('missing_year_ids.csv')

# 创建一个文件夹来保存图片
# os.makedirs('images', exist_ok=True)

# 提取 douban_link 列
# print(df['douban_link'].tolist()[894])
# print(df.at[0,'title'])
# print(df.at[1,'title'])
douban_links = df['douban_link'].tolist()
# douban_links = ["https://movie.douban.com/subject/7152908/"]
# 初始化新列 video_url
df['id'] = ''
df['rating'] = ''
df['year'] = ''
df['image'] = ''
df['video_url'] = ''
df['summary'] = ''
df['country'] = ''
df['language'] = ''
df['episode_duration'] = ''
df['episode_count'] = ''
df['director'] = ''
df['scriptwriter'] = ''
df['cast'] = ''
df['official_website'] = ''
df['also_known_as'] = ''
df['genre'] = ''
# df.drop(columns=['creator', 'tags'], inplace=True)      
# 打印所有链接
# print(df.iloc[i])
i = 0
for link in douban_links:
    df.at[i,'id'] = i
    try:
        response = requests.get(link, headers=headers)
        response.encoding = "utf-8"
        print(response.status_code)
        # print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        # with open('soup.txt', 'w', encoding='utf-8') as file:
        #         file.write(soup.prettify())
        info = soup.find('div', id='info',recursive=True)
        director = info.find('span', string='导演')
        if director:
            df.at[i,'director'] = [a.get_text(strip=True) for a in director.find_next_sibling().find_all('a')]
        # print(df.at[i,'director'] )
        scriptwriter = info.find('span', string='编剧')
        if scriptwriter:
            df.at[i,'scriptwriter'] = [a.get_text(strip=True) for a in scriptwriter.find_next_sibling().find_all('a')]
        # print(df.at[i,'scriptwriter']) 
        cast = info.find('span', string='主演')
        if cast :
            df.at[i,'cast'] = [a.get_text(strip=True) for a in cast.find_next_sibling().find_all('a')]
        # print(df.at[i,'cast'])
        genre = info.find('span', string='类型:')
        if genre:
            df.at[i,'genre'] = [span.get_text(strip=True) for span in  genre.find_all_next('span', property='v:genre')]
        # print(df.at[i,'genre'])
        official_website_link = info.find('span', string='官方网站:')
        if official_website_link:  # 确保找到了 a 标签
            df.at[0, 'official_website'] = official_website_link.get_text(strip=True)
        # print(df.at[i,'official_website'])
        country = info.find('span', string='制片国家/地区:')
        if country:
            df.at[i,'country'] = country.find_next_sibling(string=True).text.strip()
        # print(df.at[i,'country'])
        language = info.find('span', string='语言:')
        if language:
            df.at[i,'language'] =  language.find_next_sibling(string=True).get_text(strip=True)
        # print(df.at[i,'language'])
        episode = info.find('span', string='集数:')
        if episode:
            df.at[i,'episode_count'] = episode.find_next_sibling(string=True).get_text(strip=True)
        # print(df.at[i,'episode_count'])
        length = info.find('span', string='单集片长:')
        if length:
            df.at[i,'episode_duration'] = length.find_next_sibling(string=True).get_text(strip=True)
        length = info.find('span', string='片长:')
        if length:
            df.at[i,'episode_duration'] = length.find_next_sibling(string=True).get_text(strip=True)
        # # print(df.at[i,'episode_duration'])
        alias = info.find('span', string='又名:')
        if alias:
            df.at[i,'also_known_as'] = alias.find_next_sibling(string=True).get_text(strip=True)
        # # print(df.at[i,'also_known_as'])
        summary = soup.find('span',property ='v:summary')
        # print(summary)
        if summary:
            df.at[i, 'summary'] = summary.get_text(strip=True)
        rating = soup.find('strong', class_='ll rating_num')
        if rating:
            df.at[i, 'rating'] = rating.get_text(strip=True)
        year = soup.find('span', class_='year')
        if year:
            df.at[i, 'year'] = year.get_text(strip=True).replace('(', '').replace(')', '')
        title = soup.find('span', class_='v:itemreviewed')
        if title:
            df.at[i, 'title'] = title.get_text(strip=True)
        # print(df.at[i, 'summary'])
        # print(df.at[i, 'summary'])
        # print(df.iloc[i])
        # 查找所有 <script> 标签
        script_tags = soup.find_all('script')

        # 提取包含 reportTrack 函数的 <script> 标签内容
        for script in script_tags:
            if script.string and re.search(r'function reportTrack\(url\)', script.string):
                report_track_code = script.string
        sources = []
        if report_track_code:
            script_content = report_track_code
            # 使用正则表达式提取sources[1]和sources[8]
            sources_pattern = r'sources\[(\d+)\] = (\[.*?\]);'
            matches = re.findall(sources_pattern, script_content, re.DOTALL)
            # print(f"matches:{matches}")
            for index,value in matches:
                source_link = re.search(r'{play_link: "(.*?)", ep: "(\d+)"}', value, re.DOTALL)
                # print(f"value:{value}")
                # print(f"source_link:{source_link}")
                sources.append(source_link.group(1))
        df.at[i, 'video_url'] = sources

        # print(df.iloc[i])
        print('获取成功')
        # df.to_csv('updated_douban_annime.csv', index=False)
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}，链接: {link}")
        df.at[i, 'video_url'] = None  # 或者其他适当的处理方式

    except Exception as e:
        print(f"发生错误: {e}，链接: {link}")
        df.at[i, 'video_url'] = None  # 或者其他适当的处理方式

    # image_url = df.at[i,'image']
    # 查找包含图片链接的div，根据你的HTML结构，使用id来定位
    mainpic_div = soup.find('div', id='mainpic')

    # 提取img标签的src属性，即图片链接
    if mainpic_div:
        img_tag = mainpic_div.find('img')
        if img_tag and 'src' in img_tag.attrs:
            image_url = img_tag['src']
            df.at[i,'image'] = image_url
            print(f'图片链接：{image_url}')
        else:
            print('没有找到图片链接')
    else:
        print('没有找到指定的div')
    with open('updated_file2.csv', 'a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(['id','title', 'douban_link', 'rating','year','image','video_url', 'summary', 'country', 'language', 'episode_duration', 'episode_count', 'director', 'scriptwriter', 'cast', 'official_website', 'also_known_as', 'genre'])
            writer.writerow([df.at[i, 'id'], df.at[i,'title'],link,df.at[i,'rating'],df.at[i,'year'],df.at[i,'image'],df.at[i, 'video_url'], df.at[i, 'summary'], df.at[i, 'country'], df.at[i, 'language'], df.at[i, 'episode_duration'], df.at[i, 'episode_count'], df.at[i, 'director'], df.at[i, 'scriptwriter'], df.at[i, 'cast'], df.at[i, 'official_website'], df.at[i, 'also_known_as'], df.at[i, 'genre']])
            print("写入成功")
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
# df.to_csv('updated_douban_annime.csv', index=False)