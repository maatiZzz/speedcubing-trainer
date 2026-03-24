import random

moves = ['U', 'D', 'R', 'L', 'F', 'B', 'U\'', 'D\'', 'R\'', 'L\'', 'F\'', 'B\'']

def generate_sequence(moves):
    length = random.randint(16, 22)
    sequence = []

    double_move_chance = 0.3

    for _ in range(length):
        random_index = random.randint(0, len(moves) - 1)

        # don't repeat last move
        if sequence and moves[random_index] in sequence[-1]:
             length += 1
             continue
        
        if random.random() < double_move_chance:
                sequence.append("2" + moves[random_index])
        else:
            sequence.append(moves[random_index])
        
    return sequence

def print_sequence(sequence):
    
    for _ in range(6): print()
    for move in sequence:
        print(f" {move} ", end="\t")
    for _ in range(6): print()

sq = generate_sequence(moves)
print_sequence(sq)