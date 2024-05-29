class HumanPlayer:
    def __init__(self, color):
        self.color = color

    def get_move(self, board):
        player = "Black" if self.color == "X" else "White"

        while True:
            action = input(f'Please input a valid coordinate (e.g. "D3", if you want to quit, please input "Q"): ')

            if action.upper() == "Q":
                return "Q"
            else:
                row, col = action[1].upper(), action[0].upper()

                if row in '12345678' and col in 'ABCDEFGH':
                    if action in board.get_legal_actions(self.color):
                        return action
                else:
                    print("Invalid input, please try again.")
