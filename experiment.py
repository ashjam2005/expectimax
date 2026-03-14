import copy
import random
import matplotlib.pyplot as plt

from game import Game
from ai import AI


def can_move_in_direction(state, direction):
    """
    Check whether a move is valid by simulating it on a copied game.
    """
    tile_matrix, score = state
    sim = Game(copy.deepcopy(tile_matrix), score)
    return sim.move(direction)


def has_any_valid_move(state):
    """
    True iff at least one move is valid.
    """
    for direction in [0, 1, 2, 3]:
        if can_move_in_direction(state, direction):
            return True
    return False


def run_single_game(mode="exp1", max_moves=1000, seed=0):
    """
    mode:
        'exp1'          -> depth-1 expectimax with score leaves
        'exp3'          -> depth-3 expectimax with score leaves
        'exp3_improved' -> depth-3 expectimax with improved heuristic leaves
    """
    random.seed(seed)

    game = Game()
    scores = []

    for _ in range(max_moves):
        state = game.current_state()

        if not has_any_valid_move(state):
            break

        if mode == "exp1":
            ai = AI(state, search_depth=1)
            direction = ai.compute_decision()

        elif mode == "exp3":
            ai = AI(state, search_depth=3)
            direction = ai.compute_decision()

        elif mode == "exp3_improved":
            ai = AI(state, search_depth=3)
            direction = ai.compute_decision_ec()

        else:
            raise ValueError("Unknown mode")

        if direction is None:
            break

        moved = game.move(direction)

        # If AI somehow gives an invalid move, stop
        if not moved:
            break

        # Record actual engine score after the move
        _, score = game.current_state()
        scores.append(score)

    return scores


def run_multiple_games(mode, num_runs=5, max_moves=1000):
    all_runs = []
    for seed in range(num_runs):
        scores = run_single_game(mode=mode, max_moves=max_moves, seed=seed)
        all_runs.append(scores)
    return all_runs


def plot_runs(runs, title, filename):
    plt.figure(figsize=(8, 5))

    for i, scores in enumerate(runs):
        x = list(range(1, len(scores) + 1))
        plt.plot(x, scores, label=f"Run {i+1}")

    plt.xlabel("Move number")
    plt.ylabel("Actual game score")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=200)
    plt.show()


def average_curve(runs):
    max_len = max(len(run) for run in runs)
    avg = []

    for t in range(max_len):
        vals = [run[t] for run in runs if t < len(run)]
        avg.append(sum(vals) / len(vals))

    return avg


def plot_comparison(runs_a, runs_b, label_a, label_b, title, filename):
    avg_a = average_curve(runs_a)
    avg_b = average_curve(runs_b)

    x_a = list(range(1, len(avg_a) + 1))
    x_b = list(range(1, len(avg_b) + 1))

    plt.figure(figsize=(8, 5))
    plt.plot(x_a, avg_a, label=label_a)
    plt.plot(x_b, avg_b, label=label_b)

    plt.xlabel("Move number")
    plt.ylabel("Average actual game score")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=200)
    plt.show()


if __name__ == "__main__":
    # Question 3.1
    exp1_runs = run_multiple_games(mode="exp1", num_runs=5, max_moves=1000)
    exp3_runs = run_multiple_games(mode="exp3", num_runs=5, max_moves=1000)

    plot_runs(
        exp1_runs,
        "Q3.1: Exp-1 Performance (5 Runs)",
        "q3_1_exp1.png"
    )

    plot_runs(
        exp3_runs,
        "Q3.1: Exp-3 Performance (5 Runs)",
        "q3_1_exp3.png"
    )

    # Question 3.2
    exp3_improved_runs = run_multiple_games(mode="exp3_improved", num_runs=5, max_moves=1000)

    plot_runs(
        exp3_improved_runs,
        "Q3.2: Exp-3 with Improved Evaluation (5 Runs)",
        "q3_2_exp3_improved.png"
    )

    plot_comparison(
        exp3_runs,
        exp3_improved_runs,
        "Original Exp-3",
        "Improved Exp-3",
        "Q3.2: Original Exp-3 vs Improved Exp-3",
        "q3_2_comparison.png"
    )
