from .frw import Frw
from .tag import Tag
from .atom import Atom
from .element import Element
import re
import numpy as np


class Chgcar(Frw):

    def cast_line(self, line):
        ret = line.strip()
        ret = re.split('\s+', ret)
        return ret

    def read(self, adress):
        self.start_reading(adress)
        SYS = self.nextline()
        self.info.tags['SYSTEM'] = Tag('SYSTEM', ' '.join(SYS))
        self.info.unit = self.nextline()[0]
        for i in range(3):
            self.info.lattice.append(self.nextline())
        names = self.nextline()
        nums = self.nextline()
        for name, num in zip(names, nums):
            self.info.elements[name] = Element(name, num)
        self.info.cartesian = self.nextline()[0]
        for key, val in self.info.elements.items():
            for i in range(1, val.num + 1):
                a = self.nextline()
                self.info.atoms.append(Atom(key, a))
        self.nextline()
        cells = self.nextline()
        cells = list(map(int, cells))
        self.info.chgcell = cells
        ncell = cells[0] * cells[1] * cells[2]
        chgs = []
        for i in range(int(ncell / 5) + 1):
            chgs += self.nextline()
        self.info.chgsum = chgs
        # aug
        for atom in self.info.atoms:
            chgs = []
            ncell = int(self.nextline()[3])
            for i in range(int(ncell / 5) + (0 if ncell % 5 == 0 else 1)):
                chgs += self.nextline()
            atom.augsum = chgs
        chgn = []
        for i in range(int(len(self.info.atoms) / 5 + 1)):
            n = self.nextline()
            if n is None:
                return None
            chgn += n
        for n, atom in zip(chgn, self.info.atoms):
            atom.chgn = n
        cells = self.nextline()
        cells = list(map(int, cells))
        ncell = cells[0] * cells[1] * cells[2]
        chgs = []
        for i in range(int(ncell / 5) + 1):
            chgs += self.nextline()
        self.info.chgdif = chgs
        # aug
        for atom in self.info.atoms:
            chgs = []
            ncell = int(self.nextline()[3])
            for i in range(int(ncell / 5) + 1):
                chgs += self.nextline()
            atom.augdif = chgs

    def write(self, adress):
        f = open(adress, 'w')
        f.write(self.info.tags['SYSTEM'].val + '\n')
        f.write('   ' + '{0:<16.14f}'.format(float(self.info.unit)).zfill(16)+ '\n')

        for lat in self.info.lattice:
            f.write(' ')
            for num in lat:
                f.write(' ' + '{0:11.6f}'.format(float(num)))
            f.write('\n')

        for key in self.info.elements.keys():
            f.write('{0:>4s}'.format(key) + ' ')
        f.write('\n')

        for val in self.info.elements.values():
            f.write('{0:>6d}'.format(val.num))
        f.write('\n')
        if self.info.cartesian is False:
            f.write('Direct')
        else:
            f.write('Cartesian')
        f.write('\n')

        for atom in self.info.atoms:
            for num in atom.coordinate:
                f.write(' ' + '{0:9.6f}'.format(num))
            f.write('\n')
        f.write('\n')

        for num in self.info.chgcell:
            f.write(' ' + '{0:>4d}'.format(num))
        for i, chg in enumerate(self.info.chgsum):
            if i % 5 == 0:
                f.write('\n')
            f.write(' ' + '{0: 18.11E}'.format(chg))
        for i, atom in enumerate(self.info.atoms):
            f.write('\n')
            f.write('augmentation occupancies')
            f.write(' ' + '{0:3d}'.format(i + 1))
            f.write(' ' + '{0:3d}'.format(len(atom.augsum)))
            for j, augsum in enumerate(atom.augsum):
                if j % 5 == 0:
                    f.write('\n')
                f.write(' ' + '{0: 13.7E}'.format(float(augsum)))

        for i, atom in enumerate(self.info.atoms):
            if i % 5 == 0:
                f.write('\n')
            f.write(' ' + '{0: 18.12E}'.format(float(atom.chgn)))
        f.write('\n')

        for num in self.info.chgcell:
            f.write(' ' + '{0:>4d}'.format(num))
        for i, chg in enumerate(self.info.chgdif):
            if i % 5 == 0:
                f.write('\n')
            f.write(' ' + '{0: 18.11E}'.format(chg))
        f.write('\n')
        for i, atom in enumerate(self.info.atoms):
            f.write('augmentation occupancies')
            f.write(' ' + '{0:3d}'.format(i + 1))
            f.write(' ' + '{0:3d}'.format(len(atom.augdif)))
            for j, augdif in enumerate(atom.augdif):
                if j % 5 == 0:
                    f.write('\n')
                f.write(' ' + '{0: 13.7E}'.format(float(augdif)))
            f.write('\n')
