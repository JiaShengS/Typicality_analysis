import numpy as np

if __name__ == '__main__':
    points = [[1,3],[2,-4],[-3,9]]
    points_arr = np.array(points)
    print(points_arr)
    print(np.abs(points_arr))