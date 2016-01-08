from vaspm.lib.info import Info
from vaspm.lib.poscar import Poscar
from vaspm.lib.incar import Incar
from vaspm.lib.doscar import Doscar
from vaspm.lib.com import Com
import os


class Vaspm:

    def __init__(self, info=None):
        if info:
            self.info = info
        else:
            self.info = Info()
        self._poscar = Poscar(self.info)
        self._incar = Incar(self.info)
        self._doscar = Doscar(self.info)
        self.com = Com(self.info)
        self.incar = self.info.incar
        self.atoms = self.info.atoms

    def read_poscar(self, adress):
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

    def read_incar(self, adress):
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

    def translation(self, vector):
        self.info.atoms.translation(vector)

    def transform(self, matrix):
        self.info.atoms.transform(matrix)

    def set_magmom_pos_to_in(self):
        self.info.set_magmom_pos_to_in()

    def set_magmom_in_to_pos(self):
        self.info.set_magmom_in_to_pos()

    def __add__(self, other):
        info = self.info + other.info
        ret = Vaspm(info)
        return ret

    def split(self):
        infos = self.info.split()
        print(infos)
        ret = dict()
        for bel, info in infos.items():
            ret[bel] = Vaspm(info)
        return ret

    def set_belong(self, name=None):
        if name is None:
            self.info.atoms.set_belong(self.info.incar['SYSTEM'])
        else:
            self.info.atoms.set_belong(name)
