import json

apdata = []
with open("apop.txt",'r') as fp:
    apdata = json.load(fp)

fpdata = []
with open("fpop.txt",'r') as fp:
    fpdata = json.load(fp)

for i in range(len(apdata)):
    apdata[i] = frozenset(apdata[i])

for i in range(len(fpdata)):
    fpdata[i] = frozenset(fpdata[i])

print("For AP data")
for i in range(len(apdata)):
    found = 0
    for j in range(len(fpdata)):
        intersect = apdata[i] & fpdata[j]
        if len(intersect) == len(apdata[i]):
            found = 1
            break
    if found == 0:
        print(i+1,"not found")

print()
print()

print("For FP data")
for i in range(len(fpdata)):
    found = 0
    for j in range(len(apdata)):
        intersect = apdata[j] & fpdata[i]
        if len(intersect) == len(fpdata[i]):
            found = 1
            break
    if found == 0:
        print(i+1,"not found")