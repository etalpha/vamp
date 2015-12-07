from atoms import Atoms
from elements import Elements


class Info:
    def __init__(self):
        self.atoms = Atoms()
        self.elements = Elements()
        self.selective_dynamics = False
        self.cartesian = False
        self.info = dict()
