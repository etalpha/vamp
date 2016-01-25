from .frw import Frw
from .tag import Tag
from .atom import Atom
from .element import Element
import re


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
        print(self.info.cartesian)
        for key, val in self.info.elements.items():
            for i in range(1, val.num + 1):
                self.info.atoms.append(Atom(key, self.nextline()))
        self.nextline()
        cells = self.nextline()
        cells = list(map(int, cells))
        self.info.chgcell = cells
        ncell = cells[0] * cells[1] * cells[2]
        chgs = []
        print(ncell)
        for i in range(int(ncell / 5) + 1):
            chgs += self.nextline()
        self.info.chgsum = chgs
        # aug
        for atom in self.info.atoms:
            chgs = []
            ncell = int(self.nextline()[3])
            for i in range(int(ncell / 5) + 1):
                chgs += self.nextline()
            atom.augsum = chgs
        chgn = []
        for i in range(int(len(self.info.atoms) / 5 + 1)):
            chgn += self.nextline()
        for n, atom in zip(chgn, self.info.atoms):
            atom.chgn = n
        cells = self.nextline()
        cells = list(map(int, cells))
        ncell = cells[0] * cells[1] * cells[2]
        chgs = []
        print(ncell)
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
        f.write(self.info.unit + '\n')
        for lat in self.info.lattice:
            f.write(' '.join(lat) + '\n')
        for key in self.info.elements.keys():
            f.write(key + ' ')
        f.write('\n')
        for val in self.info.elements.values():
            f.write(str(val.num) + ' ')
        f.write('\n')
        if self.info.cartesian is False:
            f.write('Direct')
        else:
            f.write('Cartesian')
        f.write('\n')
        for atom in self.info.atoms:
            f.write(' '.join(map(str, atom.coordinate)) + '\n')
        f.write('\n')
        f.write(' '.join(map(str, self.info.chgcell)) + '\n')
        for i, chg in enumerate(self.info.chgsum):
            f.write(str(chg) + ' ')
            if i % 5 == 4:
                f.write('\n')
        for i, atom in enumerate(self.info.atoms):
            f.write('\naugmentation occupancies   ')
            f.write(str(i + 1) + ' ')
            f.write(str(len(atom.augsum)) + '\n')
            for j, augsum in enumerate(atom.augsum):
                f.write(str(augsum))
                f.write(' ')
                if j % 5 == 4:
                    f.write('\n')
        f.write('\n')
        for i, atom in enumerate(self.info.atoms):
            f.write(atom.chgn + ' ')
            if i % 5 == 4:
                f.write('\n')
        f.write('\n')
        f.write(' '.join(map(str, self.info.chgcell)) + '\n')
        for i, chg in enumerate(self.info.chgdif):
            f.write(str(chg) + ' ')
            if i % 5 == 4:
                f.write('\n')
        for i, atom in enumerate(self.info.atoms):
            f.write('\naugmentation occupancies   ')
            f.write(str(i + 1) + ' ')
            f.write(str(len(atom.augdif)) + '\n')
            for j, augdif in enumerate(atom.augdif):
                f.write(str(augdif))
                f.write(' ')
                if j % 5 == 4:
                    f.write('\n')
