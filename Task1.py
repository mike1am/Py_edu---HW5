def delRedundWords (sourceStr, markStr):
    wordList = sourceStr.split()

    resList = filter(lambda word: markStr not in word, wordList)
    
    return " ".join(resList)

testData = [
    ["Быть абра или не быть - вот кадабра в чём вопрос", "абр", "Быть или не быть - вот в чём вопрос"],
    ["Отговорила ёксель роща моксель золотая", "сель", "Отговорила роща золотая"]
]

for initStr, toDel, resStr in testData:
    print(delRedundWords(initStr, toDel))
    assert delRedundWords(initStr, toDel) == resStr
