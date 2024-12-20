import sys
import os
import argparse
import faiss
import pandas as pd
import numpy as np

movie_cnt = 8

def get_user_id():
    parser = argparse.ArgumentParser(description="Process user information.")
    parser.add_argument('-name', type=str, help='User name.')
    parser.add_argument('-id', type=int, help='User ID.')
    args = parser.parse_args()
    name_count = sys.argv.count('-name')
    id_count = sys.argv.count('-id')
    if id_count == 1 and name_count == 0:
        user_id = args.id
    else:
        print('Usage: main.py <-id userID>')
        exit(-1)
    return user_id

if __name__ == '__main__':
    user_id = get_user_id()
    faiss_P = faiss.read_index('faiss_P.index')
    user_feature = faiss_P.reconstruct(user_id - 1).reshape(1, -1)
    faiss_Q = faiss.read_index('faiss_Q.index')
    
    D, I = faiss_Q.search(user_feature, movie_cnt)
    print(I[0])  # 打印最近邻的索引
    # print(D)  # 打印与最近邻的距离