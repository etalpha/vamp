from frw import Frw
from info import Info
import numpy as np
from atom import Atom


class Poscar(Frw):

    def add_atom(self, atom, line):
        if line[0][0][0] in ['s', 'S']:
            self.info.selective_dynamics = True
        elif line[0][0][0] in ['c', 'C']:
            self.info.cartesian = True
        else:
            self.info.atoms.append(Atom(atom, line[0][0:3]))
            if len(line[0]) >= 6:
                self.info.atoms[-1]['TF'] = line[0][3:6]
            if 'M' in line[1]:
                self.info.atoms[-1]['m'] = line[
                    1][line[1].index('M') + 1]
            if 'B' in line[1]:
                self.info.atoms[-1]['b'] = line[
                    1][line[1].index('B') + 1]

    def read(self):
        self.start_reading()
        self.info.info['comment'] = ''.join(self.nextline()[0])
        self.info.scale = self.nextline()[0][0]
        self.info.lattice.append(np.array(self.nextline()[0][0:3], float))
        self.info.lattice.append(np.array(self.nextline()[0][0:3], float))
        self.info.lattice.append(np.array(self.nextline()[0][0:3], float))
        elems = self.nextline()[0]
        nums = self.nextline()[0]
        for elem, num in zip(elems, nums):
            self.info.elements.set_element(elem, num)
        line = self.nextline()
        for atom in self.info.elements.dic:
            for i in range(self.info.elements.dic[atom].num):
                self.add_atom(atom, line)
                line = self.nextline()

    def write(self, adress):
        pass

# a = Poscar(Info(), 'POSCAR')
# a.read()
