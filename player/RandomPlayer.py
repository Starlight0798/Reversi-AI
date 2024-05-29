import random      

class RandomPlayer:
    def __init__(self, color):
        self.color = color

    def random_choice(self, board):
        action_list = list(board.get_legal_actions(self.color))

        if len(action_list) == 0:
            return None
        else:
            return random.choice(action_list)

    def get_move(self, board):
        if self.color == 'X':
            player_name = 'Black'
        else:
            player_name = 'White'
        action = self.random_choice(board)
        return action
