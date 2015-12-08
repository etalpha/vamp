from element import Element


class Elements:

    def __init__(self):
        self.dic = dict()
        self.lis = list()

    def add_element(self, name):
        if name not in self.dic:
            self.dic[name] = Element(name)
        self.dic[name].num += 1

    def set_element(self, name, num):
        if name not in self.dic:
            self.dic[name] = Element(name)
        self.dic[name].num = int(num)

    def dic_to_lis(self):
        self.lis = []
        for key in self.dic:
            self.lis.append(self.dic[key])
        self.lis.sort(key=lambda x: x.name)

    def lis_to_dic(self):
        self.dic = dict()
        for elem in self.lis:
            self.add_element(elem.name)

    def element_list(self):
        self.dic_to_lis()
        return self.lis


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
