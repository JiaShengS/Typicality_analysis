'''
Arguements: -d <datasetFile>, -b <Bvalue>
Build a r-tree from a given data set
'''
# standard libraries
import getopt
import sys
import time
# private libraries
import Rtree
import codecs
from collections import Counter
global root
global Bvalue


# from nltk.corpus import stopwords
#
# import nltk
# nltk.download('stopwords')
# 从一个二维列表中获得skyline points
def skyline(list_attr):
    try:
        list_attr = sorted(list_attr, key=lambda x: x[0], reverse=False)
        i = 0
        for item in list_attr[1:]:
            temp = list_attr[i]
            if temp[1] <= item[1]:
                list_attr.remove(item)
                i -= 1
            i += 1
        return list_attr
    except:
        return list_attr


def handleOverFlow(node):
    global root
    global Bvalue

    # split node into two new nodes
    nodes = node.split()
    # if root node is overflow, new root need to build
    if node.paren == None:
        root = Rtree.Branch(Bvalue, node.level + 1, nodes[0])
        root.addChild(nodes[0])
        root.addChild(nodes[1])
        root.childList[0].paren = root
        root.childList[1].paren = root
    else:
        # update the parent node
        parent = node.paren
        parent.childList.remove(node)
        parent.childList += nodes
        # check whether parent node is overflow
        if parent.isOverFlow():
            handleOverFlow(parent)


# insert a point to a node
def insert(node, point):
    # if the node is a leaf, add this point
    if isinstance(node, Rtree.Leaf):
        node.addChild(point)
        if node.isOverFlow():
            handleOverFlow(node)

    # if the node is a branch, choose a child to add this point
    elif isinstance(node, Rtree.Branch):
        node.update(point)
        childNode = node.chooseChild(point)
        insert(childNode, point)
    else:
        pass


def getPoint(nextLine):
    # content[3] = [word for word in content[3] if word not in stopwords]
    # while content.count('') != 0:
    #     content.remove('')
    # point id
    content = nextLine.strip().split("^")
    ident = int(content[0])
    # print(content)
    # point id and coordinates
    x = float(content[1])
    y = float(content[2])
    # kw = content[3]
    keywords = content[3]
    attr = [float(content[4]), float(content[5])]
    # print([ident, x, y, bitmap, attr])
    return [ident, x, y, keywords, attr]


def buildRtree(dataSetName, *B):
    global root
    global Bvalue

    Bvalue = 30 # 800  # Upper limit of the node, initial 25.
    if len(B) == 1 and B[0] != None:
        Bvalue = B[0]
    f = codecs.open(dataSetName, 'r', 'utf-8')
    nextLine = f.readline()
    # nextLine = nextLine.replace("@","")

    point = Rtree.Point(getPoint(nextLine))

    # print(getPoint(nextLine))
    root = Rtree.Leaf(Bvalue, 1, point)
    root.addChild(point)
    # add the remained points
    nextLine = f.readline()
    while nextLine == '\n':
        nextLine = f.readline()
    while nextLine != '':
        point = Rtree.Point(getPoint(nextLine))
        insert(root, point)
        nextLine = f.readline()
        while nextLine == '\n':
            nextLine = f.readline()
    f.close()
    maintain(root)
    generate_key(root)
    show_Rtree(root)

    return root


def show_Rtree(root):
    print('R-tree has been built. B is:', Bvalue, '. Highest level is:', root.level)
    show_branch(root)


def show_branch(branch):
    print('第%s层:' % (branch.level), 'attribute:', branch.attribute, 'range:', branch.range,
          # '\n', 'keywords :', branch.keywords,    # 需要查看时可以取消  这里因为关键字太多 故注释掉了
          '\n', "childList:", branch.childList)
    for child in branch.childList:
        if type(child) is Rtree.Branch:
            show_branch(child)
        elif type(child) is Rtree.Leaf:
            show_leaf(child)


