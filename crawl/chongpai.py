import os
import shutil
import pandas as pd

# CSV文件路径
csv_path = '/home/hadoop/workspace/Xuekeshijian/crawl/cleaned_file.csv'
# 图片文件夹路径
images_folder = '/home/hadoop/workspace/Xuekeshijian/crawl/images'

# 读取CSV文件
df = pd.read_csv(csv_path)

# 假设原始ID列名为'id'
# 创建一个新的DataFrame来保存新的ID和旧ID的映射
new_ids = list(range(1, len(df) + 1))
df['new_id'] = new_ids
id_mapping = dict(zip(df['id'], new_ids))

id_set = set(df['id'])  # 将ID列转换为集合以提高查找效率

# 遍历图片文件夹
cnt = 0

for filename in os.listdir(images_folder):
    # 检查文件是否是.jpg格式，并且以数字开头（表示ID）
    if filename.endswith('.jpg') and filename.split('.')[0].isdigit():
        old_id = int(filename.split('.')[0])
        old_id += 1
        if old_id not in id_set:
            if os.path.exists(os.path.join(images_folder, filename)):
                os.remove(os.path.join(images_folder, filename))

for filename in os.listdir(images_folder):
    cnt = cnt + 1
    # 检查文件是否是.jpg格式，并且以数字开头（表示ID）
    if filename.endswith('.jpg') and filename.split('.')[0].isdigit():
        old_id = int(filename.split('.')[0])
        new_id = cnt
            # 重命名文件
        old_filepath = os.path.join(images_folder, filename)
        new_filename = f'{new_id}.jpg'
        new_filepath = os.path.join(images_folder, new_filename)
        os.rename(old_filepath, new_filepath)
      

# 将新的ID列替换为原始的ID列，并写回CSV文件
df['id'] = df['new_id']
df.drop(columns=['new_id'], inplace=True)
df.to_csv(csv_path, index=False)

print("ID重排和图片处理完成。")