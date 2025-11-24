import random
import os
from datetime import datetime

os.makedirs("game_stats", exist_ok=True)

def check_win(board, player, size):
    for i in range(size):
        if all(cell == player for cell in board[i]): return True
        if all(board[j][i] == player for j in range(size)): return True
    if all(board[i][i] == player for i in range(size)): return True
    if all(board[i][size-1-i] == player for i in range(size)): return True
    return False

while True:
    size = 3
    try:
        size_input = input("Размер поля: ") or "3"
        size = int(size_input)
        if size < 3: size = 3
    except:
        size = 3
    
    board = [[' ']*size for _ in range(size)]
    player = random.choice(['X', 'O'])
    stats_file = f"game_stats/game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        f.write(f"Размер: {size}x{size}\nПервый: {player}\n")
    
    print(f"\nИгра {size}x{size}")
    print(f"Начинает: {player}")
    
    mode = input("1-друг 2-робот (1): ") or "1"
    
    while True:
        print(f"\nХод: {player}")
        print(f"  {'   '.join(str(i) for i in range(size))}")
        for i in range(size):
            print(f"{i}  {' │ '.join(board[i])}")
            if i < size-1: print("   " + "───"*size)
        
        if mode == "2" and player == "O":
            empty = [(i,j) for i in range(size) for j in range(size) if board[i][j]==' ']
            row, col = random.choice(empty) if empty else (0,0)
            print(f"Робот: {row} {col}")
        else:
            try:
                row = int(input(f"Строка (0-{size-1}): "))
                col = int(input(f"Столбец (0-{size-1}): "))
            except:
                print("Ошибка!")
                continue
        
        if row < 0 or row >= size or col < 0 or col >= size or board[row][col] != ' ':
            print("Неверный ход!")
            continue
        
        board[row][col] = player
        
        with open(stats_file, 'a', encoding='utf-8') as f:
            f.write(f"{player} -> ({row},{col})\n")
        
        if check_win(board, player, size):
            print(f"\nПобедил {player}!")
            with open(stats_file, 'a', encoding='utf-8') as f:
                f.write(f"Победил: {player}\n")
            break
        
        if all(cell != ' ' for row in board for cell in row):
            print("\nНичья!")
            with open(stats_file, 'a', encoding='utf-8') as f:
                f.write("Ничья\n")
            break
        
        player = 'O' if player == 'X' else 'X'
    
    if input("\nЕще? (да/нет): ").lower() not in ['да', 'д']:
        print("Пока!")
        break