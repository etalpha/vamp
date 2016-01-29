import numpy as np
from .atom import Atom
from .elements import Elements


class Atoms(list):

    def __init__(self, atoms=None):
        list.__init__(self)
        if atoms:
            if isinstance(atoms, Atoms):
                for atom in atoms:
                    self.append(Atom(atom))
            else:
                raise TypeError

    def append(self, object):
        if type(object) is not Atom:
            raise TypeError
        else:
            list.append(self, object)

    def sort(self, key1='name', key2=None, key3=None, key4=None, key5=None,
             key6=None):
        list.sort(self, key=lambda x: (
            x[key1], x[key2], x[key3], x[key4], x[key5], x[key6]))
        return self

    def merge(self, other):
        for atom in other:
            self.append(Atom(atom))
        self.sort('name')

    def create_elements(self):
        self.sort()
        elements = Elements()
        for atom in self:
            elements.add_atom(atom.name)
        return elements

    def translation(self, vector, belong=None):
        for atom in self:
            if belong is None or atom.belong == belong:
                atom.translation(vector)

    def transform(self, matrix, belong=None):
        for atom in self:
            if belong is None or atom.belong == belong:
                atom.transform(matrix)

    def rotation(self, axis, center, theta=None, belong=None):
        cp_axis = np.array(axis)
        cp_center = np.array(center)
        for atom in self:
            if belong is None or atom.belong == belong:
                atom.rotation(cp_axis, cp_center, theta)

    def cartesianyzation(self, lattice):
        for atom in self:
            atom.cartesianyzation(lattice)

    def set_belong(self, name):
        for atom in self:
            atom['b'] = name

    def reverse_mag(self):
        for atom in self:
            atom.magmom = -atom.magmom

    def __getitem__(self, key):
        return list.__getitem__(self, key - 1)

    def __setitem__(self, key, val):
        list.__setitem__(self, key - 1, val)
