# !/usr/bin/Anaconda3/python
# -*- coding: utf-8 -*-

from func_timeout import func_timeout, FunctionTimedOut
import datetime
from core.board import Board
from copy import deepcopy


class Game(object):
    def __init__(self, black_player, white_player):
        self.board = Board()
        self.current_player = None
        self.black_player = black_player
        self.white_player = white_player
        self.black_player.color = "X"
        self.white_player.color = "O"

    def switch_player(self, black_player, white_player):
        if self.current_player is None:
            return black_player
        else:
            if self.current_player == self.black_player:
                return white_player
            else:
                return black_player

    def print_winner(self, winner):
        print(['Black win!', 'White win!', 'Draw'][winner])

    def force_loss(self, is_timeout=False, is_board=False, is_legal=False):
        if self.current_player == self.black_player:
            win_color = 'White - O'
            loss_color = 'Black - X'
            winner = 1
        else:
            win_color = 'Black - X'
            loss_color = 'White - O'
            winner = 0

        if is_timeout:
            print(f'\n{loss_color} has thought for more than 60s, {win_color} wins')
        if is_legal:
            print(f'\n{loss_color} has made 3 illegal moves, {win_color} wins')
        if is_board:
            print(f'\n{loss_color} has modified the board, {win_color} wins')

        diff = 0

        return winner, diff

    def run(self):
        total_time = {"X": 0, "O": 0}
        step_time = {"X": 0, "O": 0}
        winner = None
        diff = -1

        print('\n=====Game start!=====\n')
        self.board.display(step_time, total_time)
        while True:
            self.current_player = self.switch_player(self.black_player, self.white_player)
            start_time = datetime.datetime.now()
            color = "X" if self.current_player == self.black_player else "O"
            legal_actions = list(self.board.get_legal_actions(color))
            if len(legal_actions) == 0:
                if self.game_over():
                    winner, diff = self.board.get_winner()
                    break
                else:
                    continue

            board = deepcopy(self.board._board)

            try:
                for i in range(0, 3):
                    action = func_timeout(60, self.current_player.get_move, kwargs={'board': self.board})

                    if action == "Q":
                        break
                    if action not in legal_actions:
                        print("Illegal move, please try again!")
                        continue
                    else:
                        break
                else:
                    winner, diff = self.force_loss(is_legal=True)
                    break
            except FunctionTimedOut:
                winner, diff = self.force_loss(is_timeout=True)
                break

            end_time = datetime.datetime.now()
            if board != self.board._board:
                winner, diff = self.force_loss(is_board=True)
                break
            if action == "Q":
                winner, diff = self.board.get_winner()
                break

            if action is None:
                continue
            else:
                es_time = (end_time - start_time).seconds
                if es_time > 60:
                    print(f'\n{self.current_player} thought for more than 60s')
                    winner, diff = self.force_loss(is_timeout=True)
                    break

                self.board._move(action, color)
                if self.current_player == self.black_player:
                    step_time["X"] = es_time
                    total_time["X"] += es_time
                else:
                    step_time["O"] = es_time
                    total_time["O"] += es_time
                self.board.display(step_time, total_time)

                if self.game_over():
                    winner, diff = self.board.get_winner()
                    break

        print('\n=====Game over!=====\n')
        self.board.display(step_time, total_time)
        self.print_winner(winner)

        if winner is not None and diff > -1:
            result = {0: 'black_win', 1: 'white_win', 2: 'draw'}[winner]
            return result, diff

    def game_over(self):
        b_list = list(self.board.get_legal_actions('X'))
        w_list = list(self.board.get_legal_actions('O'))

        is_over = len(b_list) == 0 and len(w_list) == 0

        return is_over

    
class SilentGame(Game):
    def __init__(self, black_player, white_player, board=Board(), current_player=None):
        super().__init__(black_player, white_player)
        self.board = deepcopy(board)
        self.current_player = current_player
        
    def run(self):
        total_time = {"X": 0, "O": 0}
        step_time = {"X": 0, "O": 0}
        winner = None
        diff = -1

        while True:
            self.current_player = self.switch_player(self.black_player, self.white_player)
            start_time = datetime.datetime.now()
            color = "X" if self.current_player == self.black_player else "O"
            legal_actions = list(self.board.get_legal_actions(color))
            if len(legal_actions) == 0:
                if self.game_over():
                    winner, diff = self.board.get_winner()
                    break
                else:
                    continue

            action = self.current_player.get_move(self.board)

            if action is None:
                continue
            else:
                self.board._move(action, color)
                if self.game_over():
                    winner, diff = self.board.get_winner()
                    break

        return winner, diff
