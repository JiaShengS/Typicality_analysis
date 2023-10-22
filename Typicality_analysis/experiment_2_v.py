import time
import numpy as np
import pandas as pd

np.set_printoptions(suppress=True)
'''
    确定最优的V
    S使用均值
'''

# 定义全局遍历
K = 10
U = 10
V = 10
N = 3
H1 = 0
points_csv = []


# 读取excel文件
def get_csv_points(path, cols, rows):
    df = pd.read_excel(io=path, usecols=cols, nrows=rows)
    return df


# 获取典型程度
def get_typicality(h, points, index):
    # 典型程度值初始化
    sum_typicality = 0
    # 点的个数
    points_len = len(points)

    # 对每个点求距离
    for i in range(points_len):
        if i == index:
            continue
        distance = 0
        distance += 1/3 * np.linalg.norm(points[i][0:2] - points[index][0:2]) / np.sqrt(2)
        distance += 1/3 * np.linalg.norm(points[i][2:5] - points[index][2:5]) / np.sqrt(3)
        distance += 1/3 * np.linalg.norm(points[i][5:] - points[index][5:]) / np.sqrt(16)
        sum_typicality += np.power(np.e, (-(np.power(distance, 2) / (2 * np.power(h, 2)))))
    typicality = sum_typicality / (points_len * np.sqrt(2 * np.pi))
    return typicality


# 获取精确解
def get_accurate_points(points):
    points_without_id = points[:, 1:]
    points_len = len(points)
    # S取标准差
    S = 1/3 * np.std(points_without_id[:, 0:2]) / np.sqrt(2) + 1/3 * np.std(points_without_id[:, 2:5]) / np.sqrt(3) + 1/3 * np.std(points_without_id[:, 5:]) / np.sqrt(16)
    H = 1.06 * S * (points_len ** (-0.2))
    # 获取典型程度结果集
    results = []
    for i in range(points_len):
        results.append(get_typicality(H, points_without_id, i))
    return results, H


# 获取每组的最典型元素
def get_group_typicality_element(points):
    if len(points) == 1:
        return points[0]
    result_group = get_accurate_points(points)[0]
    result_index = result_group.index(max(result_group))
    return points[result_index]


# 获取分组的点集合
def get_group_points(total_points):
    total_points_len = len(total_points)
    # 打乱该array
    np.random.shuffle(total_points)

    # 根据U进行分组
    group_points = []

    for i in range(0, total_points_len, U):
        group_points.append(total_points[i:i + U])

    return group_points


# 获取最典型元素
def get_most_typical_element(points_list):
    # 定义候选集合c
    c = []

    # 遍历V次，得到V个候选元素
    for num_v in range(V):
        points_array = np.array(points_list)
        # 当前元素初始化
        current_points_array = points_array
        current_points_array_len = len(current_points_array)

        # 当前元素个数大于1的时候，进行分组
        while current_points_array_len > 1:
            group_points = get_group_points(current_points_array)
            # 获取组数
            group_points_len = len(group_points)

            # 临时点集合
            temp_points = []

            # 将每组的最典型元素放入临时点集合
            for j in range(group_points_len):
                temp_points.append(get_group_typicality_element(group_points[j]))

            # 将每组最典型元素放入当前元素集合
            current_points_array = np.array(temp_points)
            current_points_array_len = len(current_points_array)

        # 将该轮选出的候选元素放入集合
        c.append(current_points_array[0])

    # 将C中的元素求全局典型程度，并返回最典型元素
    results = []
    c_len = len(c)
    points_csv_without_id = points_csv[:, 1:]
    for num_c in range(c_len):
        c_index = int(c[num_c][0]) - 1
        results.append(get_typicality(H1, points_csv_without_id, c_index))
    max_result = max(results)
    max_index = results.index(max_result)
    return c[max_index], max_result


# 获取近似解
def get_approximate_points(points):
    # 先取points的list形式 因为在得到一个point后删除一个元素
    points_list = points.tolist()
    sum_typicality = 0

    # 定义目标集合s
    s = []
    # 遍历K轮，求TOP K
    for num_k in range(K):
        point_and_typicality = get_most_typical_element(points_list)
        point = point_and_typicality[0].tolist()
        typicality = point_and_typicality[1]
        # 装入目标集合
        s.append(point)
        # 求近似解的典型程度之和
        sum_typicality += typicality
        # 删除该元素
        points_list.remove(point)
    return s, sum_typicality


