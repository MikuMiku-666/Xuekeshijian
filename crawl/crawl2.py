import csv
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd  # 导入pandas库
import json
# 设置请求头，避免被豆瓣屏蔽
headers = {
     'Cookie':'ll="118201"; bid=8Kup7Gk9f00; douban-fav-remind=1; _pk_id.100001.8cb4=5adbc9b351b91729.1715861201.; __yadk_uid=Q73dFKTOnC05jf8IasiKRCa655dz8wlU; __utmv=30149280.28057; __gads=ID=dffbaf7dc05300a6:T=1715865462:RT=1716012761:S=ALNI_Ma8eoPPbar8Q6WwI4lgFsaks36ONg; __gpi=UID=00000e1ef803e720:T=1715865462:RT=1716012761:S=ALNI_MbyIf9n97ubP5oyqLLtEC2UpjHIgg; FCNEC=%5B%5B%22AKsRol-O-b9vBanLdQjAM_YoC0V1oPUx_3SibP8WOeftmmMLN6tV-6zcYlh8I38lg7XWZNJV-UPO1BNuHQsdXHr_5U5OTBkWJAOLFq6cW7ECU-27A7axXN4OxufKH5PND71dJEWdRK24f64cZtNerRGxUc4S90WgWg%3D%3D%22%5D%5D; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1732792526%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_ses.100001.8cb4=1; __utmc=30149280; ap_v=0,6.0; _vwo_uuid_v2=DEBF790C62063ACCA207B626B530FE6C3|ba9e3dab813746d4e4accc71f2a3bb37; viewed="37016658_30406322"; __utma=30149280.301038877.1711269045.1732792527.1732795784.14; __utmz=30149280.1732795784.14.12.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); dbcl2="280572489:hOQ0nmdq4+U"; ck=n5_2; push_noty_num=0; push_doumail_num=0; __utmb=30149280.6.10.1732795784',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}

# 获取豆瓣电影Top250的前五页数据
base_url = "https://search.douban.com/movie/subject_search?search_text=%E5%8A%A8%E6%BC%AB&cat=1002"
movie_list = []
item = 0

# 发送请求获取网页内容
def get_page(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是200，将抛出HTTPError异常
        return response.text
    except requests.exceptions.HTTPError as e:
        print(f"请求错误：{e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"请求异常：{e}")
        return None
    
# 解析网页内容并提取电影信息
def parse_page(html):
    if html is None:
        print("无法获取网页内容。")
        return
    soup = BeautifulSoup(html, 'html.parser')
    # 找到所有的script标签
    scripts = soup.find_all('script')
    
    # 遍历所有script标签，找到type为"text/javascript"的标签并打印其内容
    for script in scripts:
        if script.get('type') == 'text/javascript':
            print(script)
            script_content = script.string
            break
    data =  re.search(r'window\.__DATA__\s*=\s*(.*?);\s', script_content, re.DOTALL)
    data1 = data.group(1)
    print(data1)
    # 将字符串中的Unicode转义序列转换为实际字符
    json_string = data1.encode().decode('unicode-escape')
    # print(json_string)
    # 使用json.loads()将字符串转换为Python字典
    data_dict = json.loads(json_string)
    print(json.dumps(data_dict, ensure_ascii=False, indent=4))
    for item in data_dict["items"]:
        print(item)
        title = item["title"]  # 电影标题
        link = item["url"] # 电影链接]
        rating_value = item["rating"]["count"]  # 电影评分
        director = item["abstract_2"][0]  # 导演
        actors = item["abstract_2"].split("\n")[1:] if len(item.get("abstract_2", "").split("\n")) > 1 else []  # 演员列表
        year_type = title.split(" ")[-1]  # 年份和类型
        year = re.findall(r'\d{4}', year_type)  # 提取年份
        type_ = "".join(re.findall(r'[\u4e00-\u9fa5]+', year_type))  # 提取类型（如果有）
        image = item.get("cover_url", "")  # 电影封面链接

    # 构建电影信息字典
    movie_info = {
        "title": title,
        "link": link,
        "rating": rating_value,
        "director": director,
        "actors": actors,
        "year": year[0] if year else "",
        "type": type_,
        "image": image
    }
    movie_list.append(movie_info)

# 爬取豆瓣电影Top250的所有页面
def main():
    # 遍历前5页的豆瓣Top250
    # for start in range(0, 30, 15):
        # url = f"{base_url}&start={start}"
    url = f"{base_url}&start=0"
    html = get_page(url)
    # print(html)
    parse_page(html)

    # 输出结果
    for movie in movie_list:
        print(movie)


def save_to_csv():
    keys = movie_list[0].keys()  # 获取电影数据字典的键（即列名）

    # 写入CSV文件
    with open('douban_annime.csv', 'w', newline='', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()  # 写入列名
        dict_writer.writerows(movie_list)  # 写入电影数据


# 主函数
if __name__ == "__main__":
    main()
    
    print("爬取完成，数据已保存到 douban_top250.csv")