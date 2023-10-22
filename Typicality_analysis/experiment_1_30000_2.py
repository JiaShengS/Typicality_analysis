import time
import numpy as np
import pandas as pd

np.set_printoptions(suppress=True)
'''
    求典型点，均值点，中心点的典型程度
    S使用均值
'''

center_distance_list = []


# 读取excel文件
def get_csv_points(path, cols, rows):
    df = pd.read_excel(io=path, usecols=cols, nrows=rows)
    return df


# 获取典型程度
def get_typicality(h, points, index):
    # 典型程度值初始化
    sum_typicality = 0
    sum_distance = 0
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
        sum_distance += distance
        sum_typicality += np.power(np.e, (-(np.power(distance, 2) / (2 * np.power(h, 2)))))
    typicality = sum_typicality / (points_len * np.sqrt(2 * np.pi))
    return typicality, sum_distance


# 获取精确解
def get_accurate_points(points):
    global center_distance_list
    points_without_id = points[:, 1:]
    points_len = len(points)
    # S取标准差
    S = 1/3 * np.std(points_without_id[:, 0:2]) / np.sqrt(2) + 1/3 * np.std(points_without_id[:, 2:5]) / np.sqrt(3) + 1/3 * np.std(points_without_id[:, 5:]) / np.sqrt(16)
    H = 1.06 * S * (points_len ** (-0.2))
    # 获取典型程度结果集
    results = []
    center_distance_list = []
    for i in range(points_len):
        typicality_and_distance = get_typicality(H, points_without_id, i)
        results.append(typicality_and_distance[0])
        center_distance_list.append(typicality_and_distance[1])
    return results


if __name__ == '__main__':
    file_path, use_cols = "./poiVisualize2_30000.xlsx", [0, 3, 4, 8, 9, 10, 11]
    # 不同数据集上进行测试 500, 1000, 5000, 10000, 15000, 20000, 25000, 30000
    for max_row in [30000]:
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

        # '''
        #     获取精确解
        # '''
        # start_time = time.perf_counter()
        # result_accurate_typicality = get_accurate_points(points_csv)
        # end_time = time.perf_counter()
        # accurate_time = end_time - start_time
        # print("耗时：" + str(accurate_time))
        # # 排序输出Top1的典型程度和点内容
        # points_csv_list = points_csv.tolist()
        # z = zip(result_accurate_typicality, points_csv_list)
        # z = sorted(z, reverse=True)
        # result_accurate_typicality_sorted, result_accurate_points = zip(*z)
        #
        # # 输出
        # print("典型点的典型程度：")
        # print(result_accurate_typicality_sorted[0])
        # x_index = int(result_accurate_points[0][0]) - 1
        # x = points_csv_A[x_index]
        # print("{0:05d}".format(int(x[0])) + ":  [" + str(x[1]) + ", " + str(x[2]) + "], [" + str(int(x[3])) + ", " + str(int(x[4])) + ", " + "{:.1f}".format(x[5]) + "]", end=", [")
        # for i in range(16):
        #     print(str(x[i + 6]), end=", ")
        # print("]")
        # print("----------------------------------------------------------------------")
        #
        # '''
        #     中心点典型程度和点内容
        # '''
        # center_data_index = center_distance_list.index(min(center_distance_list))
        # # 输出
        # print("中心点的典型程度：")
        # print(result_accurate_typicality[center_data_index])
        # x = points_csv_A[center_data_index]
        # print("{0:05d}".format(int(x[0])) + ":  [" + str(x[1]) + ", " + str(x[2]) + "], [" + str(int(x[3])) + ", " + str(int(x[4])) + ", " + "{:.1f}".format(x[5]) + "]", end=", [")
        # for i in range(16):
        #     print(str(x[i + 6]), end=", ")
        # print("]")
        # print("----------------------------------------------------------------------")

        '''
            均值点典型程度和内容
        '''
        mean_data = np.mean(points_csv_A, axis=0)
        mean_data[0] = float(max_row + 1)
        points_csv_mean_A = np.row_stack((points_csv_A, mean_data))
        points_csv_mean = points_csv_mean_A / max_array

        result_accurate_typicality_mean = get_accurate_points(points_csv_mean)
        print("均值点的典型程度:")
        print(result_accurate_typicality_mean[max_row])
        x = mean_data
        print("{0:05d}".format(int(x[0])) + ":  [" + str(x[1]) + ", " + str(x[2]) + "], [" + str(int(x[3])) + ", " + str(int(x[4])) + ", " + "{:.1f}".format(x[5]) + "]", end=", [")
        for i in range(16):
            print(str(x[i + 6]), end=", ")
        print("]")
        print("----------------------------------------------------------------------")
