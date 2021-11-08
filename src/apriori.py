import operator
import copy
import math

DATASET = "../data/proof"
MINSUP = 3 #10 for proof, 450 for sign, anything below 490 for covid, 400 for msnbc, 3 for utube 
NUMPARTIOTIONS = 4
MinSup = math.ceil(MINSUP/NUMPARTIOTIONS)

def calcHash(a,b,modVal):
    c = ord(a)
    d = ord(b)
    reval = (c*10 + d)%modVal
    # print("hash ",reval) 
    return reval

def checkInfrequent(itemset,previous):
    cpy = copy.deepcopy(itemset)
    cpy = list(cpy)

    for i in range(len(cpy)):
        temp = []
        for j in range(len(cpy)):
            if i!=j:
                temp.append(cpy[j])
        
        nu = copy.deepcopy(temp)
        nu = frozenset(nu)
        if nu not in previous:
            return True
    return False


def getNextPosibleIteration(previous):
    nextPosib = {}
    for itemset1 in previous:
        for itemset2 in previous:
            # print(itemset1,"itemset1")
            # print(itemset2,"itemset2")
            intersect = itemset1|itemset2
            # print(intersect,"intersect")
            # print()
            if len(intersect) == (len(itemset1)+1):
                # print("intersect ",intersect)
                if not checkInfrequent(intersect,previous):
                    # print("Wohoo",intersect)
                    if intersect not in nextPosib:
                        nextPosib[intersect] = 0
    return nextPosib

def apriori(partition): #all transactions in partition have unique items only
    global MinSup

    frequentItemSets = [] #list of frozensets
    numTransactions = len(partition)

    modVal = numTransactions//MinSup
    modVal = modVal + (MinSup//2)
    maxK = 0

    bucket = {} #dictionary int:disctionary of frozensets to int
    bucketCtr = {}

    oneFreq = []
    dictForOne = {}
    for transaction in partition:
        # print(transaction)
        maxK = max(maxK,len(transaction))
        for item in transaction:
            if item in dictForOne:
                dictForOne[item] += 1
            else:
                dictForOne[item] = 1
        
        for i in range(len(transaction)):
            for j in range(i+1,len(transaction)):
                a = transaction[i]
                b = transaction[j]
                itemset = frozenset({transaction[i],transaction[j]})
                hashh = calcHash(a,b,modVal)
                # print(hashh)
                if hashh in bucketCtr:
                    # print("hash found")
                    bucketCtr[hashh] += 1
                    if itemset in bucket[hashh]:
                        bucket[hashh][itemset] += 1
                    else:
                        bucket[hashh][itemset] = 1
                else:
                    # print("Hash not found")
                    bucket[hashh] = {}
                    bucket[hashh][itemset] = 1
                    bucketCtr[hashh] = 1
    # closedDist = {}

    for item in dictForOne:
        if dictForOne[item] >= MinSup:
            # print("Adding ",item)
            frequentItemSets.append(frozenset({item}))
            # if dictForOne[item] not in closedDist:
            #     closedDist[dictForOne[item]] = []
            # closedDist[dictForOne[item]].append(frozenset({item}))
    
    kminus1_iteration = []

    for count in bucketCtr:
        # print(count)
        if bucketCtr[count] >= MinSup:
            allsets = bucket[count]
            for itemset in allsets:
                if allsets[itemset] >= MinSup:
                    kminus1_iteration.append(itemset)
                    frequentItemSets.append(itemset)
                    # print("adding ",itemset)
                    # if allsets[itemset] not in closedDist:
                    #     closedDist[allsets[itemset]] = []
                    # closedDist[allsets[itemset]].append(itemset)
    

    for iterate in range(3,maxK+1):
        # print("running for ",iterate)
        if len(kminus1_iteration) == 0:
            break
        kposib_iteration = getNextPosibleIteration(kminus1_iteration)
        # print(kposib_iteration)

        for transaction in partition:
            tempoSet = frozenset(transaction)
            for posib in kposib_iteration:
                if frozenset.issubset(posib,tempoSet):
                    kposib_iteration[posib] += 1
        kminus1_iteration = []
        for aset in kposib_iteration:
            if kposib_iteration[aset]>=MinSup:
                # print("adding",aset)
                kminus1_iteration.append(aset)
                frequentItemSets.append(aset)
                # if kposib_iteration[aset] not in closedDist:
                #     closedDist[kposib_iteration[aset]] = []
                # closedDist[kposib_iteration[aset]].append(aset)
    
    return frequentItemSets

data = []

# data = [
#     ['M','O','N','K','E','Y'],
#     ['D','O','N','K','E','Y'],
#     ['M','A','K','E'],
#     ['M','U','C','K','Y'],
#     ['C','O','O','K','I','E']
# ]
# for i in range(len(data)):
#     data[i] = list(set(data[i]))

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

if NUMPARTIOTIONS>len(data):
    NUMPARTIOTIONS = len(data)//2

partitions = []
for i in range(NUMPARTIOTIONS):
    partition = []
    partitions.append(partition)

partition = 0
for i in range(len(data)):
    partitions[partition].append(data[i])
    partition += 1
    partition = partition%NUMPARTIOTIONS

allPosibFrequent = {}

for partition in range(NUMPARTIOTIONS):
    fst = apriori(partitions[partition])
    for aset in fst:
        if aset not in allPosibFrequent:
            allPosibFrequent[aset] = 0


    
        
    
    


        
    

    

