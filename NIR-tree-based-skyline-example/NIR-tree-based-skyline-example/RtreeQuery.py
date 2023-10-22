'''
rtreeNN.py
Arguements: -d <datasetFile>, -q <queryFile>, -b <Bvalue>
'''
import warnings

import sys
#encoding='utf-8'
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

# standard libraries
import time
import getopt
import sys
import math
import random
# private libraries
import numpy as np
import rtreeBuilder
import Rtree
import quora
import codecs

# from gensim.models import Word2Vec
# from gensim.models.word2vec import LineSentence
# from gensim.models import word2vec
# from nltk.corpus import stopwords

# from nltk.corpus import stopwords
# noise = set(stopwords.words("english"))
global results


class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


# in a leaf, find all points which have the topk max score
def getTopK(leaf, query, k, Enough):
    global results
    query_result = []

    for point in leaf.childList:
        Scr = NodeScore(point, query)
        # print(Scr)

        query_result.append((Scr, point))

    query_result = sorted(query_result, key=lambda x: x[0], reverse=True)
    score = query_result[0][0]
    if len(query_result) > k:
        # print(query_result)
        query_result = query_result[:k]
        # print("..."*10, query_result)
        if Enough:  # 如果前一个query已经足够topk，则把results列表清空
            results.clear()
            query_result = query_result[:k]
            # print("="*10, query_result)
        results += query_result
        enough = True
        # print("!"*10, results)
        return enough
    else:
        if Enough:  # 如果前一个query已经足够topk，则把results列表清空
            results.clear()
        results += query_result
        # print("*"*10, results)
        enough = False
        return enough


def findLeaf(tupleList, query):
    while isinstance(tupleList[0][1], Rtree.Branch):

        node = tupleList[0][1]
        del tupleList[0]
        for child in node.childList:
            tupleList.append((NodeScore(child, query), child))

        tupleList = sorted(tupleList, key=lambda x: x[0], reverse=True)

    if isinstance(tupleList[0][1], Rtree.Leaf):

        return tupleList


def scoreFirst(tupleList, query, k):  # tuplelist = [(score, node)]
    global results
    enough = False
    if isinstance(tupleList[0][1], Rtree.Branch):
        node = tupleList[0][1]
        # print(node)
        del tupleList[0]
        for child in node.childList:
            # print(child)
            tupleList.append((NodeScore(child, query), child))
        # print(tupleList)
        tupleList = sorted(tupleList, key=lambda x: x[0], reverse=True)
        # print(tupleList)
    elif isinstance(tupleList[0][1], Rtree.Leaf):
        node = tupleList[0][1]
        # print("=======")
        # print(node.childList)
        # print("=======")
        del tupleList[0]
        # print(node.keywords)
        enough = getTopK(node, query, k, True)

        while not enough:
            tupleList = findLeaf(tupleList, query)
            # print(tupleList)
            node = tupleList[0][1]
            # print(k-len(results))
            enough = getTopK(node, query, k - len(results), enough)

    if enough:
        return

    # implement scoreFirst algorithm resursively
    scoreFirst(tupleList, query, k)


# 余弦相似度
def simlarity(question_1, question_2):
    # print(question_1)
    # print(question_2)
    total_questions = " ".join(question_1 + question_2)  # 输出正确
    # total_questions = total_questions.replace(",", " ")
    # print(question_1)

    # print(total_questions)
    total_questions = total_questions.replace("  ", " ")
    total_questions = total_questions.lower()
    vocab_index = quora.create_vocab(total_questions)
    for i in range(len(question_1)):
        # question_1[i] = question_1[i].replace(",", "")

        question_1[i] = question_1[i].replace("  ", " ")
        question_1[i] = question_1[i].lower()
        # question_2[i] = question_2[i].replace(",", " ")

        question_2[i] = question_2[i].replace("  ", " ")
        question_2[i] = question_2[i].lower()
        # print(question_1[i])
        #

        result = quora.compare_questions(question_1[i], question_2[i], vocab_index)
    # print(result)
    return result


def NodeScore(node, query):
    score = 0
    S1 = 0
    S_attr = 0
    # 参数
    a = 0.5
    b = 0.7
    maxSd = 200
    qA1 = 0
    qA2 = 0

    with open("query.txt", 'r') as f:
        for line in f.readlines():
            qA1 = float(line.split("^")[-2])
            qA2 = float(line.split("^")[-1])
    f.close()

    # print(qA1)
    # print(qA2)

    question1 = []
    question2 = []
    if isinstance(node, Rtree.Point):
        x = node.x
        y = node.y
        keywords = node.keywords
        # print(keywords)
        S_attr = qA1 * node.attribute[0] + qA2 * node.attribute[1]

    else:  # leaf & branch
        x = node.centre[0]
        y = node.centre[1]
        keywords = ' '.join(list(node.keywords.keys()))
        # print(keywords)
        # print(node.attribute)
        for attrtuple in node.attribute:
            temp = qA1 * attrtuple[0] + qA2 * attrtuple[1]

            if temp < S_attr:
                S_attr = temp
    # print(1-S2)
    distance = math.sqrt((query[0] - x) ** 2 + (query[1] - y) ** 2)
    # maxSd = np.max(distance)

    S_spatial = 1 - distance / maxSd
    # print(S_spatial)
    question1.append(query[2])

    # print(question1)
    question2.append(keywords)
    # print("keywords:\t", keywords)
    # print(question2)
    S_text = simlarity(question1, question2)
    # print(question1, question2, S_text)
    S1 = a * S_spatial + (1 - a) * S_text
    # print(S2)
    score = b * S1 + (1 - b) * (1-S_attr)
    # print((1 - S2))
    # print(score)
    return score


