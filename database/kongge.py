import csv

def check_password_spaces(filename):
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 2:
                print("行格式不正确:", row)
                continue
            
            username, password = row[0], row[1]
            if password.startswith(' ') or password.endswith(' '):
                print(f"用户名: {username} 的密码两侧有空格。")
            else:
                print(f"用户名: {username} 的密码没有空格。")

if __name__ == "__main__":
    check_password_spaces('/home/hadoop/workspace/Xuekeshijian/database/usernames_and_passwords.csv')