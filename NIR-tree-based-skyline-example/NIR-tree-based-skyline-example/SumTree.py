# 树结点
class Node(object):
    # 初始化
    def __init__(self, data, parent=None):
        self.data = data
        self.left_node = None
        self.right_node = None
        self.parent = parent

    # 添加左孩子结点
    def addleftchild(self, node):
        if self.left_node is None:
            self.left_node = node
            node.parent = self
            self.data += node.data
        else:
            return

    # 添加右孩子结点
    def addrightchild(self, node):
        if self.right_node is None:
            self.right_node = node
            node.parent = self
            self.data += node.data
        else:
            return


# 根据输入列表生成树
def creatTree(list):
    # 如果传入的列表只有一个值，则为根结点，返回
    if list.__len__() == 1:
        return list[0]
    # 用n1来接收新生成的结点，两个结点合成为一个新结点，如果只有一个结点传入
    n1 = []
    while True:
        if list.__len__() >= 2:
            j = list.pop(0)
            k = list.pop(0)
            i = Node(0)
            i.addleftchild(j)
            i.addrightchild(k)
            n1.append(i)

        else:
            # 判断旧的列表剩余结点数，如果有一个就是直接加入新列表中
            if list.__len__() == 1:
                n1.append(list[0])
            # 递归调用生成
            return creatTree(n1)


# 先序遍历树
def xianxu(node):
    if node is None:
        return
    else:
        print(node.data)
        xianxu(node.left_node)
        xianxu(node.right_node)

# 中序遍历树
def zhongxu(node):
    if node is None:
        return
    else:
        zhongxu(node.left_node)
        print(node.data)
        zhongxu(node.right_node)

# 层次遍历树
def cengci(node):
    stack = [node]
    while stack:
        current = stack.pop(0)
        print(current.data)
        if current.left_node:
            stack.append(current.left_node)
        if current.right_node:
            stack.append(current.right_node)

#  查找数值
def search(tree, num):
    # 如果当前结点为叶子结点则返回
    if tree.left_node is None and tree.right_node is None:
        return tree.data
    # 首次判断要查找的值在不在树中，根结点代表的是最大的范围数值
    if (tree.data < num):
        print("不存在当前树中")
        return
    if tree.left_node.data >= num:
        # if tree.left_node.data > num:    判断边界值，如果边界值在左取则 用 >
        # 如 （4-13） 和（13-25） 中 13 的取值在（13-25）中
        tree = tree.left_node
        return search(tree, num)
    else:
        # 先右子树查找时需要改变num的值
        num = num - tree.left_node.data
        tree = tree.right_node
        return search(tree, num)


if __name__ == '__main__':
    # list1 用来存储分断的结点
    list1 = [3, 10, 12, 4, 1, 2, 8, 2]
    # list1 = [3, 10, 12, 4, 1, 2, 8, 2, 8, 10]
    # list1 =[3,10,7,4,6]
    # list1=[3,6,9,2,3,7]

    # list2 用来存储开始列表的初始化成结点
    list2 = []
    for i in list1:
        list2.append(Node(i))

    # 用 n来返回生成的树的根结点
    n = creatTree(list2)
    # xianxu(n)
    # cengci(n)
    print(search(n, 24))
