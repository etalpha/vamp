from .frw import Frw
from .info import Info
import numpy as np
from .atom import Atom
import re
from .atoms import Atoms
from .elements import Elements

class Poscar(Frw):

    def __add_atom(self, atom, line):
        # a = Atom(atom, line[0][0:3])
        self.info.atoms.append(Atom(atom, line[0][0:3]))
        if len(line[0]) >= 6:
            self.info.atoms[-1]['TF'] = line[0][3:6]
        if '!M' in line[1]:
            self.info.atoms[-1]['m'] = line[
                1][line[1].index('!M') + 1]
        if '!B' in line[1]:
            self.info.atoms[-1]['b'] = line[
                1][line[1].index('!B') + 1]
        if '!C' in line[1]:
            self.info.atoms[-1].comment = line[
                    1][line[1].index('!C') + 1]

    def read(self, adress):
        self.start_reading(adress)
        self.info.incar['SYSTEM'] = ''.join(self.nextline()[0])
        self.info.scale = self.nextline()[0][0]
        self.info.lattice.append(np.array(self.nextline()[0][0:3], float))
        self.info.lattice.append(np.array(self.nextline()[0][0:3], float))
        self.info.lattice.append(np.array(self.nextline()[0][0:3], float))
        elems = self.nextline()[0]
        nums = self.nextline()[0]
        for elem, num in zip(elems, nums):
            self.info.elements.set_element(elem, num)
        line = self.nextline()
        for atom in self.info.elements:
            for i in range(self.info.elements[atom].num):
                while line[0][0].isalpha():
                    if line[0][0][0] in ['s', 'S']:
                        self.info.selective_dynamics = True
                        line = self.nextline()
                    elif line[0][0][0] in ['D', 'd']:
                        self.info.selective_dynamics = False
                        line = self.nextline()
                    elif line[0][0][0] in ['c', 'C']:
                        self.info.cartesian = True
                        line = self.nextline()
                    else:
                        raise RuntimeError('error when reading poscar')
                self.__add_atom(atom, line)
                line = self.nextline()
        self.info.create_elements()
        self.end_reading()

    def write(self, adress):
        self.info.atoms.sort()
        self.info.create_elements()
        f = open(adress,'w')
        f.write(self.info.incar['SYSTEM'] + '\n')
        f.write(self.num_to_f((self.info.scale)) + '\n')
        f.write(self.array_to_f(self.info.lattice[0]) + '\n')
        f.write(self.array_to_f(self.info.lattice[1]) + '\n')
        f.write(self.array_to_f(self.info.lattice[2]) + '\n')
        f.write(' '.join(self.info.elements.name_list()) + '\n')
        f.write(' '.join(self.info.elements.num_list()) + '\n')
        if self.info.selective_dynamics == True:
            f.write('selective dynamics\n')
        if self.info.cartesian == True:
            f.write('cartesian\n')
        else:
            f.write('Direct\n')
        for atom in self.info.atoms:
            f.write(self.array_to_f(atom.coodinate) + ' ')
            f.write(' '.join(atom['TF']))
            if atom.magmom is not None:
                f.write(' !M '+str(atom.magmom))
            if atom.belong:
                f.write(' !B '+str(atom.belong))
            if atom.comment:
                f.write(' !C '+str(atom.comment))
            f.write('\n')
        f.close()

    def cast_line(self, line):
        line = line.strip()
        if '!' in line:
            line = line.split('!', 1)
            line = list(map(lambda x: x.strip(), line))
        else:
            line = [line, '']
        line[0] = re.split('\s+', line[0])
        line[1] = re.split('\s+', '!' + line[1])
        return line
