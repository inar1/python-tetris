#!/usr/bin/python3

import os
import random
import sys

CANVAS_HORIZONTAL = 10
CANVAS_VERTICAL = 20
TOP_EDGE_SIZE = 5
EDGE_SIZE = 1

KEY_MOVE_RIGHT = ''
KEY_MOVE_LEFT = ''
KEY_ROTATE_CLOCKWISE = ''
KEY_ROTATE_ANTICLOCKWISE = ''

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
    # while True:
    #    clear_board()
    #    draw_board(board)
    clear_board()
    if not is_tetromino_exist():
        tetromino = Tetromino()
    merge_board(board, tetromino)
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
    pass


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
        self.form = self.get_random_tetrimino()
        self.position_x = self.get_init_position_x()
        self.position_y = self.get_init_position_y()
        self.board = board

    def get_random_tetromino():
        return random.choise(TETROMINOS)

    def get_init_position_x():
        return (CANVAS_HORIZONTAL + (EDGE_SIZE * 2)) / 2

    def get_init_position_y():
        return 0

    def move_right(piece):
        pass

    def can_move_right():
        pass

    def move_left(piece):
        pass

    def can_move_left():
        pass

    def move_down(self, piece):
        if self.can_move_down():
            self.position_y += 1

    def can_move_down():
        pass

    def rotate_clockwise(piece):
        pass

    def rotate_anticlockwise(piece):
        pass

    def check_overlap():
        pass


if __name__ == '__main__':
    main()
