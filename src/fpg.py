import operator
import copy
import json

class node:
    def __init__(self,letter,parent=None):
        self.letter = letter
        self.count = 0
        self.parent = parent
        self.children = {}

DATASET = "../data/msnbc"
MINSUP = 400 #10 for proof, 450 for sign, anything below 490 for covid, 400 for msnbc, 3 for utube 

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
# print(s_itemCount)

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

# temporary data

# ordered_item_set.clear()
# ordered_item_set.append(['K','E','M','O','Y'])
# ordered_item_set.append(['K','E','O','Y'])
# ordered_item_set.append(['K','E','M'])
# ordered_item_set.append(['K','M','Y'])
# ordered_item_set.append(['K','E','O'])
# s_itemCount.clear()
# s_itemCount['K'] = 5
# s_itemCount['E'] = 4
# s_itemCount['M'] = 3
# s_itemCount['O'] = 3
# s_itemCount['Y'] = 3

# temporary data ends

header_table = {}
for i in s_itemCount:
    header_table[i] = []

nodes = []
root = node('NULL')
nodes.append(root)
lstuse = 0

def insert(index,itemset,i):
    global nodes
    global lstuse
    global header_table
    curnode = nodes[index]
    curnode.count += 1
    if i == len(itemset):
        return
    letter = itemset[i]
    if letter in curnode.children:
        insert(curnode.children[letter],itemset,i+1)
    else:
        nunode = node(letter,index)
        lstuse += 1
        nodes.append(nunode)
        curnode.children[letter] = lstuse
        header_table[letter].append(lstuse)
        insert(curnode.children[letter],itemset,i+1)

for itemset in ordered_item_set:
    strt = 0
    if len(itemset) == 0:
        continue
    insert(strt,itemset,0)

conditional_pattern_base = {}
for i in s_itemCount:
    conditional_pattern_base[i] = []
    ept = []
    conditional_pattern_base[i].append(copy.deepcopy(ept))
    conditional_pattern_base[i].append(copy.deepcopy(ept))

def makePatternBase(index,base):
    global nodes
    global conditional_pattern_base
    curnode = nodes[index]
    conditional_pattern_base[curnode.letter][0].append(copy.deepcopy(base))
    conditional_pattern_base[curnode.letter][1].append(curnode.count)
    base.append(curnode.letter)
    for k in curnode.children:
        makePatternBase(curnode.children[k],base)
    base.pop()

for i in nodes[0].children:
    base = []
    makePatternBase(nodes[0].children[i],base)

frequentPatterns = {} #frozensets with support

def generate(index,base,freq,mytup,i):
    global frequentPatterns
    
    if index == len(base):
        if len(mytup) != 0:
            mytup = mytup + (i,)
            test = frozenset(mytup)
            if test in frequentPatterns:
                frequentPatterns[test] += freq
            else:
                frequentPatterns[test] = freq
        return

    copyTup1 = copy.deepcopy(mytup)
    copyTup2 = copy.deepcopy(mytup)

    # print(base[index])
    copyTup1 = copyTup1 + (base[index],)
    generate(index+1,base,freq,copyTup1,i)
    generate(index+1,base,freq,copyTup2,i)

for i in conditional_pattern_base:
    bases = conditional_pattern_base[i][0]
    freqs = conditional_pattern_base[i][1]
    for j in range(len(bases)):
        base = bases[j]
        freq = freqs[j]
        # print(base)
        mytup = ()
        generate(0,base,freq,mytup,i)

ctr = 0
for i in frequentPatterns:
    if frequentPatterns[i]>=MINSUP:
        # print("pattern is",tuple(i),"with count",frequentPatterns[i])
        ctr+=1
# print(ctr)

closedDict = {}
for i in frequentPatterns:
    if frequentPatterns[i]>=MINSUP:
        if frequentPatterns[i] in closedDict:
            closedDict[frequentPatterns[i]].append(i)
        else:
            closedDict[frequentPatterns[i]] = []
            closedDict[frequentPatterns[i]].append(i)

finalPatterns = []

for i in frequentPatterns:
    if frequentPatterns[i] >= MINSUP:
        nota = 0
        for x in closedDict[frequentPatterns[i]]:
            if i!=x and frozenset.issubset(i,x):
                nota = 1
                # print("removing",tuple(i),"due to",tuple(x))
                break
        
        if nota == 0:
            finalPatterns.append(tuple(i))

# print()
# print("closed patterns calculated")
# print()
# print(len(finalPatterns))
# finalPatterns.sort()
for i in finalPatterns:
    print(i)


# with open("fpop.txt",'w') as fp:
#     json.dump(finalPatterns,fp)

# lst = [18,143]
# lst = frozenset(lst)
# print(frequentPatterns[lst])
# print(header_table)