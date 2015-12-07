from element import Element


class Elements(dict):

    def add_element(self, name):
        if name not in self:
            self[name] = Element(name)
        self[name].num += 1

    def element_list(self):
        elemlist = []
        for key in self:
            elemlist.append(self[key])
        elemlist.sort(key=lambda x: x.name)
        return elemlist

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
