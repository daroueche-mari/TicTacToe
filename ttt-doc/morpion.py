import pygame
import random
import sys

# Initialisation de Pygame et des paramètres du jeu
pygame.init()
size = 600 # Taille de la fenêtre
grid = 3   # Taille de la grille (3x3)
box = size // grid   # Taille d'une case
player_wins = 0
ai_wins = 0
draws = 0

# Définition des couleurs utilisées
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 200, 0)
dark_green = (0, 150, 0)
grey = (200, 200, 200)
brown = (139, 69, 19)
blue = (0, 0, 255)
# Création de la fenêtre de jeu avec une zone supplémentaire pour les messages
screen = pygame.display.set_mode((size, size + 100))
# Dessine la grille de jeu et les symboles X et O
def draw_tray(board):
    screen.fill(green)
     # Dessin des lignes de la grille
    for i in range(1, grid):
        pygame.draw.line(screen, white, (0, i * box), (size, i * box), 5)
        pygame.draw.line(screen, white, (i * box, 0), (i * box, size), 5)
        # Dessin des symboles sur la grille
    for y in range(grid):
        for x in range(grid):
            if board[y][x] == "X":
                # Dessine un "X"
                pygame.draw.line(screen, white, (x * box + 50, y * box + 50), ((x + 1) * box - 50, (y + 1) * box - 50), 6)
                pygame.draw.line(screen, white, ((x + 1) * box - 50, y * box + 50), (x * box + 50, (y + 1) * box - 50), 6)
            elif board[y][x] == "O":
                # Dessine un "O"
                pygame.draw.circle(screen, blue, (x * box + box // 2, y * box + box // 2), box // 2 - 50, 6)
                
# Vérifie si une case est vide
def box_good(board, x, y):
    return board[y][x] == ""

# Joue le tour du joueur humain
def play_turn_player(board, pos):
    
    # Convertit la position en coordonnées de grille
    x, y = pos[0] // box, pos[1] // box
    # Si la case est vide
    if box_good(board, x, y): 
    # Place un "X"
        board[y][x] = "X"
        return True
    return False

# Vérifie si un joueur a gagné
def verify_win(board, symbole):
    # Vérifie les lignes et colonnes
    for i in range(grid):
        if all(board[i][j] == symbole for j in range(grid)) or all(board[j][i] == symbole for j in range(grid)):
            return True
        # Vérifie les diagonales
    if all(board[i][i] == symbole for i in range(grid)) or all(board[i][grid - 1 - i] == symbole for i in range(grid)):
        return True
    return False


# Vérifie si toutes les cases sont remplies (égalité)
def equality(board):
    return all(board[y][x] != "" for y in range(grid) for x in range(grid))

# Minimax pour l'IA, depth : profondeur
def minimax(board, depth, is_max, alpha, beta):
    if verify_win(board, "O"):
        return 10 - depth
    elif verify_win(board, "X"):
        return depth - 10
    elif equality(board):
        return 0

    if is_max:
        max_eval = -float("inf")
        for y in range(grid):
            for x in range(grid):
                if board[y][x] == "":
                    board[y][x] = "O"
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[y][x] = ""
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float("inf")
        for y in range(grid):
            for x in range(grid):
                if board[y][x] == "":
                    board[y][x] = "X"
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[y][x] = ""
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval
    
# Joue le tour de l'IA en choisissant le meilleur coup
def play_turn_ai(board):
    best_score = -float("inf")
    best_choice = None
    for y in range(grid):
        for x in range(grid):
            if board[y][x] == "":
                board[y][x] = "O"
                score = minimax(board, 0, False, -float("inf"), float("inf"))
                board[y][x] = ""
                if score > best_score:
                    best_score = score
                    best_choice = (x, y)
    if best_choice:
        x, y = best_choice
        board[y][x] = "O"
        
# indicateur de tour
def draw_turn_indicator(turn_player):
    font_title = pygame.font.Font("looneytunes.ttf", 30)
    font = pygame.font.SysFont(None, 40)
    message = "Tour du joueur" if turn_player else "Tour de l'IA"
    text = font_title.render(message, True, white)
    screen.blit(text, (10, size + 60))
    score_text = font.render(f"V: {player_wins}  D: {ai_wins} N: {draws}", True, white)
    screen.blit(score_text, (size - 200, size + 30))

    
# creation et modification du menu acceuil
def menu_home():
    font = pygame.font.SysFont(None, 50)
    small_font_menu = pygame.font.Font("tangon.ttf", 40)
    font_title = pygame.font.Font("looneytunes.ttf", 60)
    play_rect = pygame.Rect(size // 2 - 75, size // 2 - -80, 150, 50)
    background_menu = pygame.image.load("O.png")
    background_menu = pygame.transform.scale(background_menu, (size, size + 100))    
    while True:
        screen.blit(background_menu, (0, 0))
        title = font_title.render("TIC TAC TOE", True, white)
        screen.blit(title, title.get_rect(center=(size // 2, size // 2 - 40)))

        text = small_font_menu.render("Jouer", True, white)
        pygame.draw.rect(screen, green, play_rect)
        screen.blit(text, text.get_rect(center=play_rect.center))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return
                
# creation et modification du menu de fin 
def menu_end(message):
    font = pygame.font.SysFont(None, 40)
    small_font_menu = pygame.font.Font("tangon.ttf", 40)
    replay_rect = pygame.Rect(size // 2 - 160, size // 2 + 60, 150, 50)
    menu_rect = pygame.Rect(size // 2 + 10, size // 2 + 60, 150, 50)
    while True:
        screen.fill(dark_green)
        text = font.render(message, True, white)
        screen.blit(text, text.get_rect(center=(size // 2, size // 2 - 40)))
        pygame.draw.rect(screen, green, replay_rect)
        button = small_font_menu.render("Rejouer", True, white)
        screen.blit(button, button.get_rect(center=replay_rect.center))

        pygame.draw.rect(screen, red, menu_rect)
        button_menu = small_font_menu.render("Menu", True, white)
        screen.blit(button_menu, button_menu.get_rect(center=menu_rect.center))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_rect.collidepoint(event.pos):
                    return "replay"
                elif menu_rect.collidepoint(event.pos):
                    return "menu"

# Boucle principale
while True:
    menu_home()
    player_wins = 0
    ai_wins = 0
    draws = 0
    continuer = True
    while continuer:
        board = [["" for _ in range(grid)] for _ in range(grid)]
        turn_player = True
        game_end = False
        clock = pygame.time.Clock()

        while not game_end:
            draw_tray(board)
            draw_turn_indicator(turn_player)
            pygame.display.update()

            if turn_player:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if play_turn_player(board, pygame.mouse.get_pos()):
                            if verify_win(board, "X"):
                                player_wins += 1
                                choice = menu_end("Victoire du joueur !")
                                game_end = True
                            elif equality(board):
                                draws += 1
                                choice = menu_end("Match nul !")
                                game_end = True
                            else:
                                turn_player = False
            else:
                pygame.time.delay(500)
                play_turn_ai(board)
                draw_tray(board)
                draw_turn_indicator(turn_player)
                pygame.display.update()
                pygame.time.delay(300)
                if verify_win(board, "O"):
                    ai_wins += 1
                    choice = menu_end("Victoire de l'IA !")
                    game_end = True
                elif equality(board):
                    draws += 1
                    choice = menu_end("Match nul !")
                    game_end = True
                else:
                    turn_player = True

            clock.tick(30)

        if choice == "menu":
            continuer = False