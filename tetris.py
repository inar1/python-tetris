#!/usr/bin/python3

import os
import random
import sys

CANVAS_HORIZONTAL = 10
CANVAS_VERTICAL = 20
TOP_EDGE_SIZE = 5
EDGE_SIZE = 1

KEY_MOVE_RIGHT = 'd'
KEY_MOVE_LEFT = 'a'
KEY_ROTATE_CLOCKWISE = 'w'
KEY_ROTATE_ANTICLOCKWISE = 'e'

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
    tetrimino = None
    while not is_gameover():
        clear_board()
        if not tetrimino:
            tetromino = Tetromino(board)
        tetromino.move_down()
        board = merge_board(board, tetromino)
        draw_board(board)


def init_gameboard():
    board = []
    for v in range(CANVAS_VERTICAL + TOP_EDGE_SIZE):
        line = []
        for h in range(CANVAS_HORIZONTAL + (EDGE_SIZE * 2)):
            index = h + 1
            if index <= EDGE_SIZE:
                line.append(1)
            elif h >= EDGE_SIZE + CANVAS_HORIZONTAL:
                line.append(1)
            else:
                line.append(0)
        board.append(line)
    board.append([1 for x in range(CANVAS_HORIZONTAL + (EDGE_SIZE * 2))])
    return board


def clear_board():
    os.system('cls' if os.name == 'nt' else 'clear')


def merge_board(board, tetromino):
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
    for row in board:
        for column in row:
            sys.stdout.write(str(column))
        sys.stdout.write("\n")


def is_tetromino_exist():
    return False


def is_gameover():
    pass


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
        return 6

    def get_init_position_y(self):
        return 0

    def move_right(self):
        pass

    def can_move_right(self):
        pass

    def move_left(self):
        pass

    def can_move_left(self):
        pass

    def move_down(self):
        if self.can_move_down():
            self.position_y += 1

    def can_move_down(self):
        pass

    def rotate_clockwise(self, piece):
        pass

    def rotate_anticlockwise(self, piece):
        pass

    def check_overlap(self, future_position):
        pass


if __name__ == '__main__':
    main()
