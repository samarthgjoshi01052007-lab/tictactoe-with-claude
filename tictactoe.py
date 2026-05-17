import random

def create_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def print_board(board):
    print("\n  1   2   3")
    for i, row in enumerate(board):
        print(f"{i+1} " + " | ".join(row))
        if i < 2:
            print("  ---+---+---")
    print()

def check_winner(board, player):
    # Check rows and columns
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_draw(board):
    return all(board[r][c] != " " for r in range(3) for c in range(3))

def get_empty_cells(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

def minimax(board, is_maximizing, ai, human):
    if check_winner(board, ai):
        return 1
    if check_winner(board, human):
        return -1
    if is_draw(board):
        return 0

    if is_maximizing:
        best = -10
        for r, c in get_empty_cells(board):
            board[r][c] = ai
            best = max(best, minimax(board, False, ai, human))
            board[r][c] = " "
        return best
    else:
        best = 10
        for r, c in get_empty_cells(board):
            board[r][c] = human
            best = min(best, minimax(board, True, ai, human))
            board[r][c] = " "
        return best

def ai_move(board, ai, human):
    best_score = -10
    best_move = None
    for r, c in get_empty_cells(board):
        board[r][c] = ai
        score = minimax(board, False, ai, human)
        board[r][c] = " "
        if score > best_score:
            best_score = score
            best_move = (r, c)
    return best_move

def get_player_move(board, player):
    while True:
        try:
            move = input(f"Player {player}, enter row and column (e.g. 1 2): ").strip()
            row, col = map(int, move.split())
            row -= 1
            col -= 1
            if 0 <= row < 3 and 0 <= col < 3:
                if board[row][col] == " ":
                    return row, col
                else:
                    print("That cell is already taken. Try again.")
            else:
                print("Row and column must be between 1 and 3.")
        except (ValueError, IndexError):
            print("Invalid input. Enter two numbers separated by a space (e.g. 1 2).")

def play_two_player():
    board = create_board()
    players = ["X", "O"]
    turn = 0

    print("\n=== Two Player Mode ===")
    print_board(board)

    while True:
        player = players[turn % 2]
        row, col = get_player_move(board, player)
        board[row][col] = player
        print_board(board)

        if check_winner(board, player):
            print(f"🎉 Player {player} wins!")
            return
        if is_draw(board):
            print("It's a draw!")
            return

        turn += 1

def play_vs_ai():
    board = create_board()
    human = "X"
    ai = "O"

    print("\n=== vs AI Mode (you are X, AI is O) ===")
    print_board(board)

    # Randomly decide who goes first
    turn = random.choice([human, ai])
    print(f"{turn} goes first!\n")

    while True:
        if turn == human:
            row, col = get_player_move(board, human)
            board[row][col] = human
            print_board(board)
            if check_winner(board, human):
                print("🎉 You win! Great job!")
                return
        else:
            print("AI is thinking...")
            row, col = ai_move(board, ai, human)
            board[row][col] = ai
            print(f"AI played at row {row+1}, col {col+1}")
            print_board(board)
            if check_winner(board, ai):
                print("🤖 AI wins! Better luck next time.")
                return

        if is_draw(board):
            print("It's a draw!")
            return

        turn = ai if turn == human else human

def main():
    print("╔══════════════════════╗")
    print("║    TIC-TAC-TOE 🎮    ║")
    print("╚══════════════════════╝")

    while True:
        print("\nSelect mode:")
        print("  1. Two Player")
        print("  2. vs AI")
        print("  3. Quit")

        choice = input("Enter choice (1/2/3): ").strip()

        if choice == "1":
            play_two_player()
        elif choice == "2":
            play_vs_ai()
        elif choice == "3":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")

        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing! 👋")
            break

if __name__ == "__main__":
    main()