if __name__ == '__main__':
    file_path, use_cols = "./poiVisualize2.xlsx", [0, 3, 4, 8, 9, 10, 11]
    for file_path in ['./poiVisualize_1.xlsx', './poiVisualize_2.xlsx', './poiVisualize_3.xlsx']:
        # for file_path in ['./poiVisualize2.xlsx']:
        for max_row in [10000]:
            print("数据集大小:" + str(max_row))
            print("----------------------------------------------------")

            # 读取文件 获得DataFrame格式
            points_csv_all_A = get_csv_points(file_path, use_cols, max_row)
            # 去除最后一列的中括号,拆分最后一列为多列
            points_csv_all_A['text latent vector'] = points_csv_all_A['text latent vector'].str.replace('[', '', regex=True).str.replace(']', '', regex=True)
            points_csv_all = pd.concat([points_csv_all_A, points_csv_all_A['text latent vector'].str.split(',', expand=True).astype(float)], axis=1)
            points_csv_all.drop('text latent vector', axis=1, inplace=True)
            points_csv_A = np.array(points_csv_all).astype(float)
            max_array = np.max(points_csv_A, axis=0)
            max_array[0] = 1
            for num_index in range(16):
                max_array[6 + num_index] = 1
            # 等比例缩放
            max_array[1] = max(abs(max_array[1]), abs(max_array[2]))
            max_array[2] = max_array[1]

            # 直接缩放
            # max_array[1] = abs(max_array[1])
            # max_array[2] = abs(max_array[2])

            points_csv = points_csv_A / max_array
            # points_csv = np.array(points_csv_all).astype(float)

            '''
                获取精确解
            '''
            start_time = time.perf_counter()
            result_accurate_typicality_and_H = get_accurate_points(points_csv)
            result_accurate_typicality = result_accurate_typicality_and_H[0]
            end_time = time.perf_counter()
            accurate_time = end_time - start_time
            # 留着后序使用
            H1 = result_accurate_typicality_and_H[1]

            # 排序输出Top1的典型程度和点内容
            points_csv_list = points_csv.tolist()
            z = zip(result_accurate_typicality, points_csv_list)
            z = sorted(z, reverse=True)
            result_accurate_typicality_sorted, result_accurate_points = zip(*z)
            # 输出
            print("精准解：")
            accurate_id = []
            for k in range(K):
                x_index = int(result_accurate_points[k][0]) - 1
                x = points_csv_A[x_index]
                accurate_id.append("{0:05d}".format(int(x[0])))
                print("{0:05d}".format(int(x[0])) + ":  [" + str(x[1]) + ", " + str(x[2]) + "], [" + str(int(x[3])) + ", " + str(int(x[4])) + ", " + "{:.1f}".format(x[5]) + "]", end=", [")
                for i in range(16):
                    print(str(x[i + 6]), end=", ")
                print("]")
            print("耗时：" + str(accurate_time))
            print("----------------------------------------------------------------------")

            # 求典型程度之和
            sum_accurate_typicality = 0
            for k in range(K):
                sum_accurate_typicality += result_accurate_typicality_sorted[k]

            # 不同的V  2, 3, 4, 5, 6, 7, 8, 9, 10
            for V in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
                print("近似解：")
                print("-----------------------------------------")
                print("K = 10, U = 10, V = " + str(V) + "时的解：")
                print("-----------------------------------------------------")
                for n in range(N):
                    print("近似解" + str(n + 1) + "：")
                    print("-----------------------------------------------------")
                    start_time = time.perf_counter()
                    result_approximate_points_and_typicality = get_approximate_points(points_csv)
                    result_approximate_points = result_approximate_points_and_typicality[0]
                    sum_approximate_typicality = result_approximate_points_and_typicality[1]
                    end_time = time.perf_counter()
                    approximate_time = end_time - start_time
                    approximate_id = []
                    for k in range(K):
                        x_index = int(result_approximate_points[k][0]) - 1
                        x = points_csv_A[x_index]
                        approximate_id.append("{0:05d}".format(int(x[0])))
                        print("{0:05d}".format(int(x[0])) + ":  [" + str(x[1]) + ", " + str(x[2]) + "], [" + str(int(x[3])) + ", " + str(int(x[4])) + ", " + "{:.1f}".format(x[5]) + "]", end=", [")
                        for i in range(16):
                            print(str(x[i + 6]), end=", ")
                        print("]")
                    print("时间  准确率 / 误差率")
                    print(approximate_time, end="   ")
                    # 计算准确率
                    intersection_list = list(set(accurate_id).intersection(set(approximate_id)))
                    print('{:.2f}%'.format(len(intersection_list) / K * 100), end=" / ")
                    # 计算误差率 -- 准确 - 近似 / 准确
                    print('{:.2f}%'.format((sum_accurate_typicality - sum_approximate_typicality) / sum_accurate_typicality * 100))
                    print("----------------------------------------------------------------------")

