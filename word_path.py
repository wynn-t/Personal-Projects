wordList, words, neighbors=sorted(open("words_neighbors.txt").read().split("\n")), {}, {}
for i in range(len(wordList)):
    temp=wordList[i].split()
    wordList[i]=temp[0]
    if len(temp[0]) in words:words[len(temp[0])]+=[temp[0]]
    else:words[len(temp[0])]=[temp[0]]
    neighbors[temp[0]]=set(temp[1:])
def findDist(word1, word2, stats=False):
    if max(len(word1), len(word2))>max(words):quit()
    if len(word1)!=len(word2):
        #print("\nThe length of the words must be equal.")
        return float("nan")
    word1, word2=word1.lower(), word2.lower()
    if word1 not in wordList and word2 not in wordList:
        #print("\nNeither word is an actual word.")
        return float("nan")
    if word1 not in wordList:
        #print("\nThe first word is not an actual word.")
        return float("nan")
    if word2 not in wordList:
        #print("\nThe second word is not an actual word.")
        return float("nan")
    distance, wordsDistN, previous=0, {word1}, set()
    while word2 not in wordsDistN or testMode:
        distance+=1
        temp=set(wordsDistN)
        for i in temp:
            if i not in previous:
                if neighbors[i]==set():
                    for j in words[len(i)]:
                        count=0
                        for k in range(len(i)):
                            if i[k]!=j[k]:
                                count+=1
                                if count>=2:break
                        if count==1:neighbors[i]|={j}
                wordsDistN|=neighbors[i]
        if temp==wordsDistN:
            if stats:print(f"\n{len(wordsDistN)}/{len(words[len(word1)])}\n\nThere is no path between the 2 words.\n\nSearch depth: {distance}")
            return [distance-1, wordsDistN-previous] if testMode else float("inf")
        previous=temp
    if stats:print(f"\n{len(wordsDistN)}/{len(words[len(word1)])}")
    return [distance] if testMode else distance
def findPath(word1, word2):
    if max(len(word1), len(word2))>max(words) or testMode:quit()
    if len(word1)!=len(word2):
        print("\nThe length of the words must be equal.")
        return []
    word1, word2=word1.lower(), word2.lower()
    if word1 not in wordList and word2 not in wordList:
        print("\nNeither word is an actual word.")
        return []
    if word1 not in wordList:
        print("\nThe first word is not an actual word.")
        return []
    if word2 not in wordList:
        print("\nThe second word is not an actual word.")
        return []
    if findDist(word1, word2)==float("inf"):
        findDist(word1, word2, True)
        return [None]
    path, distance, previous=[word1], findDist(word1, word2), {word1}
    for i in range(distance):
        if i>=distance-1:break
        for j in neighbors[path[-1]]:
            if j not in previous and findDist(j, word2)<distance-i:
                previous|=neighbors[path[-1]]
                path+=[j]
                break
    return path+([] if distance==0 else [word2])
"""wordLength, testMode, temp, temp2=int(input("\nInput the word length: ")), True, 0, 0
print("\n"+str(len(words[wordLength])))
for i in words[wordLength]:
    test=findDist(i, words[wordLength][0])
    if len(test)==2 and test[0]>=temp:
        temp, temp2, test[1]=test[0], 1 if test[0]>temp else temp2+1, sorted(test[1])
        print(i, test)
print("\n"+str(temp2))"""
testMode=False
while True:
    word1, word2=input("\nInput the first word: "), input("Input the second word: ")
    print("\nPath:", findPath(word1, word2), "\nDistance:", findDist(word1, word2), "\n")
