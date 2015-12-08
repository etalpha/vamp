from atoms import Atoms
from atom import Atom
from elements import Elements
from element import Element
import numpy as np


class Info:

    def __init__(self):
        self.atoms = Atoms()
        self.elements = Elements()
        self.scale = 0
        self.lattice = []
        self.selective_dynamics = False
        self.cartesian = False
        self.info = dict()

    def add_atom(self, name, coodinate, TF, magmom=None, belong=None):
        self.atoms.append(Atom(name, coodinate, TF, magmom, belong))

    def add_element(self, name, num, LUAUL=None, LUAUU=None, LUAUJ=None):
        self.elements.add_element(name)
        self.elements[name].num = num
        self.elements[name].LUAUL = LUAUL
        self.elements[name].LUAUU = LUAUU
        self.elements[name].LUAUJ = LUAUJ

