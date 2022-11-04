import random
import copy
from functools import reduce

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
    for row in range(len(gameMatrix)):
        if row > 0:
            print("".join("-" for _ in range(len(gameMatrix) * 4 - 1)))
        
        for col in range(len(gameMatrix[0])): 
            if col == 0: outStr = ""
            else: outStr += "|"
                    
            if gameMatrix[row][col] == 0:
                outStr += str(row * len(gameMatrix[0]) + col + 1).center(3)
            elif gameMatrix[row][col] == 1:
                outStr += "\033[1m\033[95m + \033[0m"
            else: 
                outStr += "\033[1m\033[95m 0 \033[0m"
        print(outStr)

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
    return reduce(lambda acc, rowRes: acc and rowRes, [reduce(lambda acc, el: acc and bool(el), row, True) for row in matr], True)

# Ход человека. sign = 0 - ставим +, 1 - O
# gameMatrix содержит 0 для свободных полей, 1 - ходы 1 игрока, 2 - ходы 2 игрока
def humanTurn (gameMatrix, sign):
    outputGameField(gameMatrix)
    
    signChar = ("+", "0")[sign]
    print(f"Введите номер поля, куда хотите поставить {signChar}")
    print(f"{len(gameMatrix) * len(gameMatrix[0]) + 1} - ход за Вас сделает компьютер")
    
    while True:
        elInd = inputNatural("==> ", len(gameMatrix) * len(gameMatrix[0]) + 1)
        
        if elInd == len(gameMatrix) * len(gameMatrix[0]) + 1:
            compTurn(gameMatrix, sign)
            return
        
        i = (elInd - 1) // len(gameMatrix[0])
        j = elInd % len(gameMatrix) - 1

        if gameMatrix[i][j] == 0:
            gameMatrix[i][j] = sign + 1
            return
        else:
            print("Это поле занято. Попробуйте ещё раз.")

# Рекурсивная функция поиска лучшего хода
# matr содержит 0 для свободных полей, 1 - предполагаемые и сделанные ходы алгоритма, 2 - ходы оппонента
# avTurns - список кортежей со свободными полями (для оптимизации)
# cTurn = True - моделирование хода алгоритма, False - хода оппонента
# maxRate - макс. оценка для поиска лучшего хода
# depth - текущая глубина рекурсии
# alpha, beta - критерии для отсечения заведомо лишних ветвей, при первом (нерекурс.) вызове не требуются
def miniMax(matr, avTurns, cTurn, maxRate, depth, alpha = 0, beta = 0):
    # global miniMaxCallCnt
    # global alphaBetaPrunCnt
    # miniMaxCallCnt += 1

    bestRate = -maxRate if cTurn else maxRate
    best_i = 0
    best_j = 0
    if depth == 0:
        alpha = -maxRate
        beta = maxRate

    for avInd in range(len(avTurns)): # проход по свободным полям
        i, j = avTurns[avInd]
        avTurns.pop(avInd)
        
        matr[i][j] = int(not cTurn) + 1
        
        if isWin(matr):
            if cTurn: rate = maxRate - depth # расчёт оценки с учётом вложенности, т.е. "отдалённости" результата
            else: rate = -maxRate + depth
        elif len(avTurns) == 0:
            rate = 0
        else:
            rate = miniMax(matr, avTurns, not cTurn, maxRate, depth + 1, alpha, beta)[0]

        if cTurn and rate > bestRate or not cTurn and rate < bestRate:
            bestRate = rate
            best_i, best_j = i, j
        elif depth == 0 and cTurn and rate == bestRate and not bool(random.choice(range(len(avTurns)))): # для вариабельности поведения
            best_i, best_j = i, j
        
        matr[i][j] = 0 # освобождение поля
        avTurns.insert(avInd, (i, j))

        # При обновлении alpha на уровне depth == 0 не гарантируется достоверность возвращаемых оценок rate, если rate == bestRate,
        # при отсечении по условию alpha >= beta, что, при выполнении условия вариабельности (см. выше), может приводить к выбору неправильного хода.
        # Другое решение - заменить условием alpha > beta - приводит к увелич. в более, чем 3 раза кол. итераций miniMax
        if cTurn and alpha < bestRate and depth > 0: alpha = bestRate
        elif not cTurn and beta > bestRate: beta = bestRate
        if alpha >= beta:
            # alphaBetaPrunCnt += 1
            break # отсечение ходов, не влияющих на оценку

    return (bestRate, best_i, best_j)

# Ход компьютера (параметры - см. humanTurn)
def compTurn (gameMatrix, sign):
    # global miniMaxCallCnt
    # global alphaBetaPrunCnt
    # miniMaxCallCnt = 0
    # alphaBetaPrunCnt = 0

    if not bool(sign):
        testMatrix = copy.deepcopy(gameMatrix)
    else:
        testMatrix = list(map(lambda row: list(map(lambda el: (0, 2, 1)[el], row)), gameMatrix)) # ставит 1 для компьютера, 2 - для игрока

    maxRate = len(gameMatrix) * len(gameMatrix[0]) # макс. оценка хода в зависимости от числа полей
    
    # формирование списка возможных ходов - для ускорения
    availTurns = [(i, j) for i in range(len(testMatrix)) for j in range(len(testMatrix[0])) if testMatrix[i][j] == 0]

    nextTurn = miniMax(testMatrix, availTurns, True, maxRate, 0)

    # print(f"Common     --> {miniMaxCallCnt}")
    # print(f"Alpha-Beta --> {alphaBetaPrunCnt}")
    
    gameMatrix[nextTurn[1]][nextTurn[2]] = sign + 1
    return


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
