def read_boards(filename):
    boards = []
    current_board = []

    with open(filename, 'r') as f:
        for line in f:
            row = line.strip()
            if row:
                current_board.append(list(row))
            else:
                if current_board:
                    boards.append(current_board)
                    current_board = []
        if current_board:
            boards.append(current_board)
    return boards

def check_winner(board):
    # Check horizontal wins
    for row in board:
        if row[0] == row[1] == row[2] and row[0] in ('X', 'O', 'x', 'o'):
            return f"{row[0]} wins horizontally"
    # Check vertical wins
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] in ('X', 'O', 'x', 'o'):
            return f"{board[0][col]} wins vertically"
    # Check diagonal wins
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] in ('X', 'O', 'x', 'o'):
        return f"{board[0][0]} wins diagonally (top-left to bottom-right)"
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] in ('X', 'O', 'x', 'o'):
        return f"{board[0][2]} wins diagonally (top-right to bottom-left)"
    return "No winner"

def main():
    filename = "board.txt"
    boards = read_boards(filename)
    for i, board in enumerate(boards, 1):
        result = check_winner(board)
        print(f"Board {i}:")
        for row in board:
            print("".join(row))
        print(result)
        print()

if __name__ == "__main__":
    main()
