import random

from engine.board import Board
from engine.board_estimation import check_game_state
from engine.bot import evaluate_best_move
from engine.data_types import GameState

POPULATION_SIZE = 20
NUM_GENERATIONS = 10
MUTATION_RATE = 0.01
CROSSOVER_RATE = 0.7

DEFAULT_BLACK_MODEL_COEFFS = [10, 5, -2, 10, -10]
TURNS_LIMIT = 50


population = [
    [random.uniform(-100, 100) for _ in range(5)]
    for _ in range(POPULATION_SIZE)
]


def calculate_fitness(chromosome):
    return challenge_white_bot(chromosome)


def select_parents(population):
    # TODO: Selected best bots, not just random.
    return random.sample(population, 2)


def crossover(parent1, parent2):
    # Implement crossover logic here
    # This is a placeholder for single-point crossover
    if random.random() < CROSSOVER_RATE:
        point = random.randint(1, len(parent1) - 2)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    else:
        return parent1, parent2


def mutate(chromosome):
    for i in range(len(chromosome)):
        if random.random() < MUTATION_RATE:
            chromosome[i] += random.uniform(-0.1, 0.1)


for generation in range(NUM_GENERATIONS):
    print('starting generation', generation)
    new_population = []
    for _ in range(POPULATION_SIZE // 2):
        parent1, parent2 = select_parents(population)
        child1, child2 = crossover(parent1, parent2)
        mutate(child1)
        mutate(child2)
        new_population.extend([child1, child2])

    population = sorted(new_population, key=calculate_fitness, reverse=True)[
        :POPULATION_SIZE
    ]


def challenge_white_bot(coefficients: list[float]):
    board = Board()
    turn_number = 1
    while (game_state := check_game_state(board)) == GameState.PLAYING:
        bot_coeffs = (
            coefficients if board.white_turn else DEFAULT_BLACK_MODEL_COEFFS
        )
        best_turn = evaluate_best_move(board, bot_coeffs)
        board.make_turn(best_turn)
        turn_number += 1
        if turn_number >= TURNS_LIMIT:
            break
    bot_value = (int(game_state == GameState.WHITE_WIN)) * 2 + turn_number / 50
    print(
        f'game finished on turn {turn_number}, '
        f'game state: {game_state}, '
        f'value: {bot_value}'
    )
    return bot_value


print("Optimized Coefficients:", population[0])
