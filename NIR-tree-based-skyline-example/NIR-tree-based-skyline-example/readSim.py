import pandas as pd

b = pd.read_csv('result.txt', sep=' ', names=range(4))

p = []
d = []
with open('test.txt', 'r') as f:
    for line in f.readlines():
        line = line.replace("\n", "")
        p.append(line)
        c = line.split(' ')[0].split('^') + line.split(' ')[1:]
        c = list(set(c))
        d.append(c)

f.close()

v = []
for i in d:
    u = []
    for j in i:
        for l in b[[str(c).lower() == str(j).lower() for c in b[0]]].values:
            for m in l:
                u.append(m)
    v.append(list(set(u)))

g = []
for m in range(len(v)):
    print(' '.join(v[m]))
    g.append(p[m] + ' '.join(v[m]))
    # print(p[m])

df = pd.DataFrame(g)
df.to_csv('a.txt', index=False, header=False)