# 48.7272^9.14795^Messina Stuttgart Italian Restaurants^0.39^0.67
# 34.2^-81.839^Charlotte Restaurants

# answer all the queries using "Best First" algorithm with a given r-tree
def answerNnQueries(root, queries, k):
    global results
    resultFile = 'results.txt'
    timeStart = time.time()
    f = codecs.open(resultFile, 'w', "utf-8")
    for query in queries:
        # initialize global variables
        results = []
        # answer query
        scoreFirst([(0, root)], query, k)
        i = 0
        for resultuple in results:
            result = resultuple[1]
            # print(result.ident)
            i += 1
            f.write('top' + str(i) + ':' + str(result.ident) + "^" + str(result.x) + '^' + str(result.y) +
                    '^' + result.keywords + '^' + str(result.attribute) + "\n")
            # f.write('top' + str(i) + ':' + str(result.ident)+"\n" )
            # f.write(str(result.ident) + ",")
        f.write('\r')
    # the end time
    timeEnd = time.time()
    f.close()
    i = len(queries)
    t = (timeEnd - timeStart) * 1000
    print('TopK=', k, 'Queries finished. Average time: ' + str(t / i))


# read all queries
def readNn(queryFile):
    fileHandle = open(queryFile, 'rt')
    queries = []
    nextLine = fileHandle.readline()
    while nextLine == '\n':
        nextLine = fileHandle.readline()
    while nextLine != '':
        queries.append(getQuery(nextLine))
        nextLine = fileHandle.readline()
        while nextLine == '\n':
            nextLine = fileHandle.readline()
    fileHandle.close()
    return queries  # return一个二维列表，每一行是一个query


import pandas as pd


def readSemantic(FileName1, FileName2):
    b = pd.read_csv(FileName2, sep='@', names=range(4))
    # print(b)
    p = []
    d = []
    with open(FileName1, 'r') as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            p.append(line)
            # print(line.split(' ')[0].split('^'))
            m = line.split('^')[2:-2]   # m是查询poi的关键字部分，以空格隔开

            m = "".join(m).split(" ")   # m是单个单词
            # print("jngy",m)
            # print(line.split('@')[0].split('^')[2])
            # c = [line.split('@')[0].split('^')[2]] + m
            # print(c)
            c = list(set(m))
            # print(c)
            d.append(c)
    # print(d)
    f.close()

    v = []
    for i in d:
        u = []
        for j in i:
            # print(j)        # j是查询条件里的单个单词
            for l in b[[str(c).lower() == str(j).lower() for c in b[0]]].values:
                # print(l)    # l是语义文件中的单词
                for m in l:
                    u.append(m)
                    # print(u)    # u中进行了扩展
        v.append(list(set(u)))
    # print(v)
    # g = []
    a = ""
    for m in range(len(v)):
        # print(v[m])
        # g.append(' '.join(v[m]))
        a = ' '.join(v[m])
    # print(a)
    return a


# read a single query from a line of text
def getQuery(nextLine):
    # split the string with whitespace
    content = nextLine.strip().lower().split('^')
    while content.count('') != 0:
        content.remove('')
    result = []
    for i in [0, 1]:
        result.append(float(content[i]))
    # txt = readSemantic("queryTest.txt", "resultTest.txt")

    txt = readSemantic("query.txt", "result.txt")
    # print(txt)
    # c = content[2]+" "+txt    # 这里进行了语义扩展
    c = content[2]
    # print(c)
    c = ' '.join(list(set(c.split())))

    result.append(c)

    # result.append(txt)
    # print(result)
    return result


def main():
    datasetFile = 'business100.txt'
    #
    queryFile = 'query.txt'

    #datasetFile = 'business.txt'

    #queryFile = 'query.txt'
    Bvalue = None

    # parse arguments

    options, args = getopt.getopt(sys.argv[1:], "d:q:b:")
    for opt, para in options:
        if opt == '-d':
            datasetFile = para
        if opt == '-q':
            queryFile = para
        if opt == '-b':
            Bvalue = int(para)

    # build r-tree
    startbuild = time.time()
    root = rtreeBuilder.buildRtree(datasetFile, Bvalue)

    rtreeBuilder.checkRtree(root)
    endbuild = time.time()
    t = (endbuild - startbuild) * 1000
    print('Building time:', str(t))
    # answer NN queries
    queries = readNn(queryFile)
    # topk query
    for k in [1, 10]:
        answerNnQueries(root, queries, k)


if __name__ == '__main__':
    sys.stdout = Logger("log.txt")  # 保存到文件中
    main()



