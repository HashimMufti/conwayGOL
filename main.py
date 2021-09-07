import random as rand
import copy
import os
import sys
import getopt


def game_of_life(some_board):
    """Play a single iteration of Conway's Game of Life on a board.

    Args:
        some_board (List of lists of strings): List of lists containing the ALIVE/DEAD variable.

    Returns:
        [List of lists of strings]: List of lists containing the updated ALIVE/DEAD variables.
    """
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
    """Apply Conway's Rules to a board

    Args:
        r_index (int): Current row index
        c_index (int): Current column index
        lives (int): Number of ALIVE cells around current position
        some_board (List of lists of strings): Board used to determine rule
        duplicate_board (List of lists of strings): Board used to apply rule

    Returns:
        [List of lists of strings]: Board used to apply rule (modified board)
    """
    if some_board[r_index][c_index] == ALIVE:
        if lives < 2 or lives > 3:
            duplicate_board[r_index][c_index] = DEAD
    else:
        if lives == 3:
            duplicate_board[r_index][c_index] = ALIVE
    return duplicate_board


def get_lives(neighbors, some_board, rows, columns):
    """Get all the ALIVE cells around current position

    Args:
        neighbors (List of integers): List of row and column of neighbor
        some_board (List of lists of strings): Board used to find neighbors
        rows (int): Current row
        columns (int)): Current column

    Returns:
        [int]: Number of alive cells around current position
    """
    alive = 0
    for neighbor in neighbors:
        if valid(neighbor, rows, columns) and some_board[neighbor[0]][neighbor[1]] == ALIVE:
            alive += 1
    return alive


def valid(neighbor, rows, columns):
    """Find out if neighbor cell is valid

    Args:
        neighbor (List of integers): Neighboring cell position
        rows (int): Number of rows on the board
        columns (int): Number of columns on the board

    Returns:
        [boolean]: True if valid, False otherwise
    """
    if neighbor[0] < 0 or neighbor[1] < 0:
        return False
    if neighbor[0] >= rows or neighbor[1] >= columns:
        return False
    return True


def get_neighbors(r_index, c_index):
    """Get neighboring cell positions

    Args:
        r_index (int): Current row index
        c_index ([type]): Current column index

    Returns:
        [List of list of integers]: List of neighbors with each neighbor containing a list of their row and column index.
    """
    neighbors = []
    for x in range(-1, 2, 1):
        for y in range(-1, 2, 1):
            if x != 0 or y != 0:
                neighbors.append([r_index + x, c_index + y])
    return neighbors


def generate_board(r_size, c_size):
    """Generate board of row size, column size

    Args:
        r_size (int): Number of rows to generate
        c_size (int): Number of columns to generate

    Returns:
        [List of lists of string]: Board that can be used to play Conway's GOL
    """
    board = []
    for x in range(0, r_size):
        row = []
        for y in range(0, c_size):
            row.append(DEAD)
        board.append(row)
    return board


def pretty_print(board):
    """Pretty print a board

    Args:
        board (List of lists of string): Board to be printed!
    """
    for row in board:
        for char in row:
            print(*char, end='')
        print("\n", end='')


def random_alive(board):
    """Randomly make a subset of the board ALIVE!

    Args:
        board (List of lists of string): Board to modify

    Returns:
        [List of lists of string]: Modified board
    """
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
    """Generate a random number from 0 to n

    Args:
        n (int): Limit of number to be generated (inclusive)

    Returns:
        [int]: Random generated number
    """
    return rand.randint(0, n)


def run_game(row, column, times):
    """Run the game a certain number of times for a board of size row, column,

    Args:
        row (int): Number of rows on the board
        column (int): Number of columns on the board
        times (int): Number of times to be run
    """
    board = generate_board(row, column)
    board = random_alive(board)
    pretty_print(board)
    for time in range(0, times):
        print("Iteration: " + str(time))
        board = game_of_life(board)
        pretty_print(board)


def custom_game(board, times):
    """Run the game on your custom board

    Args:
        board (List of lists of lists of lists of strings): Board to run the game on
        times (int): How many times to run the game
    """
    pretty_print(board)
    for time in range(0, times):
        print("Iteration: " + str(time))
        board = game_of_life(board)
        pretty_print(board)


def clear():
    """Clear the terminal
    """
    os.system('cls' if os.name ==
              'nt' else 'clear')  # Nasty way to do this, find alternative


def stream_game(row, column):
    """Play the game an infinite number of times for a row, column

    Args:
        row (int): Number of rows on the board
        column (int): Number of columns on the board
    """
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
    """Parse command line arguments and run the game accordingly

    Args:
        argv (Command line arguments): Passed command line arguments
    """
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
    except Exception:  # TODO: Handle specific exception
        print('Error! Invalid row/column, please use:')
        print('main.py -h')
        sys.exit()


# Change these to change board visual
ALIVE = u"\u2591"
DEAD = u"\u2588"

if __name__ == "__main__":
    main(sys.argv[1:])
