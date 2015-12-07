import re


class Frw:

    def __init__(self, info, adress):
        self.info = info
        self.adress = adress

    def cast_line(self, line):
        if '!' in line:
            line = line.split('!', 1)
            line = list(map(lambda x: x.strip(), line))
        else:
            line = [line, '']
        line[0] = re.split('\s+', line[0])
        line[1] = line[1].split('!')
        return line


# a = 'abb aa  hh'
# b = Frw('a', 'a')
# print(b.cast_line(a))
