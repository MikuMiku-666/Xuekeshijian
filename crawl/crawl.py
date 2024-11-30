from bs4 import BeautifulSoup
import requests
import json
import re
import csv
# import pymysql.cursors
origin_url = r'https://search.douban.com/movie/subject_search?search_text=%E5%8A%A8%E6%BC%AB&cat=1002&start='
start_num = 0

headers = {
     'Cookie':'ll="118201"; bid=8Kup7Gk9f00; douban-fav-remind=1; _pk_id.100001.8cb4=5adbc9b351b91729.1715861201.; __yadk_uid=Q73dFKTOnC05jf8IasiKRCa655dz8wlU; __utmv=30149280.28057; __gads=ID=dffbaf7dc05300a6:T=1715865462:RT=1716012761:S=ALNI_Ma8eoPPbar8Q6WwI4lgFsaks36ONg; __gpi=UID=00000e1ef803e720:T=1715865462:RT=1716012761:S=ALNI_MbyIf9n97ubP5oyqLLtEC2UpjHIgg; FCNEC=%5B%5B%22AKsRol-O-b9vBanLdQjAM_YoC0V1oPUx_3SibP8WOeftmmMLN6tV-6zcYlh8I38lg7XWZNJV-UPO1BNuHQsdXHr_5U5OTBkWJAOLFq6cW7ECU-27A7axXN4OxufKH5PND71dJEWdRK24f64cZtNerRGxUc4S90WgWg%3D%3D%22%5D%5D; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1732792526%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_ses.100001.8cb4=1; __utmc=30149280; ap_v=0,6.0; _vwo_uuid_v2=DEBF790C62063ACCA207B626B530FE6C3|ba9e3dab813746d4e4accc71f2a3bb37; viewed="37016658_30406322"; __utma=30149280.301038877.1711269045.1732792527.1732795784.14; __utmz=30149280.1732795784.14.12.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); dbcl2="280572489:hOQ0nmdq4+U"; ck=n5_2; push_noty_num=0; push_doumail_num=0; __utmb=30149280.6.10.1732795784',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}
movie_list = []
def process_json(json_data):
    data = json.loads(json_data)
    for movie in data["items"]:
         # 提取基本信息
        title = movie['title'].split('\u200e')[0]  # 只取\u200e前面的部分
        # print(title)
        douban_link = movie['url']
        # print(douban_link)
        rating_value = movie['rating']['value']
        # print(rating_value)
        creator = movie['abstract_2']
        # print(creator)
        cover_url = movie['cover_url'].replace("&#39;", "'")  # 修复URL中的HTML实体
        # print(cover_url)
        # 提取年份和类型
        year_type = "".join(re.search(r'\((\d{4})\)', movie['title']).group(1))
        # print(year_type)
        type_ = movie['abstract'].split('\u200e')[0]
        # 使用split方法以'/'为分隔符分割字符串
        tags = type_.split(' / ')
        # country = tags[0]
        # 排除第一个和最后三个标签
        filtered_tags = tags[1:-3]
        # print(filtered_tags)
        id = movie['id']
        # play_link ="".join(re.search(r"onclick='moreurl\(this,\{.*?subject_id:\'(\d+).*?\}.*?\)'", movie["more_url"]).group(1))
        # print(play_link)
        # 构建电影信息字典
        movie_info = {
            'id': id,
            "title": title,
            "douban_link": douban_link,
            "rating": rating_value,
            "country": country,
            "creator": creator,
            "year": year_type if year_type else "",
            "tags": filtered_tags,
            # "play_link": play_link,
            "image": cover_url
        }
        # print(movie_info)
        movie_list.append(movie_info)
def save_to_csv():
    keys = movie_list[0].keys()  # 获取电影数据字典的键（即列名）

    # 写入CSV文件
    with open('douban_annime.csv', 'w', newline='', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()  # 写入列名
        dict_writer.writerows(movie_list)  # 写入电影数据

while start_num <= 600:
    url = origin_url + str(start_num)
    print(url)
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        print(e)
        exit()
    response.encoding = "utf-8"
    # print(response.status_code)
    # print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    
        # 查找包含window.__DATA__的<script>标签
    script_tag = soup.find('script', string=re.compile(r'window\.__DATA__'))
    
    if script_tag:
        # 提取JavaScript代码
        js_code = script_tag.string
        
        # 使用正则表达式匹配JSON数据
        # import re
        pattern = r'window\.__DATA__\s*=\s*(.*?);\s'

        match = re.search(pattern, js_code, re.DOTALL)
        # print(match)
        if match:
            json_data = match.group(1)
            process_json(json_data)
            print(movie_list.__len__())
        else:
            print("未找到匹配的JSON数据")
    else:
        print("未找到包含window.__DATA__的<script>标签")
    start_num += 15

save_to_csv()
