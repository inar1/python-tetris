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
KEY_ROTATE_CLOCKWISE = 'w'
KEY_ROTATE_ANTICLOCKWISE = 'e'

LOOP_TIME = 1

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
         [1, 1]]
]


def main():
    board = init_gameboard()
    tetromino = Tetromino(board)
    last_moving_time = time.time()
    while not is_gameover(board):
        current_time = time.time()
        time_diff = current_time - last_moving_time

        # controll position of tetromino
        if keyboard.press_and_release(KEY_MOVE_RIGHT):
            tetromino.move_right()
        elif keyboard.press_and_release(KEY_MOVE_LEFT):
            tetromino.move_left()
        elif keyboard.press_and_release(KEY_ROTATE_CLOCKWISE):
            tetromino.rotate_clockwise()
        elif keyboard.press_and_release(KEY_ROTATE_ANTICLOCKWISE):
            tetromino.rotate_anticlockwise()

        if time_diff > LOOP_TIME:
            if tetromino.can_move_down():
                tetromino.move_down()
                last_moving_time = time.time()
            else:
                merge_tetromino(board, tetromino)
                tetromino = Tetromino(board)
        board = remove_completed_row(board)
        board = append_tetromino(refresh_board(board), tetromino)
        if time_diff > LOOP_TIME:
            draw_board(board)
        # pdb.set_trace()  # for testing purpose


def init_gameboard():
    board = []
    for v in range(CANVAS_VERTICAL + TOP_EDGE_SIZE):
        board.append(create_board_row())
    board.append([3 for x in range(CANVAS_HORIZONTAL + (EDGE_SIZE * 2))])
    return board


def remove_completed_row(board):
    for row_index in range(len(board) - EDGE_SIZE):
        if 0 not in board[row_index]:
            board.pop(row_index)
            board.insert(0, create_board_row())
    return board


def create_board_row():
    line = []
    for h in range(CANVAS_HORIZONTAL + (EDGE_SIZE * 2)):
        index = h + 1
        if index <= EDGE_SIZE:
            line.append(3)
        elif h >= EDGE_SIZE + CANVAS_HORIZONTAL:
            line.append(3)
        else:
            line.append(0)
    return line


def refresh_board(board):
    for v in range(len(board)):
        for h in range(len(board[0])):
            if board[v][h] < 2:
                board[v][h] = 0
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


def draw_board(board):
    clear_board()
    for row in board:
        for col in row:
            sys.stdout.write(str(col))
        sys.stdout.write("\n")


def clear_board():
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

    def command(self, event):
        if event.key == KEY_MOVE_RIGHT:
            self.move_right()
        elif event.key == KEY_MOVE_LEFT:
            self.move_left()
        elif event.key == KEY_ROTATE_CLOCKWISE:
            self.rotate_clockwise()
        elif event.ky == KEY_ROTATE_ANTICLOCKWISE:
            self.rotate_anticlockwise()

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

    def rotate_clockwise(self):
        pass

    def rotate_anticlockwise(self):
        pass

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