def show_leaf(leaf):
    print('第%s层:' % (leaf.level), 'attribute:', leaf.attribute, '\t', 'range:', leaf.range,
          # '\n','keywords:', leaf.keywords,    # 需要查看时可以取消  这里因为关键字太多 故注释掉了
          '\n','childList:', leaf.childList)
    for child in leaf.childList:
        show_point(child)


def show_point(point):
    print(point.ident, ' ', point.attribute, '\t', point.keywords)



def generate_key(root):
    if isinstance(root, Rtree.Branch):
        for child in root.childList:
            generate_key(child)
            key = list(child.keywords.keys())
            # print(key)
            for i in key:
                if i not in root.keywords:
                    root.keywords.update({i: [(root, 0)]})
            # print(root.keywords)
            for i in key:
                # print(child.keywords)
                # j=child.keywords[i]
                for j in child.keywords[i]:
                        if root.keywords[i][0][1] < j[1]:
                            root.keywords[i] = [(child, j[1])]

    if isinstance(root, Rtree.Leaf):
        for child in root.childList:
            key = child.keywords.split()
            for i in key:
                if i not in root.keywords:
                    root.keywords.update({i: []})
            result = dict(Counter(key))
            for i in result.keys():
                root.keywords[i].append((child, result[i]))


# maintain the bitmap and list of attribute
def maintain(root):
    if isinstance(root, Rtree.Node):
        for child in root.childList:
            maintain(child)
        calculate(root)


# calculate the Node's attribute
def calculate(root):
    if isinstance(root, Rtree.Node):
        for child in root.childList:
            # root.keywords = root.keywords.append(child.keywords)
            if isinstance(child, Rtree.Point):
                root.attribute.append(child.attribute)
                # root.keywords = root.keywords + " " + child.keywords
            else:
                root.attribute += child.attribute
                # root.keywords = root.keywords + " " + child.keywords
        root.attribute = skyline(root.attribute)


# check all nodes and points in a r-tree
def checkRtree(rtree):
    checkBranch(rtree)
    print('Finished checking R-tree')


# check the correctness of a leaf node in r-tree
def checkLeaf(leaf):
    # check whether a point is inside of a leaf
    def insideLeaf(x, y, parent):
        if x < parent[0] or x > parent[1] or y < parent[2] or y > parent[3]:
            return False
        else:
            return True

    # general check
    checkNode(leaf)
    # check whether each child point is inside of leaf's range
    for point in leaf.childList:
        if not insideLeaf(point.x, point.y, leaf.range):
            print('point(', point.x, point.y, 'is not in leaf range:', leaf.range)


# check the correctness of a branch node in r-tree
def checkBranch(branch):
    # check whether a branch is inside of another branch
    def insideBranch(child, parent):
        if child[0] < parent[0] or child[1] > parent[1] or child[2] < parent[2] or child[3] > parent[3]:
            return False
        else:
            return True

    # general check
    checkNode(branch)
    # check whether child's range is inside of this node's range
    for child in branch.childList:
        if not insideBranch(child.range, branch.range):
            print('child range:', child.range, 'is not in node range:', branch.range)
        # check this child
        if isinstance(child, Rtree.Branch):
            # if child is still a branch node, check recursively
            checkBranch(child)
        elif isinstance(child, Rtree.Leaf):
            # if child is a leaf node
            checkLeaf(child)


# general check for both branch and leaf node
def checkNode(node):
    global Bvalue

    length = len(node.childList)
    # check whether is empty
    if length == 0:
        print('empty node. node level:', node.level, 'node range:', node.range)
    # check whether overflow
    if length > Bvalue:
        print('overflow. node level:', node.level, 'node range:', node.range)

    # check whether the centre is really in the centre of the node's range
    r = node.range
    if (r[0] + r[1]) / 2 != node.centre[0] or (r[2] + r[3]) / 2 != node.centre[1]:
        print('wrong centre. node level:', node.level, 'node range:', node.range)
    if r[0] > r[1] or r[2] > r[3]:
        print('wrong range. node level:', node.level, 'node range:', node.range)
