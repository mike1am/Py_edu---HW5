import random
import copy

def inputNatural (prompt, lim = 0):
    while True:
        try:
            num = int(input(prompt))
            if num <= 0: raise ValueError
        except ValueError:
            print("Вы должны ввести целое положительное число.")
        else: 
            if not bool(lim) or num <= lim:
                return num
            else:
                print("Вы ввели слишком большое число. Попробуйте ещё раз.")

def outputGameField (gameMatrix):
    outStr = "╔"
    for _ in range(len(gameMatrix[0]) - 1): outStr += "═══╤"
    outStr += "═══╗"
    print(outStr)

    for row in range(len(gameMatrix)):
        outStr = "║"
        for col in range(len(gameMatrix[0])): 
            if gameMatrix[row][col] == 0:
                outStr += str(row * len(gameMatrix[0]) + col + 1).center(3)
            elif gameMatrix[row][col] == 1:
                outStr += " + "
            else:
                outStr += " O "
            if col < len(gameMatrix[0]) - 1:
                outStr += "│"
            else:
                outStr += "║"
        print(outStr)

        if row < len(gameMatrix) - 1:
            outStr = "╟"
            for _ in range(len(gameMatrix[0]) - 1): outStr += "───┼"
            outStr += "───╢"
            print(outStr)
        else:
            outStr = "╚"
            for _ in range(len(gameMatrix[0]) - 1): outStr += "═══╧"
            outStr += "═══╝"
            print(outStr)

# Ход человека. sign = 0 - ставим +, 1 - O
# gameMatrix содержит 0 для свободных полей, 1 - ходы 1 игрока, 2 - ходы 2 игрока
def humanTurn (gameMatrix, sign):
    outputGameField(gameMatrix)
    
    signChar = ("+", "O")[sign]
    print(f"Введите номер поля, куда хотите поставить {signChar}")
    
    while True:
        elInd = inputNatural("==> ", len(gameMatrix) * len(gameMatrix[0]))
        
        i = (elInd - 1) // len(gameMatrix[0])
        j = elInd % len(gameMatrix) - 1

        if gameMatrix[i][j] == 0:
            gameMatrix[i][j] = sign + 1
            return
        else:
            print("Это поле занято. Попробуйте ещё раз.")

# Проверка списка чисел на одинаковые значения
def isSameNums (numList):
    for el in numList:
        if bool(el ^ numList[0]): return False
    return True
    
# Проверка на наличие выигрышной ситуации
def isWin(gameMatrix):
    for i in range(len(gameMatrix)): # проверка строк
        if gameMatrix[i][0] != 0 and isSameNums(gameMatrix[i]):
            return True
    
    for j in range(len(gameMatrix[0])): # проверка столбцов
        if gameMatrix[0][j] != 0 and isSameNums([gameMatrix[i][j] for i in range(len(gameMatrix))]):
            return True

    # проверка диагонали в.л. - н.пр.
    if gameMatrix[0][0] != 0 and \
        isSameNums([gameMatrix[i][j] for i, j in tuple(zip(range(len(gameMatrix)), range(len(gameMatrix[0]))))]):
        return True

    # проверка диагонали в.пр. - н.л.
    if gameMatrix[0][len(gameMatrix[0]) - 1] != 0 and \
        isSameNums([gameMatrix[i][j] for i, j in tuple(zip(range(len(gameMatrix)), range(len(gameMatrix[0]) - 1, -1, -1)))]):
        return True

    return False

# Проверка на отсутствие свободных (нулевых) полей
def isOver(matr):
    for row in matr:
        for el in row:
            if not bool(el): return False
    return True

# Рекурсивная функция поиска лучшего хода
# matr содержит 0 для свободных полей, 1 - предполагаемые и сделанные ходы алгоритма, 2 - ходы оппонента
# cTurn = True - моделирование хода алгоритма, False - хода оппонента
# maxRate - макс. оценка для поиска лучшего хода
# depth - текущая глубина рекурсии
def miniMax(matr, cTurn, maxRate, depth):
    # оценка хода в зависимости от текущей вложенности
    if isWin(matr):
        if cTurn: return [-maxRate + depth, 0, 0] # последний ход сделан оппонентом
        else: return [maxRate - depth, 0, 0] # последний ход сделан алгоритмом
    if isOver(matr): return [0, 0, 0]

    bestRate = -maxRate if cTurn else maxRate
    best_i, best_j = 0, 0
    
    for i in range(len(matr)): # проход по свободным полям
        for j in range(len(matr[0])):
            if not bool(matr[i][j]):
                matr[i][j] = int(not cTurn) + 1 # предполагаемый ход
                
                rate = miniMax(matr, not cTurn, maxRate, depth + 1)[0]

                # поиск лучшего хода в зависимости от cTurn
                if cTurn and rate > bestRate:
                    bestRate = rate
                    best_i = i
                    best_j = j
                elif cTurn and rate == bestRate: # для вариабельности поведения
                    if not bool(random.choice(range(maxRate))):
                        best_i = i
                        best_j = j
                elif not cTurn and rate < bestRate:
                    bestRate = rate
                    best_i = i
                    best_j = j
            
                matr[i][j] = 0 # освобождение поля

    return (bestRate, best_i, best_j)

# Ход компьютера (параметры - см. humanTurn)
def compTurn (gameMatrix, sign):
    if not bool(sign):
        testMatrix = copy.deepcopy(gameMatrix)
    else:
        testMatrix = list(map(lambda row: list(map(lambda el: (0, 2, 1)[el], row)), gameMatrix)) # ставит 1 для компьютера, 2 - для игрока

    maxRate = len(gameMatrix) * len(gameMatrix[0]) + 1 # макс. оценка хода в зависимости от числа полей
        
    nextTurn = miniMax(testMatrix, True, maxRate, 0)
    
    gameMatrix[nextTurn[1]][nextTurn[2]] = sign + 1


dim = inputNatural("Введите размер поля: ")

compGame = input("Желаете играть с компьютером? [Y/N] ").casefold() == "y"
if compGame: compFirst = not (input("Желаете ходить первым? [Y/N] ").casefold() == "y")

playerNames = ("компьютер", "игрок") if compGame and compFirst else ("игрок", "компьютер") if compGame else ("первый игрок", "второй игрок")
turn = 1
winFl = False

matr = [[0 for _ in range(dim)] for _ in range(dim)]

while not winFl and not isOver(matr):
    turn = (1, 0)[turn]

    if compGame and not bool(turn) == compFirst:
        compTurn(matr, turn)
    else:
        humanTurn(matr, turn)

    winFl = isWin(matr)
    
outputGameField(matr)
if winFl: print("\nВыиграл " + playerNames[turn])
else: print("\nНичья")
