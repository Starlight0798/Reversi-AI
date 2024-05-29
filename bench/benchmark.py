from core.game import SilentGame
import itertools
import time

def benchmark(player1, player2, games=10):
    total_wins_black = []
    total_wins_white = []
    results = {"black_win": 0, "white_win": 0, "draw": 0}
    winner_name = {0: 'Black', 1: 'White'}

    for i in range(games):
        print(f'Game {i+1}: ', end='')
        game = SilentGame(player1, player2)
        winner, diff = game.run()
        if winner == 2:
            results["draw"] += 1
            print('Draw')
        else:
            if winner == 0:
                results["black_win"] += 1
                total_wins_black.append(diff)
            else:
                results["white_win"] += 1
                total_wins_white.append(diff)
            print(f'{winner_name[winner]} wins, lead by {diff} pieces')

    print("\nBenchmark Results:")
    print(f"Black Wins: {results['black_win']}")
    print(f"White Wins: {results['white_win']}")
    print(f"Draws: {results['draw']}")

    return total_wins_black, total_wins_white


def run_benchmarks(players, games=10):
    player_names = list(players.keys())
    combinations = itertools.permutations(player_names, 2)

    for black, white in combinations:
        print(f"\nRunning benchmark: {black} (black) vs {white} (white)")
        black_player = players[black]("X")
        white_player = players[white]("O")
        start_time = time.time()
        benchmark(black_player, white_player, games=games)
        end_time = time.time()
        print(f"Total time: {end_time - start_time} seconds")