from .atoms import Atoms
from .atom import Atom
from .elements import Elements
from .element import Element
import numpy as np
from collections import OrderedDict
import re
import copy

class Info:

    def __init__(self, info=None):
        self.atoms = Atoms()
        self.elements = Elements()
        self.scale = 0
        self.lattice = []
        self.selective_dynamics = False
        self.cartesian = False
        self.incar = OrderedDict()
        if info:
            if type(info) == Info:
                    self.__dict__ = copy.deepcopy(info.__dict__)
            else:
                raise TypeError

    def add_atom(self, name, coodinate=(0,0,0), TF=(True,True,True), magmom=None, belong=None):
        self.atoms.append(Atom(name, coodinate, TF, magmom, belong))

    def add_element(self, name, num, LUAUL=None, LUAUU=None, LUAUJ=None):
        self.elements[name] = Element(name, num, LUAUL, LUAUU, LUAUJ)

    def create_elements(self):
        self.elements = self.atoms.create_elements()

    def set_magmom_pos_to_in(self):
        lis = []
        for atom in self.atoms:
            lis.append(atom['m'])
        self.incar['MAGMOM'] = ' '.join(map(str, lis))

    def set_magmom_in_to_pos(self):
        if 'MAGMOM' in self.incar:
            mag = self.incar['MAGMOM']
            mag = mag.split('!')[0]
            mags = re.split('\s+', mag)
            for i in range(len(mags)):
                if '*' in mags[i]:
                    mags[i] = mags[i].split('*')
                else:
                    mags[i] = ['1', mags[i]]
            lis = []
            for mag in mags:
                for i in range(int(mag[0])):
                    lis.append(mag[1])
            for m, atom in zip(lis, self.atoms):
                atom['m'] = m

    def __add__(self, other):
        ret = copy.deepcopy(self)
        add = copy.copy(other)
        for atom in add.atoms:
            ret.atoms.append(atom)
        ret.set_magmom_pos_to_in()
        ret.atoms.sort('name')
        ret.elements = ret.atoms.create_elements()
        return ret

    def split(self):
        self.set_magmom_in_to_pos()
        dic = dict()
        for atom in self.atoms:
            if atom['b'] not in dic:
                dic[atom['b']] = copy.deepcopy(self)
                dic[atom['b']].incar['SYSTEM'] = atom['b']
                dic[atom['b']].atoms = Atoms()
            dic[atom['b']].atoms.append(atom)
        return dic
