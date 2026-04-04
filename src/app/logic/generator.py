import random
from app.constants.constants import DOUBLE_MOVE_CHANCE, BACKWARD_MOVE_CHANCE, SCRAMBLE_SEQUENCE_LENGTH, CASUAL_MOVE_CHANCE

class Generator:
    def __init__(self):
        self.moves = ['U', 'D', 'R', 'L', 'F', 'B']
        self.sequence = ''

    def generate_sequence(self):
        sequence = []
        last_move, last_last_move = None, None
        opposites = {
            'L' : 'R', 'R' : 'L',
            'U' : 'D', 'D' : 'U',
            'F' : 'B', 'B' : 'F'
        }

        while len(sequence) < SCRAMBLE_SEQUENCE_LENGTH:
            random_move = random.choice(self.moves)

            if sequence:
                last_move = str(sequence[-1]).replace("\'", "").replace("2", "")        # get clean move
                if len(sequence) > 1:
                    last_last_move = str(sequence[-2]).replace("\'", "").replace("2", "")
            # don't repeat last move
            if last_move and random_move == last_move:
                continue
            # avoid 3 moves in the same axis in a row (f.e. RUR is allowed but RLR is not)
            if last_last_move and random_move == last_last_move and random_move == opposites[last_move]:
                continue
            
            move_type = random.choices(["\'", "2", ""], [BACKWARD_MOVE_CHANCE, DOUBLE_MOVE_CHANCE, CASUAL_MOVE_CHANCE])
            # print(str(move_type))
            if move_type[0] == '2':
                random_move = f"2{random_move}"
            else:
                random_move += f"{move_type[0]}"

            sequence.append(random_move)
            
        self.sequence = sequence
        print(self.sequence)

    def get_sequence(self):
        return self.sequence

    def get_sequence_str(self):
        sq = ""
        
        for move in self.sequence:
           sq += move + "   "

        return sq