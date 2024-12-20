from bs4 import BeautifulSoup
import requests
import json
import re
import csv

origin_url = r'https://search.douban.com/movie/subject_search?search_text=%E5%8A%A8%E6%BC%AB&cat=1002&start='
headers = {
     'Cookie': 'bid=SQRXXLHP2qI; douban-fav-remind=1; _ga=GA1.1.1129136344.1710157192; _ga_RXNMP372GL=GS1.1.1710242014.4.1.1710243611.60.0.0; ll="118205"; _vwo_uuid_v2=DAEF8F79E67FAEF1E6571F43B06683CB0|421eca74481511ea5bd8bf0effdef23b; __yadk_uid=Ofz1wM91cegnNJRzYCNr2KsnXCqGf5em; dbcl2="278998371:iFI2iBp5cDU"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.27899; ck=kPhF; ap_v=0,6.0; __utma=30149280.1129136344.1710157192.1734169991.1734609532.3; __utmc=30149280; __utmz=30149280.1734609532.3.2.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.6 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
}
movie_list = []

def process_json(json_data):
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误：{e}")
        return
    # 可以选择跳过错误的数据或进行其他错误处理
    for movie in data["items"]:
        title = movie['title'].split('\u200e')[0]
        douban_link = movie['url']
        movie_info = {
            "title": title,
            "douban_link": douban_link,
        }
        movie_list.append(movie_info)

def save_to_csv():
    if movie_list:  # 如果movie_list不为空
        keys = movie_list[0].keys()  # 获取电影数据字典的键（即列名）
        with open('douban_annime_plus.csv', 'a', newline='', encoding='utf-8-sig') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            if output_file.tell() == 0:  # 如果文件是新创建的，写入列名
                dict_writer.writeheader()
            dict_writer.writerows(movie_list)  # 写入电影数据
        movie_list.clear()  # 清空列表以便下一次循环
total = 0
start_num = 1890
while start_num <= 2500:
    url = origin_url + str(start_num)
    print(url)
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        print(e)
        exit()
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script', string=re.compile(r'window\.__DATA__'))
    if script_tag:
        js_code = script_tag.string
        pattern = r'window\.__DATA__\s*=\s*(.*?);\s'
        match = re.search(pattern, js_code, re.DOTALL)
        if match:
            json_data = match.group(1)
            process_json(json_data)
            total += movie_list.__len__()
            print(movie_list.__len__())
            save_to_csv()  # 每个循环都写入CSV
        else:
            print("未找到匹配的JSON数据")
    else:
        print("未找到包含window.__DATA__的<script>标签")
    start_num += 15