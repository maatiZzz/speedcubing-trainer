from ursina import Entity
import ursina as ur

class InputHandler(Entity):
    def __init__(self):
        super().__init__()

    def input(self, key):
        if key == 'left mouse down':
            print("elo")