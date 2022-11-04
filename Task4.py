from functools import reduce

# Аккумулятор количества одинаковых символов, но не более 9
# resList - список, элементы - списки, где элемент инд. 0 - символ, инд. 1 - кол.
# chEl - проверяемый элемент resList
def accSum (resList, chEl):
    if chEl[0] == resList[-1][0] and resList[-1][1] < 9: resList[-1][1] += 1
    else: resList.append(chEl)

    return resList

def strToRLE (sourceStr):
    resList = [[ch, 1] for ch in sourceStr]
    resList = reduce(accSum, resList[1:], resList[:1])

    return reduce(lambda resStr, el: resStr + str(el[1]) + el[0], resList, "")

def strFromRLE (cStr):
    resList = []
    for i in range(0, len(cStr), 2):
        resList += [[cStr[i + 1], int(cStr[i])]]

    return reduce(lambda resStr, el: resStr + el[0].rjust(el[1], el[0]), resList, "")

testData = [
    "eeekkkkkkkkkkkkkkkkkkkkkkkkkkkkow;;jiii",
    "оловянный, деревянный, стеклянный",
    "=======================================================++==============================================",
    "ё"
]

for testStr in testData:
    compStr = strToRLE(testStr)
    print(f"{testStr}\n{compStr}\n")

    assert strFromRLE(compStr) == testStr
