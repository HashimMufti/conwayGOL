import random as random
import copy
import os
import sys
import getopt


def game_of_life(some_board):
    r_index = -1
    duplicate_board = copy.deepcopy(some_board)
    for rows in some_board:
        r_index += 1
        c_index = -1
        for columns in rows:
            c_index += 1
            neighbors = get_neighbors(r_index, c_index)
            lives = get_lives(neighbors, some_board, len(
                some_board), len(some_board[0]))
            duplicate_board = rules(
                r_index, c_index, lives, some_board, duplicate_board)
    return duplicate_board


def rules(r_index, c_index, lives, some_board, duplicate_board):
    if some_board[r_index][c_index] == ALIVE:
        if lives < 2 or lives > 3:
            duplicate_board[r_index][c_index] = DEAD
    else:
        if lives == 3:
            duplicate_board[r_index][c_index] = ALIVE
    return duplicate_board


def get_lives(neighbors, some_board, rows, columns):
    alive = 0
    for neighbor in neighbors:
        if valid(neighbor, rows, columns):
            if some_board[neighbor[0]][neighbor[1]] == ALIVE:
                alive += 1
    return alive


def valid(neighbor, rows, columns):
    if neighbor[0] < 0 or neighbor[1] < 0:
        return False
    if neighbor[0] >= rows or neighbor[1] >= columns:
        return False
    return True


def get_neighbors(r_index, c_index):
    neighbors = []
    for x in range(-1, 2, 1):
        for y in range(-1, 2, 1):
            if x != 0 or y != 0:
                neighbors.append([r_index + x, c_index + y])
    return neighbors


def generate_board(r_size, c_size):
    board = []
    for x in range(0, r_size):
        row = []
        for y in range(0, c_size):
            row.append(DEAD)
        board.append(row)
    return board


def pretty_print(board):
    for row in board:
        for char in row:
            print(*char, end='')
        print("\n", end='')


def random_alive(board):
    r_index = -1
    for rows in board:
        c_index = -1
        for columns in rows:
            c_index += 1
            if random_number(1) > 0:
                board[r_index][c_index] = ALIVE
        r_index += 1
    return board


def random_number(n):
    return random.randint(0, 1)


def run_game(row, column, times):
    board = generate_board(row, column)
    board = random_alive(board)
    pretty_print(board)
    for time in range(0, times):
        print("Iteration: " + str(time))
        board = game_of_life(board)
        pretty_print(board)


def custom_game(board, times):
    pretty_print(board)
    for time in range(0, times):
        print("Iteration: " + str(time))
        board = game_of_life(board)
        pretty_print(board)


def clear():
    # Nasty!
    os.system('cls' if os.name == 'nt' else 'clear')


def stream_game(row, column):
    # Depending on game and size, can cause flashing, find other way to stream
    clear()
    board = generate_board(row, column)
    board = random_alive(board)
    pretty_print(board)
    while True:
        board = game_of_life(board)
        clear()
        pretty_print(board)


def main(argv):
    # This is janky, better ways to do this!
    try:
        opts, args = getopt.getopt(argv, "hi:r:c:", ["rows=", "columns="])
    except getopt.GetoptError as err:
        print(err)
        print('Error! Invalid option, please use:')
        print('main.py -h')
        sys.exit(2)
    if opts == []:
        print('Error! No options selected, please use:')
        print('main.py -h')
        sys.exit(2)
    row = None
    column = None
    for opt, arg in opts:
        if opt == '-h':
            print('Format:')
            print('main.py -r <int rows> -c <int columns>')
            sys.exit()
        elif opt in ("-r", "--rows"):
            row = arg
        elif opt in ("-c", "--columns"):
            column = arg
    try:
        stream_game(int(row), int(column))
    except Exception as e:
        print('Error! Invalid row/column, please use:')
        print('main.py -h')
        sys.exit()


# Change these to change board visual
ALIVE = u"\u2591"
DEAD = u"\u2588"

if __name__ == "__main__":
    main(sys.argv[1:])
