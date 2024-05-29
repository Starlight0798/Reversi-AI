#!/usr/bin/Anaconda3/python
# -*- coding: utf-8 -*-

class Board(object):
    def __init__(self):
        self.empty = '.'
        self._board = [[self.empty for _ in range(8)] for _ in range(8)]
        self._board[3][4] = 'X'
        self._board[4][3] = 'X'
        self._board[3][3], self._board[4][4] = 'O', 'O'

    def __getitem__(self, index):
        return self._board[index]

    def display(self, step_time=None, total_time=None):
        board = self._board
        print(' ', ' '.join(list('ABCDEFGH')))
        for i in range(8):
            print(str(i + 1), ' '.join(board[i]))
        if (not step_time) or (not total_time):
            step_time = {"X": 0, "O": 0}
            total_time = {"X": 0, "O": 0}
            print(f"Statistics: Total pieces / Time per move / Total time")
            print(f"Black: {self.count('X')} / {step_time['X']} / {total_time['X']}")
            print(f"White: {self.count('O')} / {step_time['O']} / {total_time['O']}\n")
        else:
            print(f"Statistics: Total pieces / Time per move / Total time")
            print(f"Black: {self.count('X')} / {step_time['X']} / {total_time['X']}")
            print(f"White: {self.count('O')} / {step_time['O']} / {total_time['O']}\n")

    def count(self, color):
        count = 0
        for y in range(8):
            for x in range(8):
                if self._board[x][y] == color:
                    count += 1
        return count

    def get_winner(self):
        black_count, white_count = 0, 0
        for i in range(8):
            for j in range(8):
                if self._board[i][j] == 'X':
                    black_count += 1
                if self._board[i][j] == 'O':
                    white_count += 1
        if black_count > white_count:
            return 0, black_count - white_count
        elif black_count < white_count:
            return 1, white_count - black_count
        elif black_count == white_count:
            return 2, 0

    def _move(self, action, color):
        if isinstance(action, str):
            action = self.board_num(action)

        flipped = self._can_flipped(action, color)

        if flipped:
            for flip in flipped:
                x, y = self.board_num(flip)
                self._board[x][y] = color

            x, y = action
            self._board[x][y] = color
            return flipped
        else:
            return False

    def backpropagation(self, action, flipped_pos, color):
        if isinstance(action, str):
            action = self.board_num(action)

        self._board[action[0]][action[1]] = self.empty
        op_color = "O" if color == "X" else "X"

        for p in flipped_pos:
            if isinstance(p, str):
                p = self.board_num(p)
            self._board[p[0]][p[1]] = op_color

    def is_on_board(self, x, y):
        return 0 <= x <= 7 and 0 <= y <= 7

    def _can_flipped(self, action, color):
        if isinstance(action, str):
            action = self.board_num(action)
        xstart, ystart = action

        if not self.is_on_board(xstart, ystart) or self._board[xstart][ystart] != self.empty:
            return False

        self._board[xstart][ystart] = color
        op_color = "O" if color == "X" else "X"

        flipped_pos = []
        flipped_pos_board = []

        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection
            y += ydirection
            if self.is_on_board(x, y) and self._board[x][y] == op_color:
                x += xdirection
                y += ydirection
                if not self.is_on_board(x, y):
                    continue
                while self._board[x][y] == op_color:
                    x += xdirection
                    y += ydirection
                    if not self.is_on_board(x, y):
                        break
                if not self.is_on_board(x, y):
                    continue
                if self._board[x][y] == color:
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        flipped_pos.append([x, y])

        self._board[xstart][ystart] = self.empty

        if len(flipped_pos) == 0:
            return False

        for fp in flipped_pos:
            flipped_pos_board.append(self.num_board(fp))
        return flipped_pos_board

    def get_legal_actions(self, color):
        direction = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

        op_color = "O" if color == "X" else "X"
        op_color_near_points = []

        board = self._board
        for i in range(8):
            for j in range(8):
                if board[i][j] == op_color:
                    for dx, dy in direction:
                        x, y = i + dx, j + dy
                        if 0 <= x <= 7 and 0 <= y <= 7 and board[x][y] == self.empty and (x, y) not in op_color_near_points:
                            op_color_near_points.append((x, y))
        l = [0, 1, 2, 3, 4, 5, 6, 7]
        for p in op_color_near_points:
            if self._can_flipped(p, color):
                if p[0] in l and p[1] in l:
                    p = self.num_board(p)
                yield p

    def board_num(self, action):
        row, col = str(action[1]).upper(), str(action[0]).upper()
        if row in '12345678' and col in 'ABCDEFGH':
            x, y = '12345678'.index(row), 'ABCDEFGH'.index(col)
            return x, y

    def num_board(self, action):
        row, col = action
        l = [0, 1, 2, 3, 4, 5, 6, 7]
        if col in l and row in l:
            return chr(ord('A') + col) + str(row + 1)
