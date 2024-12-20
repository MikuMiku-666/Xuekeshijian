from bs4 import BeautifulSoup
import requests
import json
import re
import csv
import time

origin_url = r'https://search.douban.com/movie/subject_search?search_text=%E5%8A%A8%E6%BC%AB&cat=1002&start='
headers = {
     'Cookie': 'bid=SQRXXLHP2qI; douban-fav-remind=1; _ga=GA1.1.1129136344.1710157192; _ga_RXNMP372GL=GS1.1.1710242014.4.1.1710243611.60.0.0; ll="118205"; _vwo_uuid_v2=DAEF8F79E67FAEF1E6571F43B06683CB0|421eca74481511ea5bd8bf0effdef23b; __yadk_uid=Ofz1wM91cegnNJRzYCNr2KsnXCqGf5em; dbcl2="278998371:iFI2iBp5cDU"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.27899; ck=kPhF; ap_v=0,6.0; __utma=30149280.1129136344.1710157192.1734169991.1734609532.3; __utmc=30149280; __utmz=30149280.1734609532.3.2.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.6 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
}
# headers = {
#     'Cookie':'ll="118201"; bid=8Kup7Gk9f00; douban-fav-remind=1; _pk_id.100001.8cb4=5adbc9b351b91729.1715861201.; __yadk_uid=Q73dFKTOnC05jf8IasiKRCa655dz8wlU; __utmv=30149280.28057; __gads=ID=dffbaf7dc05300a6:T=1715865462:RT=1716012761:S=ALNI_Ma8eoPPbar8Q6WwI4lgFsaks36ONg; __gpi=UID=00000e1ef803e720:T=1715865462:RT=1716012761:S=ALNI_MbyIf9n97ubP5oyqLLtEC2UpjHIgg; FCNEC=%5B%5B%22AKsRol-O-b9vBanLdQjAM_YoC0V1oPUx_3SibP8WOeftmmMLN6tV-6zcYlh8I38lg7XWZNJV-UPO1BNuHQsdXHr_5U5OTBkWJAOLFq6cW7ECU-27A7axXN4OxufKH5PND71dJEWdRK24f64cZtNerRGxUc4S90WgWg%3D%3D%22%5D%5D; _vwo_uuid_v2=DEBF790C62063ACCA207B626B530FE6C3|ba9e3dab813746d4e4accc71f2a3bb37; viewed="37016658_30406322"; push_noty_num=0; push_doumail_num=0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1734610910%2C%22https%3A%2F%2Fmovie.douban.com%2Ftop250%22%5D; __utmc=30149280; dbcl2="280572489:0M+UVp7mUHE"; ck=bE2N; frodotk_db="48c6193f25d6b04cda524bbd718410e4"; __utmz=30149280.1734613853.25.16.utmcsr=search.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/movie/subject_search; ap_v=0,6.0; __utma=30149280.301038877.1711269045.1734622449.1734662696.27; __utmb=30149280.0.10.1734662696',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
# }
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
        with open('douban_annime_plus3.csv', 'a+', newline='', encoding='utf-8-sig') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            if output_file.tell() == 0:  # 如果文件是新创建的，写入列名
                dict_writer.writeheader()
            dict_writer.writerows(movie_list)  # 写入电影数据
        movie_list.clear()  # 清空列表以便下一次循环
total = 0
start_num = 6435
while start_num <= 8000:
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
    time.sleep(2)