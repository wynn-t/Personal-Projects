import random
def unsort(l):
    l=list(l)
    for i in range(len(l)-1, -1, -1):l+=[l.pop(random.randint(0, i))]
    return l
def sort1(l, stats=False): # Merge sort with pre-processing??? not sure what I was doing, this is extremely inefficient (comments added in like 2 years after I initially wrote this code)
    if len(l)<2:
        print("List already sorted.")
        return l
    original, l, temp, count=list(l), list(l), [], 0
    while len(l)>0 and count<10**6:
        count+=1
        done=False
        for i in temp:
            if l[0]>=i[-1]:
                i+=[l.pop(0)]
                done=True
                break
        if not done:temp+=[[l.pop(0)]]
    if len(temp)==1:l=temp
    while len(temp)>1 and count<10**6:
        l=[]
        for i in range(0, len(temp)-len(temp)%2, 2):
            l+=[[]]
            while len(temp[i])>0<len(temp[i+1]):
                if temp[i][0]==temp[i+1][0]:l[-1]+=[temp[i].pop(0), temp[i+1].pop(0)]
                elif temp[i][0]<temp[i+1][0]:l[-1]+=[temp[i].pop(0)]
                else:l[-1]+=[temp[i+1].pop(0)]
                count+=1
            l[-1]+=temp[i]+temp[i+1]
        if len(temp)%2==1:l+=[temp[-1]]
        temp=l
    if stats: # editing note: using ==sorted(original) is inefficient as it is possible to check "sortedness" in linear time but I am not replacing this as it better showcases the thought process I went through at the time of creating this
        if l[0]==sorted(original):print("Successfully sorted list in", count, "steps.")
        else:print("Sorting unsuccessful.")
    return l[0]
def sort2(l, stats=False): # Merge sort (reinvented)
    if len(l)<2:
        print("List already sorted.")
        return l
    original, temp, count=list(l), [[l[i]] for i in range(len(l))], 0
    while len(temp)>1 and count<10**6:
        l=[]
        for i in range(0, len(temp)-len(temp)%2, 2):
            l+=[[]]
            while len(temp[i])>0<len(temp[i+1]):
                count+=1
                if temp[i][0]==temp[i+1][0]:l[-1]+=[temp[i].pop(0), temp[i+1].pop(0)]
                elif temp[i][0]<temp[i+1][0]:l[-1]+=[temp[i].pop(0)]
                else:l[-1]+=[temp[i+1].pop(0)]
            l[-1]+=temp[i]+temp[i+1]
        if len(temp)%2==1:l+=[temp[-1]]
        temp=l
    if stats:
        if l[0]==sorted(original):print("Successfully sorted list in", count, "steps.")
        else:print("Sorting unsuccessful.")
    return l[0]
def sort3(l, stats=False): # Quicksort
    if len(l)<2:
        print("List already sorted.")
        return l
    original, temp, length, count=list(l), [list(l)], len(l), 0
    while len(temp)<length and count<10**6:
        l=[]
        for i in temp:
            if len(i)==1:
                l+=[i]
                continue
            num=i.pop(0)
            smaller, same, larger=[], [[num]], []
            for j in range(len(i)):
                count+=1
                if i[j]<num:smaller+=[i[j]]
                elif i[j]>num:larger+=[i[j]]
                else:same+=[[i[j]]]
            if len(smaller)!=0:l+=[smaller]
            if len(same)!=0:l+=same
            if len(larger)!=0:l+=[larger]
        temp=l
    l=[]
    for i in temp:l+=i
    if stats:
        if l==sorted(original):print("Successfully sorted list in", count, "steps.")
        else:print("Sorting unsuccessful.")
    return l
def sort4(l, stats=False): # Insertion sort (reinvented)
    if len(l)<2:
        print("List already sorted.")
        return l
    original, l, temp, count=list(l), [], list(l), 0
    for i in range(len(temp)):
        for j in range(len(l)+1):
            count+=1
            if j==len(l):l+=[temp[i]]
            elif temp[i]<=l[j]:
                l.insert(j, temp[i])
                break
        if count>10**6:break
    if stats:
        if l==sorted(original):print("Successfully sorted list in", count, "steps.")
        else:print("Sorting unsuccessful.")
    return l
def sort5(l, stats=False): # Bubble sort
    if len(l)<2:
        print("List already sorted.")
        return l
    original, l, count=list(l), list(l), 0
    for i in range(len(l)):
        swaps=0
        for j in range(len(l)-i-1):
            count+=1
            if l[j]>l[j+1]:
                l.insert(j+1, l.pop(j))
                swaps+=1
        if swaps==0 or count>10**6:break
    if stats:
        if l==sorted(original):print("Successfully sorted list in", count, "steps.")
        else:print("Sorting unsuccessful.")
    return l
def sort6(l, stats=False): # Selection sort
    if len(l)<2:
        print("List already sorted.")
        return l
    original, l, temp, count=list(l), [], list(l), 0
    while len(temp)>0 and count<10**6:
        count+=len(temp)-1
        l+=[min(temp)]
        temp.remove(min(temp))
    if stats:
        if l==sorted(original):print("Successfully sorted list in", count, "steps.")
        else:print("Sorting unsuccessful.")
    return l
sorts, length=[sort1, sort2, sort3, sort4, sort5, sort6], 100
randomList=[random.randint(0, length) for i in range(length)]
print(f"\n\nList of {length} random numbers:\n{randomList}\n\nSorted list:\n{sorted(randomList)}")
for i in range(len(sorts)):
    print(f"\nSorting method #{i+1}:")
    sorts[i](randomList, True)
randomOrder=unsort([i for i in range(length)])
print(f"\n\nList of numbers 0 - {length-1} in a random order:\n{randomOrder}")
for i in range(len(sorts)):
    print(f"\nSorting method #{i+1}:")
    sorts[i](randomOrder, True)
print()