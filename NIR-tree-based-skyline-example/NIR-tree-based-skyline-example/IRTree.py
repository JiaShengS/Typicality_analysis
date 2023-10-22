'''tfidf构建节点的的倒排文件'''
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer

cv = TfidfVectorizer()
f = open("POITest.txt",'r')
keywords = []
for line in f.readlines():
    line = line.strip().split("^")
    keywords.append("".join(line[-3:-2]))
# print((keywords))

cv_fit = cv.fit_transform(keywords)

print(cv.vocabulary_)
print(cv_fit)
# cv_fit （0，12）第0个文档出现关键字9 的频率
print(cv_fit.toarray())


















