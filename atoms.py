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
        return elements.element_list()


# a = Atoms()
# a.append(Atom('Au', (0, 0, 0)))
# a.append(Atom('Ag', (1, 1, 0)))
# a.append(Atom('Ag', (0, 0, 0)))
# a.append(Atom('Ag', (0, 1, 0)))
# a.sort('name', 'z', 'x', 'y')
# b = a.create_elements()
# for i in b:
#     print(i.name)
#     print(i.num)
