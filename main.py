import random

moves = ['U', 'D', 'R', 'L', 'F', 'B', 'U\'', 'D\'', 'R\'', 'L\'', 'F\'', 'B\'']

def generate_sequence(moves):
    length = random.randint(16, 22)
    sequence = []

    double_move_chance = 0.3

    for _ in range(length):
        if random.random() < double_move_chance:
            sequence.append("2" + moves[random.randint(0, len(moves) - 1)])
        else:
            sequence.append(moves[random.randint(0, len(moves) - 1)])
        
    return sequence

def print_sequence(sequence):
    
    for _ in range(6): print()
    for move in sequence:
        print(f" {move} ", end="\t")
    for _ in range(6): print()

sq = generate_sequence(moves)
print_sequence(sq)