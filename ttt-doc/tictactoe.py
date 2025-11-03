def show_board(board):
    for i in range(0, 9, 3):
        print(f"{board[i] or ' '} | {board[i+1] or ' '} | {board[i+2] or ' '}")
        if i < 6:
            print("--+---+--")
def check_result(board):
    def win(a, b, c):
        return board[a] == board[b] == board[c] 
    set = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # lignes
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colonnes
        (0, 4, 8), (2, 4, 6)              # diagonales
    ]
# Vérifier chaque combinaison, si une combinaison est gagnante on affiche "vous avez gagné" 
    for a, b, c in set:
        if win(a, b, c):
            
            print(f"Vous avez gagné la partie avec les '{board[a]}'")
            return
    if None not in board:
        print("Match nul")

# Initialisation du plateau
board = [None] * 9
board[0] = "X"
board[1] = "O"
board[4] = "O"
board[7] = "O"

# Affichage et vérification
show_board(board)
check_result(board)

