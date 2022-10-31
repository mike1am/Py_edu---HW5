import random

def inputNatural (prompt, maxLim = 0):
    while True:
        try:
            num = int(input(prompt))
            if num <= 0: raise ValueError
        except ValueError:
            print("Вы должны ввести целое положительное число.")
        else: 
            if not bool(maxLim) or num <= maxLim:
                return num
            else:
                print("Вы ввели слишком большое число. Попробуйте ещё раз.")

def humanTurn (cNum, pName, maxDecr):
    print(pName.capitalize() + ", сколько берёте конфет?")
    
    decr = inputNatural("==> ", min(maxDecr, cNum))

    return cNum - decr

def compTurn (cNum, maxDecr):
    decr = cNum % (maxDecr + 1)
    if decr == 0:
        decr = random.randint(1, min(cNum, maxDecr))
 
    print(f"Компьютер взял {decr} конфет")
    return cNum - decr

candyNum = inputNatural("Введите количество конфет: ")
maxDecr = inputNatural("Введите макс. количество конфет, которое можно взять за ход: ")
    
compGame = input("Желаете играть с компьютером? [Y/N] ").casefold() == "y"
if compGame: compFirst = not (input("Желаете ходить первым? [Y/N] ").casefold() == "y")

playerNames = ("компьютер", "игрок") if compGame and compFirst else ("игрок", "компьютер") if compGame else ("первый игрок", "второй игрок")
turn = 1

while candyNum > 0:
    turn = (1, 0)[turn]
    if compGame and not bool(turn) == compFirst:
        candyNum = compTurn(candyNum, maxDecr)
    else:
        candyNum = humanTurn(candyNum, playerNames[turn], maxDecr)
    print(f"Осталось конфет: {candyNum}")

print("\nВыиграл " + playerNames[turn])
