import quora
import math
import numpy as np
def simlarity(question_1,question_2):
    # print(question_1)
    # print(question_2)
    total_questions = " ".join(question_1+question_2)  # 输出正确
    # total_questions = total_questions.replace(",", " ")
    # print(total_questions)

    # print(total_questions)
    total_questions = total_questions.replace("  ", " ")
    total_questions = total_questions.lower()
    vocab_index = quora.create_vocab(total_questions)
    # print(vocab_index)
    for i in range(len(question_1)):
        # question_1[i] = question_1[i].replace(",", "")

        question_1[i] = question_1[i].replace("  ", " ")
        question_1[i] = question_1[i].lower()
        # question_2[i] = question_2[i].replace(",", " ")

        question_2[i] = question_2[i].replace("  ", " ")
        question_2[i] = question_2[i].lower()
        # print(question_1[i])
        #
        # print(vocab_index)
        result = quora.compare_questions(question_1[i], question_2[i], vocab_index)
        # print(result)
    return result


question_1 = []# 查询列表
question_2 = [] # poi文件
distance = 0
print("================距离接近度============================")
with open("queryTest.txt", 'r') as f:
    for line in f.readlines():
        line = line.replace("\n", "").split("^")
        queryx=float(line[0])
        queryy = float(line[1])


        with open("POITest.txt", 'r') as f2:
            for line2 in f2.readlines():
                line2 = line2.replace("\n", "").split("^")
                x = float(line2[1])
                y = float(line2[2])

                distance = math.sqrt((queryx - x) ** 2 + (queryy - y) ** 2)


                print("%.4f"%(1-distance/100))
        f2.close()
f.close()

print("================距离接近度============================")


print("================文本接近度============================")
question_1.append('chicken McDonalds kfc')
question_2.append('pizza steak')#1
print("%.4f"%simlarity(question_1,question_2))

question_2.clear()
question_2.append('chicken McDonalds')#2
print("%.4f"%simlarity(question_1,question_2))
question_2.clear()
question_2.append('tea coffee')#3
print("%.4f"%simlarity(question_1,question_2))
question_2.clear()
question_2.append('chicken McDonalds')#4
print("%.4f"%simlarity(question_1,question_2))

question_2.clear()
question_2.append('shopping market')#5
print("%.4f"%simlarity(question_1,question_2))
question_2.clear()
question_2.append('bars beer chicken')#6
print("%.4f"%simlarity(question_1,question_2))
question_2.clear()
question_2.append('chicken McDonalds')#7
print("%.4f"%simlarity(question_1,question_2))
question_2.clear()
question_2.append('bread sandwiches')#8
print("%.4f"%simlarity(question_1,question_2))

question_2.clear()
question_2.append('spa stylists')#9
print("%.4f"%simlarity(question_1,question_2))
print("================文本接近度============================")



l1 = [0.5,0.7]
l2 = [0.6,0.4]
l3 = [0.4,0.5]
l4 = [0.3,0.6]

l5 = [0.7,0.9]
l6 = [0.7,0.9]
l7 = [0.3,0.5]
l8 = [0.3,0.4]
l9 = [0.4,0.3]


qA1 = 0.4
qA2 = 0.6

# qA1 = 0.7
# qA2 = 0.3

# qA3 = 0.5
print("================数值接近度============================")
temp = qA1 * l1[0] + qA2 * l1[1]
print("%.4f"%(1 - temp))
temp2 = qA1 * l2[0] + qA2 * l2[1]
print("%.4f"%(1 - temp2))
temp3 = qA1 * l3[0] + qA2 * l3[1]
print("%.4f"%(1 - temp3))
temp4 = qA1 * l4[0] + qA2 * l4[1]
print("%.4f"%(1 - temp4))
temp5 = qA1 * l5[0] + qA2 * l5[1]
print("%.4f"%(1 - temp5))
temp6 = qA1 * l6[0] + qA2 * l6[1]
print("%.4f"%(1 - temp6))
temp7 = qA1 * l7[0] + qA2 * l7[1]
print("%.4f"%(1 - temp7))
temp8 = qA1 * l8[0] + qA2 * l8[1]
print("%.4f"%(1 - temp8))
temp9 = qA1 * l9[0] + qA2 * l9[1]
print("%.4f"%(1 - temp9))
print("================数值接近度============================")


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

