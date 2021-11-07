import operator
import copy
import math

DATASET = "../data/proof"
MINSUP = 10 #10 for proof, 450 for sign, anything below 490 for covid, 400 for msnbc, 3 for utube 
NUMPARTIOTIONS = 2
MinSup = math.ceil(MINSUP/NUMPARTIOTIONS)

def calcHash(a,b,modVal):
    return (a*10 + b)%modVal

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
            intersect = itemset1&itemset2
            if len(intersect) == (len(itemset1)+1):
                if not checkInfrequent(intersect,previous):
                    if intersect not in nextPosib:
                        nextPosib[intersect] = 0
    return nextPosib

def apriori(partition):
    global MinSup

    frequestItemSets = [] #list of frozensets
    numTransactions = len(partition)

    modVal = numTransactions//MinSup
    modVal = modVal + (MinSup//2)
    maxK = 0

    bucket = {} #dictionary int:disctionary of frozensets to int
    bucketCtr = {}

    oneFreq = []
    dictForOne = {}
    for transaction in partition:
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
                if hashh in bucket:
                    bucketCtr[hashh] += 1
                    if itemset in bucket[hashh]:
                        bucket[hashh][itemset] += 1
                    else:
                        bucket[hashh][itemset] = 1
                else:
                    bucket[hashh] = {}
                    bucket[hashh][itemset] = 1
                    bucketCtr[hashh] = 1
    
    for item in dictForOne:
        if dictForOne[item] >= MinSup:
            frequestItemSets.append(frozenset({item}))
    
    kminus1_iteration = []

    for count in bucketCtr:
        if count >= MinSup:
            allsets = bucket[count]
            for itemset in allsets:
                if allsets[itemset] >= MinSup:
                    kminus1_iteration.append(itemset)
                    frequestItemSets.append(itemset)
    
    kposib_iteration = getNextPosibleIteration(kminus1_iteration)

    for transaction in partition:
        for posib in kposib_iteration:


        
    

    

