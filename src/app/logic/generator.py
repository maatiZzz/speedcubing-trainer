import random

class Generator:
    def __init__(self):
        self.moves = ['U', 'D', 'R', 'L', 'F', 'B', 'U\'', 'D\'', 'R\'', 'L\'', 'F\'', 'B\'']
        self.double_move_chance = 0.5
        self.sequence = ''

    def generate_sequence(self):
        length = random.randint(20, 22)
        sequence = []
        last_move = None

        for _ in range(length):
            random_move = random.choice(self.moves)
            # don't repeat last move
            if sequence:
                last_move = str(sequence[-1])
            if last_move and (random_move[0] in last_move 
                              or (random_move[0] == 'R' and 'L' in last_move or random_move[0] == 'L' and 'R' in last_move)
                              or (random_move[0] == 'U' and 'D' in last_move or random_move[0] == 'D' and 'U' in last_move)
                              or (random_move[0] == 'F' and 'B' in last_move or random_move[0] == 'B' and 'F' in last_move)
                              ):
                length += 1
                continue

            
            if random.random() < self.double_move_chance and '\'' not in random_move:
                sequence.append("2" + random_move)
            else:
                sequence.append(random_move)
            
        self.sequence = sequence

    def get_sequence(self):
        return self.sequence

    def get_sequence_str(self):
        sq = ""
        
        for move in self.sequence:
           sq += move + "   "

        return sq