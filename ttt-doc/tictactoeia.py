def show_board(board):
    for i in range(0, 9, 3):
        print(f"{board[i] or ' '} | {board[i+1] or ' '} | {board[i+2] or ' '}")
        if i < 6:
            print("--+---+--")
def check_result(board):
    def win(a, b, c):
        return board[a] == board[b] == board[c] 
   
    set = [
         (0, 1, 2), (3, 4, 5), (6, 7, 8), # ligne winnere
        (0, 3, 6), (1, 4, 7), (2, 5, 8), # colonne winnere                 
        (0, 4, 8), (2, 4, 6)   # daigonale winnere
    ]
    for a, b, c in set:
        if win(a, b, c):
            return board[a]  # Retourne le winner
    if None not in board:
        return "Égalité"
    
    return None  # Pas encore de winner

def ai(board, signe):
    for i in range(9):
        # Cette fonction cherche la première case vide sur le plateau (board) et la retourne.
        if board[i] is None:
            return i
        # Si toutes les cases sont prises, elle retourne False.
    return False

# --- Boucle de jeu ---
board = [None] * 9
player = "X"
player_ai = "O"

while True:
    show_board(board)
    # Tour du player
    try:
        # - Le player entre un chiffre entre 0 et 8.
        choice = int(input("Choisis une case (0-8) : "))
        # - Si la case est déjà prise, on affiche "Case déjà prise".
        if board[choice] is not None:
            print("Case déjà prise.")
            continue
        # - Si tout va bien, on place "X" sur la case choisie. (player = "X")
        board[choice] = player
        # - Si l’entrée n’est pas un nombre (int), on affiche "Entrée invalide".
    except:
        print("Entrée invalide.")
        continue
    winner = check_result(board)
    if winner:
        show_board(board)
        print("Résultat :", winner)
        break
    # Tour de l'ai
    # - L’ai choisit une case vide (la première disponible).
    attempt = ai(board, player_ai)
    if attempt is not False:
        board[attempt] = player_ai
    winner = check_result(board)
    if winner:
        show_board(board)
        print("Résultat :", winner)
        break