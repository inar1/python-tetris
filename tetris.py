#!/usr/bin/python3

import os
import random
import sys
import time
import keyboard

# for testing purpose
# import pdb

CANVAS_HORIZONTAL = 10
CANVAS_VERTICAL = 20
TOP_EDGE_SIZE = 5
EDGE_SIZE = 1

KEY_MOVE_RIGHT = 'd'
KEY_MOVE_LEFT = 'a'
KEY_MOVE_DOWN = 's'
KEY_ROTATE = 'w'
KEY_PAUSE = 'p'

LOOP_TIME = 0.5
CONTROL_DURATION = 0.1
DRAWING_DURATION = 0.2
PAUSE_DURATION = 1

CANVAS_EDGE = 3
MERGED_BLOCK = 2
DROPPING_BLOCK = 1
BLANK = 0

TETROMINOS = [
        [[1],
         [1],
         [1],
         [1]],

        [[1, 0],
         [1, 0],
         [1, 1]],

        [[0, 1],
         [0, 1],
         [1, 1]],

        [[1, 1],
         [1, 1]],

        [[0, 1, 1],
         [1, 1, 0]],

        [[1, 1, 0],
         [0, 1, 1]],

        [[0, 1, 0],
         [1, 1, 1]]
]


def main():

    # initialization
    board = init_gameboard()
    tetromino = Tetromino(board)
    current_time = time.time()
    last_moving_time = current_time
    last_slide_time = current_time
    last_rotate_time = current_time
    last_drawing_time = current_time
    last_paused_time = current_time
    is_paused = False
    clear_console()

    while not is_gameover(board):
        current_time = time.time()

        # pause if pause button is pressed
        if keyboard.is_pressed(KEY_PAUSE):
            if current_time - last_paused_time > PAUSE_DURATION:
                if is_paused:
                    is_paused = False
                    last_paused_time = time.time()
                else:
                    is_paused = True
                    last_paused_time = time.time()
        if is_paused:
            last_moving_time = time.time()
            continue

        # controll position of tetromino
        if current_time - last_slide_time > CONTROL_DURATION:
            if keyboard.is_pressed(KEY_MOVE_RIGHT):
                tetromino.move_right()
                last_slide_time = time.time()
            elif keyboard.is_pressed(KEY_MOVE_LEFT):
                tetromino.move_left()
                last_slide_time = time.time()
            elif keyboard.is_pressed(KEY_MOVE_DOWN):
                tetromino.move_down()
                last_slide_time = time.time()

        if current_time - last_rotate_time > CONTROL_DURATION:
            if keyboard.is_pressed(KEY_ROTATE):
                tetromino.rotate()
                last_rotate_time = time.time()

        if current_time - last_moving_time > LOOP_TIME:
            if tetromino.can_move_down():
                tetromino.move_down()
                last_moving_time = time.time()
            else:
                merge_tetromino(board, tetromino)
                tetromino = Tetromino(board)

        board = remove_completed_row(board)
        board = append_tetromino(refresh_board(board), tetromino)
        if current_time - last_drawing_time > DRAWING_DURATION:
            draw_board(board)
            last_drawing_time = time.time()
        # pdb.set_trace()  # for testing purpose


def init_gameboard():
    board = []
    for v in range(CANVAS_VERTICAL + TOP_EDGE_SIZE):
        board.append(create_board_row())
    board.append([CANVAS_EDGE for x in range(CANVAS_HORIZONTAL + (EDGE_SIZE * 2))])
    return board


def remove_completed_row(board):
    for row_index in range(len(board) - EDGE_SIZE):
        if BLANK not in board[row_index] and DROPPING_BLOCK not in board[row_index]:
            board.pop(row_index)
            board.insert(BLANK, create_board_row())
    return board


def create_board_row():
    line = []
    for h in range(CANVAS_HORIZONTAL + (EDGE_SIZE * 2)):
        index = h + 1
        if index <= EDGE_SIZE:
            line.append(CANVAS_EDGE)
        elif h >= EDGE_SIZE + CANVAS_HORIZONTAL:
            line.append(CANVAS_EDGE)
        else:
            line.append(BLANK)
    return line


def refresh_board(board):
    for v in range(len(board)):
        for h in range(len(board[0])):
            if board[v][h] < 2:
                board[v][h] = BLANK
    return board


def merge_tetromino(board, tetromino):
    form = tetromino.form
    pos_x = tetromino.pos_x
    pos_y = tetromino.pos_y
    size_x = tetromino.size_x
    size_y = tetromino.size_y
    for x in range(size_x):
        for y in range(size_y):
            if form[y][x] == 1:
                board[pos_y + y][pos_x + x] = 2
    return board


def append_tetromino(board, tetromino):
    form = tetromino.form
    pos_x = tetromino.pos_x
    pos_y = tetromino.pos_y
    size_x = tetromino.size_x
    size_y = tetromino.size_y
    for x in range(size_x):
        for y in range(size_y):
            if form[y][x] == 1:
                board[pos_y + y][pos_x + x] = 1
    return board


def draw_grid(grid):
    if grid == 0:
        sys.stdout.write(" ")
    else:
        sys.stdout.write(str(grid))


def draw_board(board):
    clear_console()
    for row in board:
        for col in row:
            draw_grid(col)
        sys.stdout.write("\n")
    sys.stdout.write("\nExplanation:\n")
    sys.stdout.write("\tMove right: {}\n".format(KEY_MOVE_RIGHT))
    sys.stdout.write("\tMove left: {}\n".format(KEY_MOVE_LEFT))
    sys.stdout.write("\tMove down: {}\n".format(KEY_MOVE_DOWN))
    sys.stdout.write("\tRotate: {}\n".format(KEY_ROTATE))
    sys.stdout.write("\tPause: {}\n".format(KEY_PAUSE))


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def is_gameover(board):
    for row in board[:TOP_EDGE_SIZE - 1]:
        for col in row:
            if col == 2:
                return True
    return False


class Tetromino:
    def __init__(self, board):
        self.form = self.get_random_tetromino()
        self.pos_x = self.get_init_position_x()
        self.pos_y = self.get_init_position_y()
        self.size_x = len(self.form[0])
        self.size_y = len(self.form)
        self.board = board

    def get_random_tetromino(self):
        return random.choice(TETROMINOS)

    def get_init_position_x(self):
        return random.randint(1, 8)

    def get_init_position_y(self):
        return 0

    def move_right(self):
        if self.can_move_right():
            self.pos_x += 1

    def can_move_right(self):
        return self.is_no_overlap(self.form, [1, 0])

    def move_left(self):
        if self.can_move_left():
            self.pos_x += -1

    def can_move_left(self):
        return self.is_no_overlap(self.form, [-1, 0])

    def move_down(self):
        if self.can_move_down():
            self.pos_y += 1

    def can_move_down(self):
        return self.is_no_overlap(self.form, [0, 1])

    def rotate(self):
        new_size_x = self.size_y
        new_size_y = self.size_x
        new_form = self.form[::-1]
        new_form = [x for x in zip(*new_form)]
        if self.can_rotate(new_form):
            self.form = new_form
            self.size_x = new_size_x
            self.size_y = new_size_y

    def can_rotate(self, new_form):
        return self.is_no_overlap(new_form, [0, 0])

    def is_no_overlap(self, form, next_pos):
        x = next_pos[0]
        y = next_pos[1]
        for v in range(len(form)):
            for h in range(len(form[0])):
                grid_x = self.pos_x + h + x
                grid_y = self.pos_y + v + y
                if form[v][h] + self.board[grid_y][grid_x] >= 3:
                    return False
        return True


if __name__ == '__main__':
    main()
