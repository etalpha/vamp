from .frw import Frw
import re
import numpy as np


class Doscar(Frw):
    def read(self, adress):
        self.start_reading(adress)
        line = self.nextline()
        line = self.nextline()
        line = self.nextline()
        line = self.nextline()
        line = self.nextline()
        info = self.nextline()
        for i in range(int(info[2])):
            line = self.nextline()
        for atom in self.info.atoms:
            info = self.nextline()
            atom.pdos = []
            for i in range(int(info[2])):
                line = self.nextline()
                line = list(map(float, line))
                atom.pdos.append(line)
            atom.pdos = np.array(atom.pdos)

    def cast_line(self, line):
        line = line.strip()
        line = re.split('\s+', line)
        return line
