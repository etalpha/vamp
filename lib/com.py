from .frw import Frw
from .info import Info
import re
import numpy as np
import os


class Com(Frw):

    def cast_line(self, line):
        line = line.split('!', 1)[0]
        line = line.strip()
        line = re.split('\s+', line)
        return line

    def read(self, adress):
        self.info.incar['SYSTEM'] = os.path.basename(adress)[:-4]  # removing .com
        self.info.lattice.append(np.array((0, 0, 0)))
        self.info.lattice.append(np.array((0, 0, 0)))
        self.info.lattice.append(np.array((0, 0, 0)))
        self.start_reading(adress)
        line = self.nextline()
        while line[0] != '':
            line = self.nextline()
        line = self.nextline()
        while line[0] != '':
            line = self.nextline()
        line = self.nextline()
        line = self.nextline()
        while line[0] != '':
            self.info.add_atom(line[0], (line[1], line[2], line[3]))
            line = self.nextline()
        self.end_reading()
