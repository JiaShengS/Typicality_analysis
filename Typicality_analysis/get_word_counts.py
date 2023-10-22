import numpy as np
import pandas as pd


# 读取excel文件
def get_csv_points(path):
    df = pd.read_csv(path, delimiter='\t',header=None)
    return df


# 获取不同的单词数
def get_word_counts(points):
    # 获取长度
    points_len = len(points)

    results = {}

    # 遍历每一个元素
    for index in range(points_len):
        # 取出来每一个元素
        str_word = points[index][0]
        # 对该元素进行大写处理，并切分
        str_list = str_word.upper().split('@')
        for word in str_list:
            if word in ['A', 'IS', 'OF']:
                continue
            results[word] = 1
    return len(results)


if __name__ == '__main__':
    # 读取文件
    file_path = "./businessKeywords.txt"
    # 读取文件 获得DataFrame格式
    points_csv_all_A = get_csv_points(file_path)
    points_csv_all = np.array(points_csv_all_A)

    word_counts = get_word_counts(points_csv_all)
    print(word_counts)
