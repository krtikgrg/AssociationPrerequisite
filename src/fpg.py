import operator

class node:
    def __init__(self,letter,parent=None):
        self.letter = letter
        self.count = 1
        self.parent = parent
        self.children = {}

DATASET = "../data/sign"
MINSUP = 400

data = []
itemCount = {}


with open(DATASET,'r') as file:
    curdata = []
    for line in file:
        for word in line.split():
            num = int(word)
            if num == -2:
                data.append(curdata)
                curdata = []
            elif num != -1:
                curdata.append(num)

for i in range(len(data)):
    data[i] = list(set(data[i]))
    for j in data[i]:
        if j in itemCount:
            itemCount[j] += 1
        else:
            itemCount[j] = 1

s_itemCount = dict( sorted(itemCount.items(), key=operator.itemgetter(1),reverse=True))
# print(itemCount.items())
print(s_itemCount)

ordered_item_set = []
for j in range(len(data)):
    data[j].sort(key = lambda x : s_itemCount[x],reverse=True)
    
    nulist = []
    for i in range(0,len(data[j])):
        if s_itemCount[data[j][i]] >= MINSUP:
            nulist.append(data[j][i])
        else:
            break
    ordered_item_set.append(nulist)
    # print(ordered_item_set[len(ordered_item_set)-1])

header_table = {}
for i in s_itemCount:
    header_table[i] = []

nodes = []
root = node('NULL')
nodes.append(root)
lstuse = 0

# print(header_table)