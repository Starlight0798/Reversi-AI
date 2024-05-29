from bench.benchmark import run_benchmarks
from player.HumanPlayer import HumanPlayer
from player.RandomPlayer import RandomPlayer
from player.RoxannePlayer import RoxannePlayer
from player.MCTSPlayer import MCTSPlayer

if __name__ == "__main__":
    players = {
        "Roxanne": RoxannePlayer,
        "MCTS": MCTSPlayer
    }
    run_benchmarks(players, games=10)