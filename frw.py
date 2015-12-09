import re


class Frw:

    def __init__(self, info, adress=None):
        self.info = info

    def start_reading(self, adress):
        self.f = open(adress, 'r')

    def nextline(self):
        line = self.f.readline()
        if line:
            return self.cast_line(line)

    def f_to_num(self, num):
        raise NotImplementedError

    def num_to_f(self, num):
        l = len(str(num))
        ret = str(num) + '0' * (18 - l)
        return ret

    def array_to_f(self, arr):
        arr = list(arr)
        arr = map(str, arr)
        arr = map(self.num_to_f, arr)
        arr = ' '.join(arr)
        return arr

# a = 'abb aa  hh\n'
# b = Frw('a', 'a')
# print(b.cast_line(a))
