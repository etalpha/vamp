import re


class Frw:

    def __init__(self, info, adress):
        self.info = info
        self.adress = adress

    def start_reading(self):
        self.f = open(self.adress, 'r')

    def cast_line(self, line):
        line = line.strip()
        if '!' in line:
            line = line.split('!', 1)
            line = list(map(lambda x: x.strip(), line))
        else:
            line = [line, '']
        line[0] = re.split('\s+', line[0])
        line[1] = re.split('[\s!]+', line[1])
        return line

    def nextline(self):
        return self.cast_line(self.f.readline())


# a = 'abb aa  hh\n'
# b = Frw('a', 'a')
# print(b.cast_line(a))
