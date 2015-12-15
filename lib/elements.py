from .element import Element
from collections import OrderedDict


class Elements(OrderedDict):

    def __init__(self, elements=None):
        OrderedDict.__init__(self)
        if elements:
            if type(elements) == Elements:
                for key, val in elements.items:
                    self[key] = Element(val)
            else:
                raise TypeError

    def add_atom(self, name):
        if name not in self:
            self[name] = Element(name)
        self[name].num += 1

    def set_element(self, name, num):
        if name not in self:
            self[name] = Element(name, num)

    def name_list(self):
        lis = []
        for elem in self:
            lis.append(elem)
        return lis

    def num_list(self):
        lis = []
        for elem in self.values():
            lis.append(str(int(elem.num)))
        return lis


# a = Elements()
# a.add_element('Au')
# a.add_element('Au')
# a.add_element('Ag')
# a.add_element('Au')
#
# b = a.element_list()
# for i in b:
#     print(i.name)
#     print(i.num)
