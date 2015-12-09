from atom import Atom
from elements import Elements


class Atoms(list):

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
            elements.add_element(atom.name)
        elements.dic_to_lis()
        return elements

    # def create_element_list(self):
    #     self.sort()
    #     elements = Elements()
    #     for atom in self:
    #         elements.add_element(atom.name)
    #     return elements.element_list()

    def translation(self, vector):
        for atom in self:
            atom += vector

    def transform(self, matrix):
        for atom in self:
            atom.transform(matrix)

    def set_belong(self, name):
        for atom in self:
            atom['b'] = name
