import string
import random
import csv

# 定义生成随机密码的函数
def generate_random_password(length=8):
    # 密码字符集，可以根据需要添加或删除字符，这里移除了双引号
    # characters = string.ascii_letters + string.digits + string.punctuation.replace('"', '')
    characters = string.ascii_letters + string.digits
    # 随机选择字符集中的字符来生成密码
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# 打开一个新的CSV文件用于写入
with open('usernames_and_passwords.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # 写入表头
    writer.writerow(['Username', 'Password'])
    
    # 循环生成用户名和随机密码，并写入CSV
    for i in range(500):
        username = "testusr" + str(i).zfill(3)  # 使用zfill确保用户名长度一致
        password = generate_random_password()  # 调用函数生成随机密码
        writer.writerow([username, password])