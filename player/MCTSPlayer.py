from math import log, sqrt
from time import time
from copy import deepcopy
from core.game import SilentGame
from player.RoxannePlayer import RoxannePlayer
import concurrent.futures
import threading

class TreeNode:
    def __init__(self, parent, color):
        self.parent = parent
        self.w = 0
        self.n = 0
        self.color = color
        self.child = dict()
        self.lock = threading.Lock()

class MCTSPlayer:
    def __init__(self, color, time_limit=0.5, c_param=sqrt(2), num_threads=4):
        self.c_param = c_param
        self.time_limit = time_limit
        self.num_threads = num_threads
        self.tick = 0
        self.sim_black = RoxannePlayer('X')
        self.sim_white = RoxannePlayer('O')
        self.color = color

    def mcts(self, board):
        root = TreeNode(None, self.color)
        self.tick = time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = [executor.submit(self.simulation_thread, root, deepcopy(board)) for _ in range(self.num_threads)]
            for future in concurrent.futures.as_completed(futures):
                pass  

        best_n = -1
        best_move = None
        for k in root.child.keys():
            if root.child[k].n > best_n:
                best_n = root.child[k].n
                best_move = k
        return best_move

    def simulation_thread(self, root, board):
        while time() - self.tick < self.time_limit:
            sim_board = deepcopy(board)
            choice = self.select(root, sim_board)
            self.expand(choice, sim_board)
            winner, diff = self.simulate(choice, sim_board)
            back_score = [1, 0, 0.5][winner]
            if choice.color == 'X':
                back_score = 1 - back_score
            self.back_prop(choice, back_score)

    def select(self, node, board):
        with node.lock:
            if len(node.child) == 0:
                return node
            else:
                best_score = -1
                best_move = None
                for k in node.child.keys():
                    if node.child[k].n == 0:
                        best_move = k
                        break
                    else:
                        N = node.n
                        n = node.child[k].n
                        w = node.child[k].w
                        score = w / n + self.c_param * sqrt(log(N) / n)
                        if score > best_score:
                            best_score = score
                            best_move = k
                board._move(best_move, node.color)
                return self.select(node.child[best_move], board)

    def expand(self, node, board):
        op_color = 'O' if node.color == 'X' else 'X'
        with node.lock:
            for move in board.get_legal_actions(node.color):
                if move not in node.child:
                    node.child[move] = TreeNode(node, op_color)

    def simulate(self, node, board):
        if node.color == 'O':
            current_player = self.sim_black
        else:
            current_player = self.sim_white
        sim_game = SilentGame(self.sim_black, self.sim_white, board, current_player)
        return sim_game.run()

    def back_prop(self, node, score):
        while node is not None:
            with node.lock:
                node.n += 1
                node.w += score
            score = 1 - score
            node = node.parent

    def get_move(self, board):
        self.tick = time()
        action = self.mcts(deepcopy(board))
        return action
