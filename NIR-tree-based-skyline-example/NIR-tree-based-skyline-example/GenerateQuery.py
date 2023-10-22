'''
Arguements: -s <size>, -r <rangeLimit>, -o <outputFile>
Build a set of 100 (default size) range queries
Format:
 x_1 y_1 bitmap_1 10100...0101100
 ......
 x_m y_m bitmap_2 10001...0000110
 ......
'''
# standard libraries
import sys
import getopt
import random
# private libraries
# from datasetBuilder import random_bitmap, random_index
import linecache
import random
import codecs

def main():
    fout = codecs.open("test.txt", 'w','utf-8')
    for i in range(1,11):
        a = random.randrange(1,100) # 要读取的行数
        # print(a)
        # fh = codecs.open('businessWithoutRow.txt','rb','utf-8')
        # data = fh.read().encode("utf-8")
        theline = linecache.getline('query.txt',a)   # 获取该行的数据
        # print(theline)
        fout.write("".join(theline))
    fout.close()


if __name__ == '__main__':
    main()
