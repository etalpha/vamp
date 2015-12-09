import re
from frw import Frw


class Incar(Frw):

    def read(self, adress):
        self.start_reading(adress)
        line = self.nextline()
        while line:
            self.info.info[line[0]] = line[1]
            line = self.nextline()

    def write(self, adress):
        f = open(adress, 'w')
        for key in self.info.info:
            if key != '':
                f.write(key + '=' + self.info.info[key] + '\n')

    def cast_line(self, line):
        line = line.strip()
        if '=' in line:
            line = line.split('=', 1)
            line = list(map(lambda x: x.strip(), line))
        else:
            line = [line, '']
        return line
