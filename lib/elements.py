from .element import Element
from collections import OrderedDict


class Elements(OrderedDict):

    def __init__(self, elements=None):
        OrderedDict.__init__(self)
        if elements:
            if type(elements) == Elements:
                for key, val in elements.items:
                    self[key] = Element(val)

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

    def merge(self, other):
        for elem in other:
            if elem not in self:
                self[elem] = Element(other[elem])
            else:
                self[elem].num += other[elem].num
        tmp_dic = OrderedDict(sorted(self.items()))
        self.clear()
        for key, val in tmp_dic.items():
            self[key] = val

# a = Elements()
# a.add_atom('Au')
# a.add_atom('Au')
# a.add_atom('U')
# a.add_atom('Ag')
# a.add_atom('Au')
#
# b = Elements()
# b.add_atom('Au')
# b.add_atom('Cu')
#
# a.merge(b)
# for elem in a:
#     print(elem)
#     print(a[elem].num)
