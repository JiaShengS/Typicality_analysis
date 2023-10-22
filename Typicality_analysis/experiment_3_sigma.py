import time
import vptree
import numpy as np
import pandas as pd

np.set_printoptions(suppress=True)
'''
    求典型点，均值点，中心点的典型程度
    S使用均值
'''

# 定义全局遍历
K = 10
H1 = 0
points_csv = []
sum_search_time = 0


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


# 计算距离
def euclidean(point1, point2):
    return 1/3 * np.sqrt(np.mean(np.power(point2[1:3] - point1[1:3], 2))) + 1/3 * np.sqrt(np.mean(np.power(point2[3:6] - point1[3:6], 2))) + 1/3 * np.sqrt(np.mean(np.power(point2[6:] - point1[6:], 2)))


# 依靠VP-Tree获取近似解
def get_approximate_points_from_tree(points, number_h):
    global sum_search_time
    results = []
    points_len = len(points)
    sum_search_time = 0
    for i in range(points_len):
        start_search_time = time.perf_counter()
        # 获得该点的邻域元组列表
        tree_points_tuple = tree.get_all_in_range(points[i], number_h * H1 * 0.1)
        end_search_time = time.perf_counter()
        sum_search_time += end_search_time - start_search_time

        # 获得该点集合
        tree_points_list = []
        count = 0
        for y in tree_points_tuple:
            tree_points_list.append(y[1])
            if int(y[1][0]) == i + 1:
                tree_point_index = count
            count += 1
        tree_points = np.array(tree_points_list)
        tree_points_without_id = tree_points[:, 1:]


        # S = 1/3 * np.std(tree_points_without_id[:, 0:2]) / np.sqrt(2) + 1/3 * np.std(tree_points_without_id[:, 2:5]) / np.sqrt(3) + 1/3 * np.std(tree_points_without_id[:, 5:]) / np.sqrt(16)
        # H = 1.06 * S * (points_len ** (-0.2))
        # 最后一个元素是自己
        results.append(get_typicality(H1, tree_points_without_id, tree_point_index))
    return results


if __name__ == '__main__':
    file_path, use_cols = "./poiVisualize2.xlsx", [0, 3, 4, 8, 9, 10, 11]
    # for file_path in ['./poiVisualize_1.xlsx', './poiVisualize_2.xlsx', './poiVisualize_3.xlsx']:
    for file_path in ['./poiVisualize_1.xlsx']:
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


            # 构建VPTree
            tree = vptree.VPTree(points_csv, euclidean)

            # VPTree获取解
            for num_h in range(55, 201, 5):
                # 获取近似解，通过VPTree
                start_time = time.perf_counter()
                # 获取典型程度
                tree_approximate_typicality = get_approximate_points_from_tree(points_csv, num_h)
                end_time = time.perf_counter()
                approximate_tree_time = end_time - start_time - sum_search_time

                # 压缩排序，获取结果
                z2 = zip(tree_approximate_typicality, points_csv_list)
                z2 = sorted(z2, reverse=True)
                result_approximate_typicality_sorted, result_approximate_tree_points = zip(*z2)


                # 对获取到的点求全局典型程度
                points_csv_without_id = points_csv[:, 1:]
                result_approximate_tree_global_typicality = []
                for num_k in range(K):
                    point_tree_index = int(result_approximate_tree_points[num_k][0]) - 1
                    result_approximate_tree_global_typicality.append(get_typicality(H1, points_csv_without_id, point_tree_index))

                z3 = zip(result_approximate_tree_global_typicality, result_approximate_tree_points)
                z3 = sorted(z3, reverse=True)
                result_approximate_tree_global_typicality_sorted, result_approximate_tree_global_points = zip(*z3)

                # 计算典型程度和
                sum_approximate_tree_typicality = 0
                for num_k in range(K):
                    sum_approximate_tree_typicality += result_approximate_tree_global_typicality_sorted[num_k]

                # 输出
                print("在" + str(num_h * 0.1) + "h时的近似解：")
                print("----------------------------------------------------")
                approximate_tree_id = []
                for k in range(K):
                    x_index = int(result_approximate_tree_global_points[k][0]) - 1
                    x = points_csv[x_index]
                    x_num = len(tree.get_all_in_range(x, num_h * H1 * 0.1))
                    print("邻域对象个数：" + str(x_num))
                    x = points_csv_A[x_index]
                    approximate_tree_id.append("{0:05d}".format(int(x[0])))
                    print("{0:05d}".format(int(x[0])) + ":  [" + str(x[1]) + ", " + str(x[2]) + "], [" + str(int(x[3])) + ", " + str(int(x[4])) + ", " + "{:.1f}".format(x[5]) + "]", end=", [")
                    for i in range(16):
                        print(str(x[i + 6]), end=", ")
                    print("]")
                print("h参数  时间  准确率  误差率")
                print(str(num_h * 0.1) + "h", end="   ")
                # 时间
                print(approximate_tree_time, end="   ")
                # 计算准确率
                intersection_list = list(set(accurate_id).intersection(set(approximate_tree_id)))
                print('{:.2f}%'.format(len(intersection_list) / K * 100), end=" / ")
                # 误差率
                print('{:.2f}%'.format((sum_accurate_typicality - sum_approximate_tree_typicality) / sum_accurate_typicality * 100))






