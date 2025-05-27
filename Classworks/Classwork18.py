# 1 Counting letters on each line:
def count_letters_per_line(filename):
    letter_counts = []
    with open(filename, 'r', ) as f:
        for line in f:
            count = sum(c.isalpha() for c in line)
            letter_counts.append(count)
    return letter_counts


def write_to_file(filename, letter_counts):
    with open(filename, 'w', ) as f:
        for i, count in enumerate(letter_counts, start=1):
            f.write(f"Line {i}: {count} letters\n")


filename = 'a.txt'
counts = count_letters_per_line(filename)
for i, count in enumerate(counts, start=1):
    print(f"Line {i}: {count} letters")

write_to_file('result.txt', counts)


# 2 TicTacToe (Determining the winner):

def read_board(filename):
    board = []
    with open(filename, 'r', ) as f:
        for line in f:
            row = line.strip()
            if row:
                board.append(list(row))
    return board

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] in ('X', 'O', 'x', 'o'):
            return f"{row[0]} wins horizontally"
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] in ('X', 'O', 'x', 'o'):
            return f"{board[0][col]} wins vertically"
    return "No winner"


filename = "board.txt"
board = read_board(filename)
result = check_winner(board)
print()
print(result)
