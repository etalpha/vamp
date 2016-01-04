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

    def create_elements(self):
        self.sort()
        elements = Elements()
        for atom in self:
            elements.add_atom(atom.name)
        return elements

    def translation(self, vector):
        for atom in self:
            atom += vector

    def transform(self, matrix):
        for atom in self:
            atom.transform(matrix)

    def set_belong(self, name):
        for atom in self:
            atom['b'] = name

    # def __getitem__(self, key):
    #     if isinstance(key,(int)):
    #         pass
    #
