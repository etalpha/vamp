from vaspm.lib.info import Info
from vaspm.lib.poscar import Poscar
from vaspm.lib.incar import Incar
from vaspm.lib.doscar import Doscar
from vaspm.lib.com import Com
import numpy as np
import os


class Vaspm:

    def __init__(self, *args):
        if isinstance(args[0], Info):
            self.info = args[0]
        else:
            self.info = Info()
        self._poscar = Poscar(self.info)
        self._incar = Incar(self.info)
        self._doscar = Doscar(self.info)
        self.com = Com(self.info)
        self.tags = self.info.tags
        self.atoms = self.info.atoms
        for arg in args:
            if isinstance(arg, str):
                self.read(arg)

    def read(self, *args):
        for arg in args:
            if os.path.isdir(arg):
                self.read_poscar(arg)
                self.read_incar(arg)
            else:
                if 'POSCAR' in arg:
                    self.read_poscar(arg)
                elif 'INCAR' in arg:
                    self.read_incar(arg)

    def write(self, num):
        self.write_poscar('POSCAR' + num)
        self.write_incar('INCAR' + num)

    def read_poscar(self, adress='POSCAR'):
        if os.path.isfile(adress):
            self._poscar.read(adress)
        elif os.path.isdir(adress):
            adress = os.path.join(adress, 'POSCAR')
            if os.path.isfile(adress):
                self._poscar.read(adress)
        else:
            print('Failed to read')

    def write_poscar(self, adress):
        if os.path.isdir(adress):
            adress = os.path.join(adress, 'POSCAR')
        self._poscar.write(adress)

    def read_incar(self, adress='INCAR'):
        if os.path.isfile(adress):
            self._incar.read(adress)
        elif os.path.isdir(adress):
            adress = os.path.join(adress, 'INCAR')
            if os.path.isfile(adress):
                self._incar.read(adress)
        else:
            print('Failed to read')

    def write_incar(self, adress):
        if os.path.isdir(adress):
            adress = os.path.join(adress, 'INCAR')
        self._incar.write(adress)

    def read_com(self, adress):
        self.com.read(adress)

    def read_PDOS(self, DOSCAR):
        self._doscar.read(DOSCAR)

    def translation(self, vector, belong=None):
        'translation'
        self.info.atoms.translation(vector, belong)

    def transform(self, matrix, belong=None):
        'rotation'
        self.info.atoms.transform(matrix, belong)

    def rotation(self, axis, center, theta=None, belong=None):
        '''Using Rodrigues\'s formula
        axis is rotation axis.
        center is rotation center.
        theta is rotation angle.
        If you specify belong, it rotate atoms which belong to
        your specify.'''
        self.info.atoms.rotation(axis, center, theta, belong)

    def set_magmom_pos_to_in(self):
        self.info.set_magmom_pos_to_in()

    def set_magmom_in_to_pos(self):
        self.info.set_magmom_in_to_pos()

    def set_LDAU_tag_to_elem(self):
        self.info.set_LDAU_tag_to_elem()

    def set_LDAU_elem_to_tag(self):
        self.info.set_LDAU_elem_to_tag()

    def set_num(self):
        for num, atom in enumerate(self.atoms):
            atom.comment = atom.name + str(num + 1)

    def get_belonginfo(self, other):
        'get belonginfo from other'
        if len(self.atoms) != len(other.atoms):
            raise RuntimeError('number of atoms not consistant')
        for atom, otom in zip(self.atoms, other.atoms):
            atom.belong = otom.belong

    def __add__(self, other):
        info = self.info + other.info
        ret = Vaspm(info)
        return ret

    def split(self):
        infos = self.info.split()
        # print(infos)
        ret = dict()
        for bel, info in infos.items():
            ret[bel] = Vaspm(info)
        return ret

    def cartesianyzation(self):
        self.info.cartesianyzation()

    def set_belong(self, name=None):
        if name is None:
            self.info.atoms.set_belong(self.info.incar['SYSTEM'])
        else:
            self.info.atoms.set_belong(name)