"""Longest distances of word length n:
1: "a", "b" (1, 26/26), (26)
2: "aa", "qu" (3, 427/427), (419)
3: "btu", "kpc" (7, 2128/2130), (30)
4: "expo", "xdiv" (15, 7081/7186), (4)
5: "epist", "orgia" (24, 14556/15920), (2)
6: "afghan", "elbowy" (66, 20043/29874), (3)
7: "cirrhus", "zealand" (70, 12897/41998), (3)
8: "airthing", "defuzing" (49, 1758/51627), (9)
9: "dodginess", "weariless" (33, 147/53402), (2)
10: "unsignable", "unwashable" (13, 44/45872), (7)
11: "buckishness", "goosishness" (12, 15/37539), (2)
12: "bilification", "modification" (7, 16/29124), (9)
13: "expansibility", "extensibility" (6, 7/20944), (2)
14: "inventibleness", "unbondableness" (5, 7/14149), (2)
15: "processionalist", "professionalize" (3, 5/8846), (2)
16: "incontrovertible", "uncontrovertably" (3, 6/5182), (4)
17: "transcendentalist", "transcendentalize" (3, 4/2967), (2)
18: "chlorophylliferous", "chlorophylligenous" (2, 3/1471), (2)
19: "anticonventionalism", "anticonventionalist" (1, 2/760), (46)
20: "incontrovertibleness", "uncontrovertableness" (2, 3/359), (2)
21: "anticonstitutionalism", "anticonstitutionalist" (1, 2/168), (8)
22: "electroencephalographs", "electroencephalography" (1, 2/74), (2)
23: "pseudolamellibranchiata", "pseudolamellibranchiate" (1, 2/31), (2)
24: No neighboring words (0, 1/12), (12)
25: No neighboring words (0, 1/8), (8)
26: No words (nan, 0/0), (0)
27: No neighboring words (0, 1/3), (3)
28: No neighboring words (0, 1/2), (2)
29: No neighboring words (0, 1/2), (2)
30: No words (nan, 0/0), (0)
31: Insufficient (1) words (0, 1/1), (1)

Shortest furthest word distances in largest island of word length n:
1: "a", "b" (1, 26/26), (26)
2: "ar", "ba" (2, 427/427), (8)
3: "tos", "acc" (4, 2128/2130), (1)
4: "alle", "edhs" (8, 7081/7186), (1)
5: "bries", "aggro" (13, 14556/15920), (1)
6: "causus", "afghan" (33, 20043/29874), (1)
7: "candies", "cirrhus" (35, 12897/41998), (1)
8: "bangling", "airthing" (25, 1758/51627), (4)
9: "woodiness", "dodginess" (17, 147/53402), (3)
10: "unvendable", "unwashable" (7, 44/45872), (3)
11: "bearishness", "buckishness" (6, 15/37539), (1)
12: "sanification", "bilification" (4, 16/29124), (3)
13: "formalization", "formulisation" (2, 7/20944), (2)
14: "philanthropise", "psilanthropism" (2, 7/14149), (3)
15: "professionalise", "processionalist" (2, 5/8846), (3)
16: "uncontrovertible", "incontrovertibly" (2, 6/5182), (2)
17: "consubstantialism", "nonsubstantialist" (2, 4/2967), (10)
18: "chlorophylligerous", "chlorophylliferous" (1, 3/1471), (1)
19: "anticonventionalism", "anticonventionalist" (1, 2/760), (46)
20: "uncontrovertibleness", "incontrovertibleness" (1, 3/359), (1)
21: "anticonstitutionalism", "anticonstitutionalist" (1, 2/168), (8)
22: "electroencephalographs", "electroencephalography" (1, 2/74), (2)
23: "pseudolamellibranchiata", "pseudolamellibranchiate" (1, 2/31), (2)
24: No neighboring words (0, 1/12), (12)
25: No neighboring words (0, 1/8), (8)
26: No words (nan, 0/0), (0)
27: No neighboring words (0, 1/3), (3)
28: No neighboring words (0, 1/2), (2)
29: No neighboring words (0, 1/2), (2)
30: No words (nan, 0/0), (0)
31: 1 word: "dichlorodiphenyltrichloroethane" (0, 1/1), (1)

Words with most neighbors for length n:
1: "a" (25), (26)
2: "as" (47), (1)
3: "tat" (51), (1)
4: "care" (43), (1)
5: "cares" (37), (1)
6: "batter" (27), (1)
7: "barling" (23), (1)
8: "unmailed" (14), (1)
9: "battering" (12), (1)
10: "slattering" (9), (1)
11: "unshakeable" (6), (1)
12: "materialized" (5), (2)
13: "revolutionist" (4), (1)
14: "philanthropise" (4), (1)
15: "conventionalise" (3), (9)
16: "anthropomorphise" (4), (1)
17: "consubstantialism" (2), (16)
18: "chlorophylligerous" (2), (1)
19: "anticonventionalism" (1), (46)
20: "uncontrovertibleness" (2), (1)
21: "anticonstitutionalism" (1), (8)
22: "electroencephalographs" (1), (2)
23: "pseudolamellibranchiata" (1), (2)
24: No neighboring words (0), (12)
25: No neighboring words (0), (8)
26: No words (nan), (0)
27: No neighboring words (0), (3)
28: No neighboring words (0), (2)
29: No neighboring words (0), (2)
30: No words (nan), (0)
31: 1 word: "dichlorodiphenyltrichloroethane" (0), (1)"""