with open("POITest.txt", 'r') as f:
    list_1 = []
    for line in f.readlines():
        line = line.replace("\n", "").split("^")[4:]
        # attr1=float(line[-3])
        # attr2 = float(line[-2])
        # attr3 = float(line[-1])
        list_1.append(line)
        # print(line)
    print(skyline(list_1))

f.close()

'''
# f2 = open("attr50.txt",'w')
f2 = open("business50withNoRow.txt",'w')
with open("business50.txt", 'r') as f:
    for line in f.readlines():
        line = line.replace("\n", "").split("^")
        attr1=line[1:]
        f2.write("^".join(attr1)+"\n")
    f.close()
f2.close()


# 34.2^-81.839^Charlotte Restaurants
queryx = 34.2
queryy = -81.839
# 48.7272^9.14795^Messina Stuttgart Italian Restaurants^0.39^0.67
x = 48.7272
y = 9.14795

distance = math.sqrt((queryx - x) ** 2 + (queryy - y) ** 2)
S_spatial = 1-distance/100#0.07860623997432581 0.07860623997432581
question_1.append('charlotte phoenix johnson pool smile motor quest tours latin restaurants pollo soccer entertainment sporting')
question_2.clear()
question_2.append('Messina Stuttgart Italian Restaurants')#2
S_text=simlarity(question_1,question_2)
print(S_text)
l8 = [0.39,0.67]


qA1 = 0.63
qA2 = 0.37
a = 0.5
b = 0.86
S2 = qA1 * l8[0] + qA2 * l8[1]
# print(1 - S2)

S1 = a * S_spatial + (1 - a) * S_text
score = b*S1+(1-b)*(1-S2)
print(score)
'''
'''
f2 = open("ssstest.txt",'w')
with open("sss.txt", 'r') as f:
    for line in f.readlines():
        line = line.replace("\n", "").split(",")
        attr1=line[:2]
        f2.write(",".join(attr1)+"\n")
    f.close()
f2.close()
'''

list1 = [0.6985,
0.9307,
0.6972,
0.9367,
0.6986,
0.0786,
0.9335,
0.6653,
0.6651]

list2 = [0.0000,
        0.8165,
        0.0000,
        0.8165,
        0.0000,
        0.3333,
        0.8165,
        0.0000,
        0.0000  ]

list3 = [
    0.3800,
    0.5200,
    0.5400,
    0.5200,
    0.1800,
    0.1800,
    0.5800,
    0.6400,
    0.6600

]

alpha = 0.5
beta = 0.7
count = 1
print("距离接近度    文本接近度   数值接近度   综合得分")
for dis,tex,att in zip(list1,list2,list3):

    s1 = alpha*dis+(1-alpha)*tex
    # print(s1,att)

    score = (beta*s1+(1-beta)*att)

    print(count, dis, tex, att, score)
    count = count+1

'''
    1 0.6985 0.0 0.38 0.358475
    2 0.9307 0.8165 0.52 0.76752
    3 0.6972 0.0 0.54 0.40602000000000005
    4 0.9367 0.8165 0.52 0.76962
    5 0.6986 0.0 0.18 0.29851
    6 0.0786 0.3333 0.18 0.19816499999999998
    7 0.9335 0.8165 0.58 0.7865
    8 0.6653 0.0 0.64 0.424855
    9 0.6651 0.0 0.66 0.43078500000000003
      7  4  2  9 8 3 1 5 6
      
      
      
      

top1:7^40.6151^-80.0913^chicken McDonalds^[0.3, 0.5]
top2:4^40.2917^-80.1049^chicken McDonalds^[0.3, 0.6]
top3:2^41.1195^-81.4757^chicken McDonalds^[0.6, 0.4]
top4:6^48.7272^9.14795^bars beer chicken^[0.7, 0.9]
top5:8^36.1975^-115.2497^bread sandwiches chicken^[0.3, 0.4]
top6:9^36.2074^-115.2685^movie drink^[0.4, 0.3]
top7:3^33.5249^-112.1153^tea coffee^[0.4, 0.5]
top8:1^33.3307^-111.9786^pizza steak^[0.5, 0.7]
top9:5^33.3831^-111.9647^shopping market^[0.7, 0.9]
top10:8^36.1975^-115.2497^bread sandwiches chicken^[0.3, 0.4]
'''


