import faiss
import pandas as pd
import numpy as np

# 从文件加载索引
user_feature_matrix = faiss.read_index("faiss_P.index")
object_feature_matrix = faiss.read_index("faiss_Q.index")
df = pd.read_csv('/home/hadoop/workspace/Xuekeshijian/cleaned_file_int_year.csv')

# 获取 rating 列
rating_column = df['rating'].values  # 将 pandas Series 转换为 numpy 数组

# 获取 object_feature_matrix 的维度
d = object_feature_matrix.d

# 重建 object_feature_matrix 中的所有向量
object_features = np.empty((object_feature_matrix.ntotal, d), dtype=np.float32)
object_feature_matrix.reconstruct_n(0, object_feature_matrix.ntotal, object_features)
original_features, residuals, rank, s = np.linalg.lstsq(object_features, rating_column, rcond=None)
original_features = original_features.reshape(1,-1)
# # 检查 original_features 的形状
# print(original_features.shape)
# # 检查索引中的向量维度
# print(user_feature_matrix.d)
# 将 weighted_features 添加到 user_feature_matrix 中
for i in range(10):
    user_feature_matrix.add(original_features)  # add 方法会返回新的索引
print(user_feature_matrix.ntotal)
faiss.write_index(user_feature_matrix, "faiss_P.index")

index = faiss.IndexFlatL2(user_feature_matrix.d)  # 创建索引
index.add(original_features)
faiss.write_index(index,"faiss_original.index")