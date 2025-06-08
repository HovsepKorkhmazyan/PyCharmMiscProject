import random


def print_board(board):
    for row in range(3):
        print(" | ".join(board[row]))
        if row < 2:
            print("-" * 9)


def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None


def is_board_full(board):
    for row in board:
        if " " in row:
            return False
    return True


def player_move(board):
    while True:
        try:
            row = int(input("Enter the row (0-2): "))
            col = int(input("Enter the column (0-2): "))
            if row not in range(3) or col not in range(3):
                print("Row and column must be between 0 and 2. Try again.")
                continue
            if board[row][col] != " ":
                print("That cell is already taken. Try again.")
                continue
            board[row][col] = "X"
            break
        except ValueError:
            print("Please enter valid integers for row and column.")


def computer_move(board):
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = "O"
        print(f"Computer placed an O at row {row}, column {col}.")


def tic_tac_toe_vs_pc():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic-Tac-Toe!\nYou are X and the computer is O.")
    while True:
        print_board(board)
        player_move(board)
        winner = check_winner(board)
        if winner:
            print_board(board)
            print("Congratulations, you win!")
            break
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        computer_move(board)
        winner = check_winner(board)
        if winner:
            print_board(board)
            print("Computer wins! Better luck next time.")
            break
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break


if __name__ == "__main__":
    tic_tac_toe_vs_pc()
